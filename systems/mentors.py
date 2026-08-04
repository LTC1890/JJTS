
import sys
import os
import time

sys .path .insert (0 ,os .path .dirname (os .path .abspath (__file__ )))

import ui 
from ui import Color ,c 

MENTOR_COOLDOWN_SECONDS =45 *60 

MENTORS ={
"Satoru Gojo":{
"name":"Satoru Gojo",
"rank":"Grau Especial",
"tech":"Limitless + Six Eyes",
"available_after_rank":"Grau 4",
"available_if_karma_min":-50 ,
"always_available":True ,
"training_options":[
{
"name":"Aula de Controle de CE",
"cost_free":True ,
"reward":{"attr_bonus":{"controle":2 },"msg":"Gojo te ensina a refinar seu CE."},
"unlock":None ,
"desc":"Aprenda a controlar CE com mais precisao.",
},
{
"name":"Aula sobre Dominios",
"cost_free":True ,
"reward":{"unlock":"learned_simple_domain","msg":"Voce aprende Dominio Simples (Hollow Wicker Basket)."},
"unlock":"learned_simple_domain",
"desc":"Aprenda a criar um dominio defensivo.",
"available_if_level_min":10 ,
},
{
"name":"Treino Avancado: Controle Total",
"cost_free":True ,
"reward":{"attr_bonus":{"controle":5 ,"ce":3 },"msg":"Gojo te ensina segredos do CE."},
"unlock":None ,
"desc":"Treino profundo com o feiticeiro mais forte.",
"available_if_level_min":15 ,
"available_once":True ,
},
],
"intro":"Gojo aparece do nada. 'Yo! Vamos treinar um pouco?'",
"ascii":"ASCII_GOJO",
},
"Kento Nanami":{
"name":"Kento Nanami",
"rank":"Grau 1",
"tech":"Razao Proporcional (Ratio)",
"available_after_rank":"Grau 3",
"available_if_karma_min":0 ,
"training_options":[
{
"name":"Licao de Razao Proporcional",
"cost_free":True ,
"reward":{"attr_bonus":{"forca":3 ,"controle":2 },"msg":"Nanami te ensina a encontrar pontos fracos."},
"unlock":None ,
"desc":"Aprenda a identificar o ponto 7:3 do inimigo.",
},
{
"name":"Treino de Profissionalismo",
"cost_free":True ,
"reward":{"attr_bonus":{"vigor":3 ,"sorte":2 },"msg":"Nanami te ensina disciplina."},
"unlock":None ,
"desc":"Aprenda a eficiencia no combate.",
"available_once":True ,
},
{
"name":"Ensina RCT (Tecnica Reversa)",
"cost_free":True ,
"reward":{"unlock":"learned_rct","msg":"Voce aprende a inverter CE para curar."},
"unlock":"learned_rct",
"desc":"Aprenda a curar com CE.",
"available_if_level_min":12 ,
"available_if_control_min":15 ,
"available_once":True ,
},
],
"intro":"Nanami ajeita o relogio. 'Vou te ensinar. Mas sem horas extras.'",
"ascii":None ,
},
"Aoi Todo":{
"name":"Aoi Todo",
"rank":"Grau 1",
"tech":"Boogie Woogie",
"available_after_rank":"Grau 3",
"available_if_karma_min":-10 ,
"training_options":[
{
"name":"Pergunta: Qual seu tipo de mulher?",
"cost_free":True ,
"reward":{"attr_bonus":{"forca":4 ,"velocidade":3 },"msg":"Todo te aceita como melhor amigo!"},
"unlock":None ,
"desc":"Responda corretamente e ganhe amizade de Todo.",
"available_once":True ,
"special":"todo_question",
},
{
"name":"Treino de Combate Fisico",
"cost_free":True ,
"reward":{"attr_bonus":{"forca":3 ,"vigor":2 },"msg":"Todo te espanca... mas voce fica mais forte."},
"unlock":None ,
"desc":"Treino brutal com Todo.",
"available_once":False ,
},
{
"name":"Treino de Combos",
"cost_free":True ,
"reward":{"attr_bonus":{"velocidade":4 ,"controle":2 },"msg":"Todo te ensina a usar o campo de batalha."},
"unlock":None ,
"desc":"Aprenda combos e troca de posicao.",
"available_once":True ,
},
],
"intro":"Todo surge bufando. 'VOCE! Qual seu tipo de mulher?'",
"ascii":None ,
},
"Maki Zenin (Treino Fisico)":{
"name":"Maki Zenin",
"rank":"Grau 1",
"tech":"Restricao Celestial",
"available_after_rank":"Grau 3",
"available_if_karma_min":0 ,
"training_options":[
{
"name":"Treino de Armas",
"cost_free":True ,
"reward":{"attr_bonus":{"forca":3 ,"vigor":2 },"msg":"Maki te ensina a usar armas amaldicoadas."},
"unlock":None ,
"desc":"Aprenda combate com arma.",
},
{
"name":"Treino de Velocidade",
"cost_free":True ,
"reward":{"attr_bonus":{"velocidade":4 ,"forca":1 },"msg":"Maki te faz correr ate cair."},
"unlock":None ,
"desc":"Treino cardiovascular brutal.",
"available_once":False ,
},
],
"intro":"Maki te encara. 'Se nao aguenta, sai.",
"ascii":None ,
},
"Diretor Yaga":{
"name":"Masamichi Yaga",
"rank":"Grau 1",
"tech":"Construcao de Maldicoes (Dolls)",
"available_after_rank":"Grau 3",
"available_if_karma_min":0 ,
"training_options":[
{
"name":"Aula de Etica Jujutsu",
"cost_free":True ,
"reward":{"attr_bonus":{"controle":2 ,"ce":1 },"msg":"Yaga te ensina sobre responsabilidade."},
"unlock":None ,
"desc":"Aprenda sobre a etica dos feiticeiros.",
"available_once":True ,
},
],
"intro":"Yaga te encara. 'Voce tem responsabilidades agora.",
"ascii":None ,
},
}

def get_mentor (name ):
    return MENTORS .get (name )

def get_available_mentors (player ):

    rank_order =["Grau 4","Grau 3","Grau 2","Grau 1","Grau Especial"]
    player_rank_idx =rank_order .index (player .rank_system .rank )if player .rank_system .rank in rank_order else 0 
    available =[]
    for name ,data in MENTORS .items ():
        required_rank =data .get ("available_after_rank","Grau 4")
        req_idx =rank_order .index (required_rank )if required_rank in rank_order else 0 
        if player_rank_idx <req_idx :
            continue 
        if player .karma .karma <data .get ("available_if_karma_min",-100 ):
            continue 
        available .append (name )
    return available 

def show_mentor_menu (player ,ui_module ):

    ui_module .clear_screen ()
    ui_module .title_box ("  MENTORES DISPONIVEIS  ")

    available =get_available_mentors (player )
    if not available :
        ui_module .tprint (c ("\nNenhum mentor disponivel no momento.",Color .YELLOW ))
        ui_module .tprint ("Suba de rank para conhecer mais mentores.")
        ui_module .pause ()
        return 

    labels =[]
    for name in available :
        remaining =get_mentor_cooldown_remaining (player ,name )
        if remaining >0 :
            mins =int (remaining //60 )
            secs =int (remaining %60 )
            labels .append (f"{name } (cooldown: {mins }m {secs }s)")
        else :
            labels .append (f"{name } (disponivel)")
    labels .append ("Voltar")

    idx =ui_module .arrow_menu (labels ,title ="Escolha um mentor (cooldown: 45min por uso):")
    if idx <0 or idx ==len (labels )-1 :
        return 

    mentor_name =available [idx ]
    mentor =MENTORS [mentor_name ]
    train_with_mentor (player ,mentor ,ui_module )

def train_with_mentor (player ,mentor ,ui_module ):

    ui_module .clear_screen ()
    ui_module .title_box (f"  TREINO COM {mentor ['name'].upper ()}  ")

    if mentor .get ("ascii")and hasattr (ui ,mentor ["ascii"]):
        ui_module .show_ascii (getattr (ui ,mentor ["ascii"]),clear =False )

    ui_module .tprint (c (f"\n{mentor ['intro']}",Color .BRIGHT_CYAN ))
    ui_module .pause ()

    while True :
        ui_module .clear_screen ()
        ui_module .title_box (f"  TREINO COM {mentor ['name'].upper ()}  ")

        options =[]
        for opt in mentor ["training_options"]:

            if opt .get ("available_if_level_min")and player .level_system .level <opt ["available_if_level_min"]:
                label =f"{opt ['name']} (requer Level {opt ['available_if_level_min']})"
                options .append ({"label":label ,"desc":"(bloqueado)","blocked":True ,"opt":opt })
                continue 
            if opt .get ("available_if_control_min")and player .attributes .get ("controle",0 )<opt ["available_if_control_min"]:
                label =f"{opt ['name']} (requer Controle {opt ['available_if_control_min']})"
                options .append ({"label":label ,"desc":"(bloqueado)","blocked":True ,"opt":opt })
                continue 
            if opt .get ("available_once")and opt .get ("name")in player .mentors_used_once :
                label =f"{opt ['name']} (ja feito)"
                options .append ({"label":label ,"desc":"(bloqueado)","blocked":True ,"opt":opt })
                continue 
            options .append ({"label":opt ["name"],"desc":opt ["desc"],"blocked":False ,"opt":opt })

        options .append ({"label":"Voltar","desc":"","blocked":False ,"opt":None })

        labels =[o ["label"]for o in options ]
        idx =ui_module .arrow_menu (labels ,title ="O que voce quer aprender?")
        if idx <0 or idx ==len (options )-1 :
            return 

        selected =options [idx ]
        if selected .get ("blocked"):
            ui_module .tprint (c ("Opcao bloqueada.",Color .RED ))
            ui_module .pause ()
            continue 

        opt =selected ["opt"]

        cooldown_msg =check_mentor_cooldown (player ,mentor ["name"])
        if cooldown_msg is not None :
            ui_module .tprint (c (cooldown_msg ,Color .YELLOW ))
            ui_module .pause ()
            continue 

        ui_module .tprint (c (f"\n>> {opt ['name']}",Color .BRIGHT_MAGENTA +Color .BOLD ))

        if opt .get ("special")=="todo_question":
            ui_module .tprint ("Todo: 'Qual o seu tipo de mulher??'")
            ui_module .pause ()
            answers =[
            "Alta, com bunda grande (resposta correta)",
            "Baixinha e fofa",
            "Inteligente e gentil",
            "Nao tenho tempo para isso",
            ]
            a_idx =ui_module .arrow_menu (answers ,title ="Sua resposta:")
            if a_idx ==0 :
                ui_module .tprint (c ("Todo: 'ISSO! Voce eh meu melhor amigo!'",Color .BRIGHT_GREEN +Color .BOLD ))
                ui_module .tprint (c ("Todo te da um abraço que quase quebra suas costas.",Color .DIM ))
            else :
                ui_module .tprint (c ("Todo: 'Hmpf. Voce eh fraco.'",Color .YELLOW ))
                ui_module .tprint (c ("Todo te da um soco de treino. Mas ainda te ensina algo.",Color .DIM ))
            ui_module .pause ()

        reward =opt .get ("reward",{})
        if "attr_bonus"in reward :
            for attr ,bonus in reward ["attr_bonus"].items ():
                player .attributes [attr ]=player .attributes .get (attr ,0 )+bonus 
            ui_module .tprint (c (f"Atributos aumentados: {reward ['attr_bonus']}",Color .BRIGHT_GREEN ))

        if "unlock"in reward and reward ["unlock"]:
            if reward ["unlock"]=="learned_simple_domain":
                player .learned_simple_domain =True 
            elif reward ["unlock"]=="learned_rct":
                player .learned_rct =True 
            ui_module .tprint (c (f"Desbloqueado: {reward ['unlock']}",Color .BRIGHT_YELLOW +Color .BOLD ))

        ui_module .tprint (c (reward .get ("msg","Treino concluido."),Color .CYAN ))

        if opt .get ("available_once"):
            player .mentors_used_once .add (opt ["name"])

        if "Gojo"in mentor ["name"]:
            player .karma .on_train_with_gojo ()
            player .gojo_met =True 
            player .gojo_trained_count +=1 
        elif "Nanami"in mentor ["name"]:
            player .nanami_trained_count +=1 
        elif "Todo"in mentor ["name"]:
            player .todo_trained_count +=1 

        player .recalculate_derived ()
        player .hp =player .max_hp 
        player .ce_current =player .max_ce 

        player .mentor_last_used [mentor ["name"]]=time .time ()

        ui_module .pause ()

def check_mentor_cooldown (player ,mentor_name ):

    last_used =player .mentor_last_used .get (mentor_name ,0 )
    if last_used ==0 :
        return None 
    elapsed =time .time ()-last_used 
    if elapsed >=MENTOR_COOLDOWN_SECONDS :
        return None 
    remaining =MENTOR_COOLDOWN_SECONDS -elapsed 
    mins =int (remaining //60 )
    secs =int (remaining %60 )
    return (f"{mentor_name } esta em cooldown. "
    f"Faltam {mins }m {secs }s para treinar com ele novamente.")

def get_mentor_cooldown_remaining (player ,mentor_name ):

    last_used =player .mentor_last_used .get (mentor_name ,0 )
    if last_used ==0 :
        return 0 
    elapsed =time .time ()-last_used 
    if elapsed >=MENTOR_COOLDOWN_SECONDS :
        return 0 
    return MENTOR_COOLDOWN_SECONDS -elapsed
