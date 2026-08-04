import os 
import json 
import time 
import sys 
import hmac 
import hashlib 
import base64 

sys .path .insert (0 ,os .path .dirname (os .path .abspath (__file__ )))

from config import CONFIG 
from ui import Color ,c 

SAVE_DIR =os .path .join (os .path .dirname (os .path .dirname (os .path .abspath (__file__ ))),"saved games")
SAVE_INDEX =os .path .join (SAVE_DIR ,"saves_index.json")

SAVE_VERSION ="1.6.5"

_SAVE_SECRET =b"jjts-mahoraga-antisave-v1-do-not-share-this-key-9f3a7c2e"
_SAVE_FMT ="jjts_secure_v1"

def _xor_bytes (data ,key ):
    if not key :
        return data 
    return bytes (b ^key [i %len (key )]for i ,b in enumerate (data ))

def _sign_and_pack (data_dict ):
    raw =json .dumps (data_dict ,ensure_ascii =False ,default =str ,sort_keys =True ).encode ("utf-8")
    sig =hmac .new (_SAVE_SECRET ,raw ,hashlib .sha256 ).hexdigest ()
    obfuscated =_xor_bytes (raw ,_SAVE_SECRET )
    payload ={
    "fmt":_SAVE_FMT ,
    "sig":sig ,
    "blob":base64 .b64encode (obfuscated ).decode ("ascii"),
    }
    return payload 

def _unpack_and_verify (payload ):
    try :
        obfuscated =base64 .b64decode (payload ["blob"])
        raw =_xor_bytes (obfuscated ,_SAVE_SECRET )
        expected_sig =hmac .new (_SAVE_SECRET ,raw ,hashlib .sha256 ).hexdigest ()
        if not hmac .compare_digest (expected_sig ,payload .get ("sig","")):
            return None ,"tampered"
        data =json .loads (raw .decode ("utf-8"))
        return data ,None 
    except Exception :
        return None ,"corrupted"

def _read_save_file (filepath ):
    with open (filepath ,"r",encoding ="utf-8")as f :
        raw_json =json .load (f )
    if isinstance (raw_json ,dict )and raw_json .get ("fmt")==_SAVE_FMT :
        data ,error =_unpack_and_verify (raw_json )
        if error =="tampered":
            raise ValueError ("SAVE_TAMPERED")
        if error =="corrupted":
            raise ValueError ("SAVE_CORRUPTED")
        return data 
    return raw_json 

def _write_save_file (filepath ,data ):
    payload =_sign_and_pack (data )
    with open (filepath ,"w",encoding ="utf-8")as f :
        json .dump (payload ,f ,indent =2 ,ensure_ascii =False )

def ensure_save_dir ():
    if not os .path .exists (SAVE_DIR ):
        try :
            os .makedirs (SAVE_DIR )
        except (PermissionError ,OSError ):
            return False 
    return True 

def list_saves ():
    if not os .path .exists (SAVE_DIR ):
        return []
    saves =[]
    for fname in os .listdir (SAVE_DIR ):
        if fname .endswith (".json")and fname !="saves_index.json":
            filepath =os .path .join (SAVE_DIR ,fname )
            try :
                data =_read_save_file (filepath )
                saves .append ({
                "filename":fname ,
                "filepath":filepath ,
                "name":data .get ("player",{}).get ("name","Unknown"),
                "level":data .get ("player",{}).get ("level_system",{}).get ("level",1 ),
                "rank":data .get ("player",{}).get ("rank_system",{}).get ("rank","Grau 4"),
                "karma":data .get ("player",{}).get ("karma",{}).get ("karma",0 ),
                "timestamp":data .get ("timestamp",0 ),
                "date_str":data .get ("date_str",""),
                "playtime_turns":data .get ("player",{}).get ("playtime_turns",0 ),
                "save_version":data .get ("save_version","1.0"),
                "is_dead":data .get ("is_dead",False ),
                })
            except ValueError as e :
                saves .append ({
                "filename":fname ,
                "filepath":filepath ,
                "name":"[SAVE INVALIDO]",
                "level":0 ,"rank":"?","karma":0 ,"timestamp":0 ,"date_str":"",
                "playtime_turns":0 ,"save_version":"?",
                "is_dead":False ,
                "corrupted":True ,
                "corruption_reason":str (e ),
                })
            except (json .JSONDecodeError ,IOError ):
                continue 
    saves .sort (key =lambda x :x ["timestamp"],reverse =True )
    return saves 

def save_game (player ,slot_name =None ,is_dead =False ):
    if not ensure_save_dir ():
        return False ,"Nao foi possivel criar diretorio de saves."

    if not slot_name :
        slot_name =f"save_{int (time .time ())}"

    if not slot_name .endswith (".json"):
        slot_name =slot_name +".json"

    slot_name ="".join (ch for ch in slot_name if ch .isalnum ()or ch in "._-")

    filepath =os .path .join (SAVE_DIR ,slot_name )

    data ={
    "save_version":SAVE_VERSION ,
    "version":SAVE_VERSION ,
    "timestamp":time .time (),
    "date_str":time .strftime ("%Y-%m-%d %H:%M:%S"),
    "player":player .to_dict (),
    "config":CONFIG .to_dict (),
    "is_dead":is_dead ,
    }

    try :
        _write_save_file (filepath ,data )
        return True ,filepath 
    except (PermissionError ,IOError )as e :
        return False ,str (e )

def save_death_to_all_slots (player ,ui_module =None ):

    if not ensure_save_dir ():
        return 0 
    count =0 
    target_name =player .name 
    for fname in os .listdir (SAVE_DIR ):
        if not fname .endswith (".json")or fname =="saves_index.json":
            continue 
        filepath =os .path .join (SAVE_DIR ,fname )
        try :
            data =_read_save_file (filepath )
            saved_name =data .get ("player",{}).get ("name","")
            if saved_name ==target_name :
                slot_name =fname .replace (".json","")
                ok ,_ =save_game (player ,slot_name ,is_dead =True )
                if ok :
                    count +=1 
        except (json .JSONDecodeError ,IOError ,ValueError ):
            continue 
    if ui_module and count >0 :
        ui_module .tprint (c (f"[Estado de morte salvo em {count } slot(s).]",Color .DIM ))
    return count 

def wipe_all_saves_for_character (player_name ,ui_module =None ):

    if not os .path .exists (SAVE_DIR ):
        return 0 
    count =0 
    for fname in list (os .listdir (SAVE_DIR )):
        if not fname .endswith (".json")or fname =="saves_index.json":
            continue 
        filepath =os .path .join (SAVE_DIR ,fname )
        try :
            data =_read_save_file (filepath )
            saved_name =data .get ("player",{}).get ("name","")
            if saved_name ==player_name :
                try :
                    os .remove (filepath )
                    count +=1 
                except (PermissionError ,IOError ):
                    pass 
        except (json .JSONDecodeError ,IOError ,ValueError ):
            continue 
    if ui_module :
        if count >0 :
            ui_module .tprint (c (f"[{count } save(s) apagado(s) pelo Selo de Dedo.]",Color .BRIGHT_RED ))
        else :
            ui_module .tprint (c ("[Nenhum save encontrado para apagar.]",Color .DIM ))
    return count 

def _migrate_save_data (data ):
    if not isinstance (data ,dict ):
        return data 

    save_ver =data .get ("save_version","1.0")

    if "player"not in data or not isinstance (data ["player"],dict ):
        data ["player"]={}

    player =data ["player"]

    if "rank_system"not in player or not isinstance (player ["rank_system"],dict ):
        player ["rank_system"]={}
    if "level_system"not in player or not isinstance (player ["level_system"],dict ):
        player ["level_system"]={}
    if "karma"not in player or not isinstance (player ["karma"],dict ):
        player ["karma"]={}
    if "attributes"not in player or not isinstance (player ["attributes"],dict ):
        player ["attributes"]={
        "forca":10 ,"ce":10 ,"controle":10 ,
        "velocidade":10 ,"vigor":10 ,"sorte":10 
        }
    if "equipped"not in player or not isinstance (player ["equipped"],dict ):
        player ["equipped"]={"arma":None ,"amuletos":[None ,None ,None ,None ,None ]}
    else :
        if "amuletos"not in player ["equipped"]or not isinstance (player ["equipped"].get ("amuletos"),list ):
            old_amul =player ["equipped"].get ("amuleto")
            amuletos =[None ,None ,None ,None ,None ]
            if old_amul :
                amuletos [0 ]=old_amul 
            player ["equipped"]["amuletos"]=amuletos 
        if "amuleto"in player ["equipped"]:
            del player ["equipped"]["amuleto"]
    if "inventory"not in player or not isinstance (player ["inventory"],dict ):
        player ["inventory"]={}
    if "completed_stories"not in player :
        player ["completed_stories"]=[]
    if "mentors_used_once"not in player :
        player ["mentors_used_once"]=[]
    if "mentor_last_used"not in player or not isinstance (player ["mentor_last_used"],dict ):
        player ["mentor_last_used"]={}
    if "tamed_shikigami"not in player or not isinstance (player ["tamed_shikigami"],list ):
        player ["tamed_shikigami"]=[]
    if "sukuna_mastered"not in player :
        player ["sukuna_mastered"]=False 
    if "dmg_buff_next_battle"not in player :
        player ["dmg_buff_next_battle"]=0.0 
    if "xp_mult_battles_left"not in player :
        player ["xp_mult_battles_left"]=0 
    if "sukuna_fingers_eaten"not in player :
        player ["sukuna_fingers_eaten"]=0 
    if "sukuna_control_pct"not in player :
        player ["sukuna_control_pct"]=0 
    if "sukuna_fingers_in_inventory"not in player :
        player ["sukuna_fingers_in_inventory"]=0 
    if "learned_simple_domain"not in player :
        player ["learned_simple_domain"]=False 
    if "learned_rct"not in player :
        player ["learned_rct"]=False 
    if "auto_allocate_build"not in player :
        player ["auto_allocate_build"]=None 
    if "auto_sell_list"not in player :
        player ["auto_sell_list"]=[]
    if "technique_roulette_count"not in player :
        player ["technique_roulette_count"]=0 
    if "trait_roulette_count"not in player :
        player ["trait_roulette_count"]=0 

    data ["save_version"]=SAVE_VERSION 
    data ["migrated_from"]=save_ver 

    return data 

def load_game (filepath ):
    if not os .path .exists (filepath ):
        return None ,"Arquivo nao encontrado."

    try :
        data =_read_save_file (filepath )
    except ValueError as e :
        if str (e )=="SAVE_TAMPERED":
            return None ,"Este save foi alterado fora do jogo e nao pode ser carregado (falha de integridade)."
        return None ,"Este save esta corrompido e nao pode ser carregado."
    except (json .JSONDecodeError ,IOError )as e :
        return None ,str (e )

    data =_migrate_save_data (data )

    from player import Player 
    player =Player ()
    player .from_dict (data .get ("player",{}))

    return player ,"OK"

def delete_save (filepath ):
    try :
        os .remove (filepath )
        return True 
    except (PermissionError ,IOError ,FileNotFoundError ):
        return False 

def show_load_menu (ui_module ):
    ui_module .screen_header (ui_module .ASCII_SAVE ,"JOGOS SALVOS",color =Color .BRIGHT_CYAN )

    saves =list_saves ()
    if not saves :
        ui_module .tprint (c ("\nNenhum save encontrado.",Color .YELLOW ))
        ui_module .tprint (c (f"Pasta de saves: {SAVE_DIR }",Color .DIM ))
        ui_module .pause ()
        return None 

    labels =[]
    for s in saves :
        if s .get ("corrupted"):
            labels .append (c (f"{s ['filename']} - [SAVE INVALIDO/ALTERADO]",Color .RED ))
            continue 
        ver_tag =""
        if s .get ("save_version","1.0")!=SAVE_VERSION :
            ver_tag =c (f" [v{s .get ('save_version','1.0')}]",Color .DIM )
        dead_tag =c (" [MORTO]",Color .BRIGHT_RED +Color .BOLD )if s .get ("is_dead")else ""
        label =f"{s ['name']} - Lv.{s ['level']} {s ['rank']} | {s ['date_str']}{ver_tag }{dead_tag }"
        labels .append (label )
    labels .append ("Voltar")

    idx =ui_module .arrow_menu (labels ,title ="Escolha um save:")
    if idx <0 or idx ==len (saves ):
        return None 

    selected =saves [idx ]
    player ,msg =load_game (selected ["filepath"])
    if player is None :
        ui_module .tprint (c (f"Erro ao carregar: {msg }",Color .RED ))
        ui_module .pause ()
        return None 

    save_ver =selected .get ("save_version","1.0")
    if save_ver !=SAVE_VERSION :
        ui_module .tprint (c (f"\n[Save v{save_ver } migrado para v{SAVE_VERSION } com sucesso.]",Color .DIM ))

    if selected .get ("is_dead"):
        ui_module .tprint (c ("\n!! ESTE PERSONAGEM ESTA MORTO !!",Color .BRIGHT_RED +Color .BOLD ))
        ui_module .tprint (c ("Ele foi salvo como morto. Nao pode ser continuado.",Color .RED ))
        ui_module .tprint (c ("Apenas o historico permanece.",Color .DIM ))
        ui_module .pause ()
        return None 

    ui_module .tprint (c (f"\nJogo carregado: {selected ['name']}",Color .BRIGHT_GREEN ))
    ui_module .pause ()
    return player 

def show_save_menu (player ,ui_module ):
    ui_module .screen_header (ui_module .ASCII_SAVE ,"SALVAR JOGO",color =Color .BRIGHT_GREEN )

    options =["Novo slot de save"]
    saves =list_saves ()
    for s in saves [:5 ]:
        dead_tag =" [MORTO]"if s .get ("is_dead")else ""
        options .append (f"Sobrescrever: {s ['name']} - {s ['date_str']}{dead_tag }")
    options .append ("Voltar")

    idx =ui_module .arrow_menu (options ,title ="Escolha onde salvar:")
    if idx <0 or idx ==len (options )-1 :
        return 

    if idx ==0 :
        ui_module .tprint (c ("\nDigite o nome do save (ou deixe vazio para auto):",Color .BRIGHT_YELLOW ))
        name =input ("> ").strip ()
        if not name :
            name =player .name 
        slot_name =name 
    else :
        selected =saves [idx -1 ]
        slot_name =selected ["filename"].replace (".json","")

    success ,msg =save_game (player ,slot_name )
    if success :
        ui_module .tprint (c ("\nJogo salvo com sucesso!",Color .BRIGHT_GREEN ))
        ui_module .tprint (c (f"Arquivo: {msg }",Color .DIM ))
    else :
        ui_module .tprint (c (f"\nErro ao salvar: {msg }",Color .RED ))
    ui_module .pause ()

def quicksave (player ,ui_module =None ,is_dead =False ):
    success ,msg =save_game (player ,"quicksave",is_dead =is_dead )
    if ui_module :
        if success :
            if is_dead :
                ui_module .tprint (c ("[Quick Save: estado de MORTO salvo]",Color .BRIGHT_RED ))
            else :
                ui_module .tprint (c ("[Quick Save OK]",Color .BRIGHT_GREEN ))
        else :
            ui_module .tprint (c (f"[Quick Save Falhou: {msg }]",Color .RED ))

def quickload (ui_module ):
    filepath =os .path .join (SAVE_DIR ,"quicksave.json")
    player ,msg =load_game (filepath )
    if player is None :
        ui_module .tprint (c (f"Quick Load falhou: {msg }",Color .RED ))
        return None 
    return player 

def autosave_after_battle (player ,ui_module =None ):

    if not CONFIG .auto_save :
        return 
    target_name =player .name 
    saved_count =0 
    if not ensure_save_dir ():
        return 
    for fname in list (os .listdir (SAVE_DIR )):
        if not fname .endswith (".json")or fname =="saves_index.json"or fname =="quicksave.json":
            continue 
        filepath =os .path .join (SAVE_DIR ,fname )
        try :
            data =_read_save_file (filepath )
            saved_name =data .get ("player",{}).get ("name","")
            if saved_name ==target_name :
                slot_name =fname .replace (".json","")
                ok ,_ =save_game (player ,slot_name ,is_dead =False )
                if ok :
                    saved_count +=1 
        except (json .JSONDecodeError ,IOError ,ValueError ):
            continue 
    quicksave (player ,ui_module =None )
    if ui_module and saved_count >0 :
        ui_module .tprint (c (f"[Auto-save: {saved_count } slot(s) atualizado(s)]",Color .DIM ))
