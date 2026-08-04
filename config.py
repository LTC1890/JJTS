import os 
import json 

CONFIG_DIR =os .path .dirname (os .path .abspath (__file__ ))
CONFIG_FILE =os .path .join (CONFIG_DIR ,"jjts_config.json")

TEXT_SPEEDS ={
"Lento":0.08 ,
"Normal":0.025 ,
"Rapido":0.008 ,
"Instantaneo":0.0 ,
}

DIFFICULTY_MODS ={
"Facil":{
"enemy_hp":0.7 ,"enemy_dmg":0.7 ,"enemy_def":0.8 ,"enemy_speed":0.9 ,
"enemy_ai_aggression":0.7 ,
"xp_mult":1.4 ,"drop_mult":1.5 ,
"stun_resist_bonus":-0.15 ,
"player_hp_mult":1.25 ,"player_ce_mult":1.20 ,
"permadeath":False ,"wipe_all_saves_on_death":False ,
"desc":"Inimigos fracos, mais XP e drops, jogador com HP/CE maiores.",
},
"Normal":{
"enemy_hp":1.0 ,"enemy_dmg":1.0 ,"enemy_def":1.0 ,"enemy_speed":1.0 ,
"enemy_ai_aggression":1.0 ,
"xp_mult":1.0 ,"drop_mult":1.0 ,
"stun_resist_bonus":0.0 ,
"player_hp_mult":1.0 ,"player_ce_mult":1.0 ,
"permadeath":False ,"wipe_all_saves_on_death":False ,
"desc":"Experiencia padrao.",
},
"Pesadelo":{
"enemy_hp":1.5 ,"enemy_dmg":1.4 ,"enemy_def":1.25 ,"enemy_speed":1.15 ,
"enemy_ai_aggression":1.35 ,
"xp_mult":0.85 ,"drop_mult":0.8 ,
"stun_resist_bonus":0.15 ,
"player_hp_mult":0.90 ,"player_ce_mult":0.90 ,
"permadeath":False ,"wipe_all_saves_on_death":False ,
"desc":"Inimigos fortes, menos XP/drops, jogador levemente enfraquecido.",
},
"Selo de Dedo":{
"enemy_hp":2.2 ,"enemy_dmg":2.0 ,"enemy_def":1.5 ,"enemy_speed":1.3 ,
"enemy_ai_aggression":1.6 ,
"xp_mult":0.6 ,"drop_mult":0.6 ,
"stun_resist_bonus":0.30 ,
"player_hp_mult":0.85 ,"player_ce_mult":0.85 ,
"permadeath":True ,"wipe_all_saves_on_death":True ,
"desc":"PERMADEATH TOTAL. Morrer apaga TODOS os saves do personagem.",
},
}

DEFAULT_CONFIG ={
"text_speed":"Normal",
"difficulty":"Normal",
"ascii_art":True ,
"color_enabled":True ,
"auto_save":True ,
"auto_update":True ,
"admin_mode":False ,
"input_mode":"pc",
}

class Config :

    def __init__ (self ):
        self .text_speed ="Normal"
        self .difficulty ="Normal"
        self .ascii_art =True 
        self .color_enabled =True 
        self .auto_save =True 
        self .auto_update =True 
        self .admin_mode =False 
        self .input_mode ="pc"
        self .load ()

    def load (self ):
        if os .path .exists (CONFIG_FILE ):
            try :
                with open (CONFIG_FILE ,"r",encoding ="utf-8")as f :
                    data =json .load (f )
                    for k ,v in data .items ():
                        setattr (self ,k ,v )
            except (json .JSONDecodeError ,IOError ):
                pass 

    def save (self ):
        data ={
        "text_speed":self .text_speed ,
        "difficulty":self .difficulty ,
        "ascii_art":self .ascii_art ,
        "color_enabled":self .color_enabled ,
        "auto_save":self .auto_save ,
        "auto_update":self .auto_update ,
        "input_mode":self .input_mode ,
        }
        try :
            with open (CONFIG_FILE ,"w",encoding ="utf-8")as f :
                json .dump (data ,f ,indent =2 ,ensure_ascii =False )
        except IOError :
            pass 

    def get_text_delay (self ):
        return TEXT_SPEEDS .get (self .text_speed ,0.025 )

    def get_difficulty_mod (self ):
        return DIFFICULTY_MODS .get (self .difficulty ,DIFFICULTY_MODS ["Normal"])

    def is_permadeath (self ):
        return self .get_difficulty_mod ().get ("permadeath",False )

    def wipes_all_saves_on_death (self ):
        return self .get_difficulty_mod ().get ("wipe_all_saves_on_death",False )

    def get_stun_resist_bonus (self ):
        return self .get_difficulty_mod ().get ("stun_resist_bonus",0.0 )

    def get_player_hp_mult (self ):
        return self .get_difficulty_mod ().get ("player_hp_mult",1.0 )

    def get_player_ce_mult (self ):
        return self .get_difficulty_mod ().get ("player_ce_mult",1.0 )

    def get_enemy_hp_mult (self ):
        return self .get_difficulty_mod ().get ("enemy_hp",1.0 )

    def get_enemy_dmg_mult (self ):
        return self .get_difficulty_mod ().get ("enemy_dmg",1.0 )

    def get_enemy_def_mult (self ):
        return self .get_difficulty_mod ().get ("enemy_def",1.0 )

    def get_enemy_speed_mult (self ):
        return self .get_difficulty_mod ().get ("enemy_speed",1.0 )

    def get_enemy_ai_aggression (self ):
        return self .get_difficulty_mod ().get ("enemy_ai_aggression",1.0 )

    def is_mobile (self ):
        return self .input_mode =="mobile"

    def to_dict (self ):
        return {
        "text_speed":self .text_speed ,
        "difficulty":self .difficulty ,
        "ascii_art":self .ascii_art ,
        "color_enabled":self .color_enabled ,
        "auto_save":self .auto_save ,
        "admin_mode":self .admin_mode ,
        "auto_update":self .auto_update ,
        "input_mode":self .input_mode ,
        }

CONFIG =Config ()

def check_admin_privileges ():
    try :
        if os .name =="nt":
            import ctypes 
            return ctypes .windll .shell32 .IsUserAnAdmin ()!=0 
        else :
            return os .geteuid ()==0 
    except Exception :
        return False 

def try_elevate_privileges ():
    if check_admin_privileges ():
        return True 
    try :
        if os .name =="nt":
            import ctypes 
            params =" ".join ([f'"{arg }"'for arg in sys_args ()])
            ctypes .windll .shell32 .ShellExecuteW (
            None ,"runas",sys_executable (),params ,None ,1 
            )
            return True 
        else :
            return False 
    except Exception :
        return False 

def sys_executable ():
    import sys 
    return sys .executable 

def sys_args ():
    import sys 
    return sys .argv
