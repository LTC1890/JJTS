
import random 
import sys 
import os 

sys .path .insert (0 ,os .path .dirname (os .path .abspath (__file__ )))

from ui import Color ,c
from items import ITEMS_DB ,roll_loot 
from generator import generate_procedural_curse ,generate_procedural_sorcerer 

EVENTS =[

{
"id":"civil_em_perigo",
"name":"Civil em Perigo",
"weight":20 ,
"text":"Voce caminha por uma rua escura. Uma maldicao de baixo rank esta prestes a comer um civil.",
"options":[
{"label":"Salvar o civil (inicia batalha)","effect":"battle_save_civil",
"desc":"+karma, mas custa tempo"},
{"label":"Ignorar e focar na missao","effect":"ignore_civil",
"desc":"-karma, mas segue"},
],
},
{
"id":"objeto_amaldicoado_chao",
"name":"Objeto Amaldicoado",
"weight":15 ,
"text":"Voce encontrou um objeto amaldicoado de grau 1 no chao. Ele pulsa com CE.",
"options":[
{"label":"Pegar o objeto","effect":"pickup_item",
"desc":"Item aleatorio"},
{"label":"Selar e levar para escola","effect":"seal_item",
"desc":"+karma, +reputacao"},
{"label":"Destruir","effect":"destroy_item",
"desc":"+karma, sem item"},
],
},
{
"id":"clima_amaldicoado",
"name":"Clima Amaldicoado",
"weight":10 ,
"text":"A energia amaldicoada esta densa hoje. Todas as maldicoes estao 20% mais fortes, mas o drop de XP eh maior.",
"options":[
{"label":"Aceitar a bencao (1 dia)","effect":"accept_curse_weather",
"desc":"+30% XP, maldicoes +20%"},
],
"automatic":True ,
},
{
"id":"feiticeiro_ferido",
"name":"Feiticeiro Ferido",
"weight":8 ,
"text":"Voce encontra um feiticeiro ferido. Ele pede ajuda.",
"options":[
{"label":"Ajuda-lo (cura itens)","effect":"help_sorcerer",
"desc":"+karma, ganha aliado temporario"},
{"label":"Roubar seus itens","effect":"rob_sorcerer",
"desc":"-karma, ganha itens"},
],
},
{
"id":"vendedor_ambulante",
"name":"Vendedor Ambulante",
"weight":10 ,
"text":"Um vendedor misterioso aparece. 'Tenho itens raros... por um preco.'",
"options":[
{"label":"Ver mercadorias","effect":"merchant_shop",
"desc":"Loja especial"},
{"label":"Recusar","effect":"nothing",
"desc":"Continuar"},
],
},
{
"id":"ritual_amaldicoado",
"name":"Ritual Amaldicoado",
"weight":8 ,
"text":"Voce presencia um ritual amaldicoado. Maldicoes estao sendo convocadas!",
"options":[
{"label":"Interromper o ritual","effect":"interrupt_ritual",
"desc":"+karma, batalha"},
{"label":"Esperar e observar","effect":"watch_ritual",
"desc":"Aprende algo, mas maldicoes surgem"},
],
},
{
"id":"dedo_sukuna_rumor",
"name":"Rumor de Dedo",
"weight":5 ,
"text":"Boatos de que um Dedo de Sukuna apareceu na cidade. Mas voce nao eh o unico cacador.",
"options":[
{"label":"Investigar","effect":"investigate_finger",
"desc":"Possivel batalha com rival"},
{"label":"Ignorar boatos","effect":"nothing",
"desc":"Continuar"},
],
},
{
"id":"maldicao_fugitiva",
"name":"Maldicao Fugitiva",
"weight":12 ,
"text":"Uma maldicao foge ao te ver. Pode estar indo atacar civis.",
"options":[
{"label":"Perseguir","effect":"chase_curse",
"desc":"+XP, +karma"},
{"label":"Deixar ir","effect":"nothing",
"desc":"-karma menor"},
],
},
{
"id":"encontro_com_gojo",
"name":"Encontro com Gojo",
"weight":4 ,
"text":"Satoru Gojo aparece do nada. 'Yo! Que surpresa. Treinando?'",
"options":[
{"label":"Conversar","effect":"talk_gojo",
"desc":"+relacao com Gojo"},
{"label":"Pedir treino","effect":"ask_train_gojo",
"desc":"Treino rapido"},
],
"requires_not_met_gojo":False ,
},
{
"id":"maldicao_especial_subita",
"name":"Maldicao Especial Subita",
"weight":3 ,
"text":"Uma maldicao de Grau Especial surge do nada! Voce nao esperava por isso.",
"options":[
{"label":"Lutar (altissimo risco)","effect":"fight_special",
"desc":"Recompensa massiva"},
{"label":"Correr!","effect":"run_special",
"desc":"Fuga com chance de falha"},
],
},
{
"id":"sukuna_fala",
"name":"Sukuna Sussurra",
"weight":6 ,
"text":"Voce ouve uma voz na sua cabeca. 'Hm. Voce eh interessante. Aceitaria poder?'",
"options":[
{"label":"Aceitar pacto (-karma, +poder)","effect":"pact_sukuna",
"desc":"Poder imediato, karma negativo"},
{"label":"Recusar","effect":"refuse_sukuna",
"desc":"+karma, sem poder"},
],
"requires_sukuna_fingers":True ,
},
{
"id":"discipulo_amaldicao",
"name":"Discipulo Amaldicoado",
"weight":5 ,
"text":"Um jovem feiticeiro cobaia de maldicoes pede abrigo.",
"options":[
{"label":"Aceita como discipulo","effect":"accept_disciple",
"desc":"+reputacao, +karma"},
{"label":"Recusar","effect":"nothing",
"desc":"Continuar"},
],
},
{
"id":"fenomeno_celestial",
"name":"Fenomeno Celestial",
"weight":4 ,
"text":"O ceu brilha com energia amaldicoada. Voce sente seu CE crescer.",
"options":[
{"label":"Meditar (ganho de CE)","effect":"meditate_ce",
"desc":"+atributo CE"},
],
"automatic":True ,
},
{
"id":"encontro_com_nanami",
"name":"Encontro com Nanami",
"weight":5 ,
"text":"Kento Nanami, de terno e gravata, suspira ao ver voce. 'Fora do horario de trabalho...'",
"options":[
{"label":"Conversar profissionalmente","effect":"talk_nanami",
"desc":"+relacao"},
],
},
{
"id":"proposta_renegada",
"name":"Proposta Renegada",
"weight":3 ,
"text":"Um feiticeiro renegado te oferece uma proposta. 'Junte-se a nos. Poder real.'",
"options":[
{"label":"Aceitar (renegado)","effect":"join_renegade",
"desc":"-karma grande, +poder"},
{"label":"Recusar (lealdade)","effect":"refuse_renegade",
"desc":"+karma"},
{"label":"Denunciar","effect":"report_renegade",
"desc":"+karma, +reputacao, mas inimigo"},
],
"requires_karma_min":-30 ,
},
{
"id":"feiticeiro_cacador",
"name":"Feiticeiro Caçador",
"weight":6 ,
"text":"Sua reputacao chegou ao Jujutsu High. Um feiticeiro forte foi enviado para te deter "
"ou te trazer de volta - pela forca, se necessario.",
"options":[
{"label":"Enfrentar","effect":"fight_sorcerer_hunter",
"desc":"Combate dificil contra um feiticeiro canonico"},
{"label":"Tentar fugir","effect":"flee_sorcerer_hunter",
"desc":"Chance de escapar baseada em velocidade"},
],
"requires_karma_min":-25 ,
"automatic":False ,
},
]

def trigger_random_event (player ,ui_module ):

    available =[]
    for e in EVENTS :

        if e .get ("requires_sukuna_fingers")and player .sukuna_fingers_eaten ==0 :
            continue 
        if e .get ("requires_karma_min")and player .karma .karma >e ["requires_karma_min"]:
            continue 
        if e .get ("requires_not_met_gojo")is False and player .gojo_met :
            continue 
        available .append (e )

    if not available :
        return 

    weights =[e ["weight"]for e in available ]
    event =random .choices (available ,weights =weights )[0 ]

    return execute_event (player ,event ,ui_module )

def execute_event (player ,event ,ui_module ):

    ui_module .clear_screen ()
    ui_module .title_box (f"  EVENTO: {event ['name'].upper ()}  ")
    ui_module .tprint (c (f"\n{event ['text']}",Color .BRIGHT_CYAN ))
    ui_module .pause ()

    if event .get ("automatic"):

        apply_effect (player ,event ["options"][0 ]["effect"],ui_module ,event )
        return 

    labels =[f"{o ['label']} - {o ['desc']}"for o in event ["options"]]
    labels .append ("Ignorar")
    idx =ui_module .arrow_menu (labels ,title ="O que voce faz?")
    if idx <0 or idx ==len (event ["options"]):
        return 

    apply_effect (player ,event ["options"][idx ]["effect"],ui_module ,event )

def apply_effect (player ,effect ,ui_module ,event ):

    if effect =="nothing":
        ui_module .tprint (c ("Voce segue seu caminho.",Color .DIM ))
        ui_module .pause ()
        return 

    if effect =="fight_sorcerer_hunter":
        from enemies import get_sorcerer_boss_by_karma 
        karma_val =player .karma .karma 
        level_val =player .level_system .level 
        boss =get_sorcerer_boss_by_karma (karma_val ,level_val )
        if boss is None :
            ui_module .tprint (c ("Ninguem forte o suficiente aparece ainda. Seu karma nao "
            "esta baixo o bastante (ou seu nivel ainda nao e suficiente) para atrair "
            "a atencao dos feiticeiros mais fortes.",Color .DIM ))
            ui_module .pause ()
            return 
        ui_module .tprint (c (f"\n{boss ['intro']}",Color .BRIGHT_RED +Color .BOLD ))
        ui_module .pause ()
        from combat import Combat 
        from allies import get_available_allies ,get_ally 
        allies =[]
        available =get_available_allies (player )
        if available and random .random ()<0.5 :
            allies =[get_ally (random .choice (available ))]
        combat =Combat (player ,[boss ],allies ,ui_module =ui_module )
        result =combat .start ()
        if result =="victory":
            karma_bonus =abs (boss .get ("karma_reward",-5 ))
            ui_module .tprint (c (f"\nVoce derrotou {boss ['name']}! Sua lenda cresce.",
            Color .BRIGHT_YELLOW +Color .BOLD ))
        return 

    if effect =="flee_sorcerer_hunter":
        speed =player .get_total_speed ()
        flee_chance =min (0.85 ,0.35 +speed *0.01 )
        if random .random ()<flee_chance :
            ui_module .tprint (c ("Voce consegue escapar antes que ele te alcance.",
            Color .BRIGHT_GREEN ))
            ui_module .pause ()
            return 
        ui_module .tprint (c ("Voce nao consegue fugir! Ele te alcanca.",Color .RED ))
        ui_module .pause ()
        apply_effect (player ,"fight_sorcerer_hunter",ui_module ,event )
        return 

    if effect =="battle_save_civil":

        from combat import Combat

        curse =generate_procedural_curse ("Grau 3",1.0 +player .level_system .level *0.03 )
        ui_module .tprint (c ("\nVoce enfrenta a maldicao!",Color .BRIGHT_RED ))
        ui_module .pause ()
        combat =Combat (player ,[curse ],[],ui_module =ui_module )
        result =combat .start ()
        if result =="victory":
            player .karma .on_civil_salvo ()
            ui_module .tprint (c ("Civil salvo! +karma",Color .BRIGHT_GREEN ))
            ui_module .pause ()

    elif effect =="ignore_civil":
        player .karma .on_civil_ignorado ()
        ui_module .tprint (c ("Voce ignora os gritos. Seu coracao fica mais frio.",Color .DIM ))
        ui_module .pause ()

    elif effect =="pickup_item":
        item =roll_loot (1.5 )
        if item =="Dedo de Sukuna":
            player .sukuna_fingers_in_inventory +=1 
        else :
            player .add_item (item )
        ui_module .tprint (c (f"Voce pega: {item }",Color .BRIGHT_GREEN ))
        ui_module .pause ()

    elif effect =="seal_item":
        player .karma .add_karma (3 )
        player .karma .add_reputacao (2 )
        ui_module .tprint (c ("Voce sela o objeto e leva para a escola. +karma, +reputacao",Color .BRIGHT_GREEN ))
        ui_module .pause ()

    elif effect =="destroy_item":
        player .karma .add_karma (5 )
        ui_module .tprint (c ("Voce destruiu o objeto. +karma",Color .BRIGHT_GREEN ))
        ui_module .pause ()

    elif effect =="accept_curse_weather":
        player .level_system .xp_mult =1.3 
        player .xp_mult_battles_left =5 
        ui_module .tprint (c ("A densidade de CE aumenta seu ganho de XP em 30%!",Color .BRIGHT_YELLOW ))
        ui_module .tprint (c ("(Efeito dura 5 batalhas)",Color .BRIGHT_CYAN ))
        ui_module .pause ()

    elif effect =="help_sorcerer":
        player .karma .add_karma (4 )
        player .add_item ("Selo de Cura")
        player .add_item ("Selo de CE Basico")
        ui_module .tprint (c ("O feiticeiro curado oferece itens. +karma",Color .BRIGHT_GREEN ))
        ui_module .pause ()

    elif effect =="rob_sorcerer":
        player .karma .add_karma (-8 )
        items_to_steal =["Cristal de CE","Sangue Amaldicoado","Selo de CE Avancado"]
        for it in random .sample (items_to_steal ,k =random .randint (1 ,2 )):
            player .add_item (it )
            ui_module .tprint (c (f"+ {it }",Color .BRIGHT_RED ))
        ui_module .tprint (c ("-8 karma. Que vergonha.",Color .RED ))
        ui_module .pause ()

    elif effect =="merchant_shop":
        merchant_shop (player ,ui_module )

    elif effect =="interrupt_ritual":
        player .karma .add_karma (5 )
        ui_module .tprint (c ("Voce interrompe o ritual! Mas maldicoes te atacam!",Color .BRIGHT_RED ))
        ui_module .pause ()
        from combat import Combat 
        from generator import generate_enemy_group 
        enemies =generate_enemy_group (player .level_system .level ,2 ,1.0 )
        combat =Combat (player ,enemies ,[],ui_module =ui_module )
        result =combat .start ()

    elif effect =="watch_ritual":
        ui_module .tprint (c ("Voce observa escondido. Sua percepcao de CE melhora.",Color .CYAN ))
        player .attributes ["controle"]+=1 
        player .recalculate_derived ()

        if random .random ()<0.5 :
            ui_module .tprint (c ("\nMas elas te notaram!",Color .BRIGHT_RED ))
            ui_module .pause ()
            from combat import Combat

            enemies =[generate_procedural_curse ("Grau 2",1.0 +player .level_system .level *0.05 )]
            combat =Combat (player ,enemies ,[],ui_module =ui_module )
            combat .start ()
        ui_module .pause ()

    elif effect =="investigate_finger":
        ui_module .tprint (c ("Voce investiga o rumor...",Color .DIM ))
        ui_module .pause ()

        if random .random ()<0.5 :
            ui_module .tprint (c ("Um rival aparece!",Color .BRIGHT_RED ))
            ui_module .pause ()
            from combat import Combat

            rival =generate_procedural_sorcerer ("Grau 1",1.0 +player .level_system .level *0.05 )
            rival ["karma_reward"]=-8 
            combat =Combat (player ,[rival ],[],ui_module =ui_module )
            result =combat .start ()
            if result =="victory":

                if random .random ()<0.3 :
                    player .sukuna_fingers_in_inventory +=1 
                    ui_module .tprint (c ("Voce encontrou o Dedo de Sukuna!",Color .BRIGHT_RED +Color .BOLD ))
        else :

            if random .random ()<0.4 :
                player .sukuna_fingers_in_inventory +=1 
                ui_module .tprint (c ("Voce encontrou o Dedo de Sukuna!",Color .BRIGHT_RED +Color .BOLD ))
            else :
                ui_module .tprint (c ("Era um falso rumor. Nada encontrado.",Color .DIM ))
        ui_module .pause ()

    elif effect =="chase_curse":
        ui_module .tprint (c ("Voce persegue a maldicao!",Color .BRIGHT_RED ))
        ui_module .pause ()
        from combat import Combat

        curse =generate_procedural_curse ("Grau 2",1.0 +player .level_system .level *0.05 )
        combat =Combat (player ,[curse ],[],ui_module =ui_module )
        result =combat .start ()
        if result =="victory":
            player .karma .add_karma (2 )
            ui_module .tprint (c ("Maldicao exorcizada! +karma",Color .BRIGHT_GREEN ))

    elif effect =="talk_gojo":
        player .gojo_met =True 
        player .karma .on_train_with_gojo ()
        ui_module .tprint (c ("Gojo: 'Voce tem potencial. Continue assim.'",Color .BRIGHT_CYAN ))
        ui_module .tprint (c ("+relacao com Gojo",Color .BRIGHT_GREEN ))
        ui_module .pause ()

    elif effect =="ask_train_gojo":
        player .gojo_met =True 
        player .karma .on_train_with_gojo ()
        player .attributes ["controle"]+=2 
        player .recalculate_derived ()
        ui_module .tprint (c ("Gojo: 'Tudo bem, vou te dar uma dica.'",Color .BRIGHT_CYAN ))
        ui_module .tprint (c ("+2 Controle de CE",Color .BRIGHT_GREEN ))
        ui_module .pause ()

    elif effect =="fight_special":
        ui_module .tprint (c ("Voce enfrenta a maldicao especial!",Color .BRIGHT_RED +Color .BOLD ))
        ui_module .pause ()
        from combat import Combat 
        from enemies import random_boss 
        boss =random_boss ("Grau Especial")
        from allies import get_available_allies ,get_ally 
        allies =[]
        available =get_available_allies (player )
        if available :
            allies =[get_ally (random .choice (available ))]
        combat =Combat (player ,[boss ],allies ,ui_module =ui_module )
        result =combat .start ()

    elif effect =="run_special":
        speed =player .get_total_speed ()
        if random .random ()<0.4 +speed *0.01 :
            ui_module .tprint (c ("Voce consegue fugir!",Color .BRIGHT_GREEN ))
        else :
            ui_module .tprint (c ("Nao foi possivel fugir!",Color .RED ))
            ui_module .pause ()
            from combat import Combat 
            from enemies import random_boss 
            boss =random_boss ("Grau Especial")
            combat =Combat (player ,[boss ],[],ui_module =ui_module )
            combat .start ()

    elif effect =="pact_sukuna":
        player .karma .add_karma (-15 )
        player .karma .sukuna_relation =min (100 ,player .karma .sukuna_relation +10 )
        player .attributes ["forca"]+=5 
        player .attributes ["ce"]+=3 
        player .recalculate_derived ()
        player .hp =player .max_hp 
        ui_module .tprint (c ("Sukuna ri em sua mente. 'Boa escolha, inseto.'",Color .BRIGHT_RED +Color .BOLD ))
        ui_module .tprint (c ("+5 Forca, +3 CE, HP maximo. -15 karma.",Color .BRIGHT_YELLOW ))
        ui_module .pause ()

    elif effect =="refuse_sukuna":
        player .karma .add_karma (5 )
        ui_module .tprint (c ("Voce recusa o Rei das Maldicoes. Sua vontade se fortalece.",Color .BRIGHT_CYAN ))
        ui_module .tprint (c ("+5 karma",Color .BRIGHT_GREEN ))
        ui_module .pause ()

    elif effect =="accept_disciple":
        player .karma .add_karma (3 )
        player .karma .add_reputacao (3 )
        ui_module .tprint (c ("O jovem agradece. Sua reputacao cresce.",Color .BRIGHT_GREEN ))
        ui_module .pause ()

    elif effect =="meditate_ce":
        player .attributes ["ce"]+=2 
        player .ce_current =player .max_ce 
        player .recalculate_derived ()
        ui_module .tprint (c ("Voce medita sob o fenomeno. +2 CE.",Color .BRIGHT_CYAN ))
        ui_module .pause ()

    elif effect =="talk_nanami":
        player .nanami_trained_count +=1 
        player .attributes ["controle"]+=1 
        player .recalculate_derived ()
        ui_module .tprint (c ("Nanami: 'Trabalho efficiente. Nada mais.'",Color .DIM ))
        ui_module .tprint (c ("+1 Controle",Color .BRIGHT_GREEN ))
        ui_module .pause ()

    elif effect =="join_renegade":
        player .karma .add_karma (-25 )
        player .attributes ["forca"]+=8 
        player .attributes ["ce"]+=5 
        player .recalculate_derived ()
        ui_module .tprint (c ("Voce abraçou o caminho renegado.",Color .BRIGHT_RED +Color .BOLD ))
        ui_module .tprint (c ("Os feiticeiros vao te tratar como inimigo.",Color .RED ))
        ui_module .tprint (c ("+8 Forca, +5 CE. -25 karma.",Color .YELLOW ))
        ui_module .pause ()

    elif effect =="refuse_renegade":
        player .karma .add_karma (8 )
        ui_module .tprint (c ("Voce recusa. O renegado sorri. 'Vou lembrar disso.'",Color .BRIGHT_CYAN ))
        ui_module .pause ()

    elif effect =="report_renegade":
        player .karma .add_karma (10 )
        player .karma .add_reputacao (5 )
        ui_module .tprint (c ("Voce denuncia o renegado. A escola agradece.",Color .BRIGHT_GREEN ))
        ui_module .tprint (c ("Mas voce agora tem um inimigo.",Color .YELLOW ))
        ui_module .pause ()

def merchant_shop (player ,ui_module ):

    ui_module .clear_screen ()
    ui_module .title_box ("  VENDEDOR AMBULANTE  ")
    ui_module .tprint (c ("'Tenho itens raros... so pra voce.'",Color .BRIGHT_MAGENTA ))

    rare_items =[n for n ,d in ITEMS_DB .items ()if d ["rarity"]in ("raro","epico")and d ["price"]>0 ]
    offered =random .sample (rare_items ,k =min (5 ,len (rare_items )))

    labels =[]
    for item_name in offered :
        item =ITEMS_DB [item_name ]

        price =int (item ["price"]*random .uniform (0.7 ,1.3 ))
        labels .append (f"{item_name } - {price } ienes")
    labels .append ("Sair")

    idx =ui_module .arrow_menu (labels ,title =f"Seu dinheiro: {player .money } ienes")
    if idx <0 or idx ==len (offered ):
        return 

    item_name =offered [idx ]
    item =ITEMS_DB [item_name ]
    price =int (item ["price"]*random .uniform (0.7 ,1.3 ))

    if player .money <price :
        ui_module .tprint (c ("Dinheiro insuficiente!",Color .RED ))
        ui_module .pause ()
        return 

    player .money -=price 
    player .add_item (item_name )
    ui_module .tprint (c (f"Comprou {item_name }!",Color .BRIGHT_GREEN ))
    ui_module .pause ()
