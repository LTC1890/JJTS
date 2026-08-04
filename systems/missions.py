
import random 
import sys 
import os 

sys .path .insert (0 ,os .path .dirname (os .path .abspath (__file__ )))

from ui import Color ,c

MISSION_TEMPLATES ={
"Grau 4":[
{"name":"Investigar Desaparecimento","type":"dungeon","difficulty":1 ,
"desc":"Um civil desapareceu na regiao. Investigue e exorcize qualquer maldicao.",
"xp_reward":100 ,"money_reward":100 ,"min_danger":1 ,"max_danger":5 },
{"name":"Patrulha Noturna","type":"combat","difficulty":1 ,
"desc":"Patrulhe as ruas e exorcize maldicoes menores.",
"xp_reward":80 ,"money_reward":80 ,"num_enemies":2 ,"rank":"Grau 4"},
{"name":"Resgatar Civil","type":"combat","difficulty":1 ,
"desc":"Uma maldicao raptou um civil. Salve-o antes que seja tarde.",
"xp_reward":90 ,"money_reward":120 ,"num_enemies":1 ,"rank":"Grau 3",
"karma_bonus":3 },
{"name":"Limpar Parque Abandonado","type":"dungeon","difficulty":1 ,
"desc":"Maldicoes fracas infestam um parque. Limpe antes que ataquem criancas.",
"xp_reward":110 ,"money_reward":90 ,"min_danger":1 ,"max_danger":5 },
{"name":"Selar Objeto Amaldicoado Menor","type":"combat","difficulty":1 ,
"desc":"Um objeto amaldicoado grau 4 esta atraindo maldicoes. Destrua ou sele.",
"xp_reward":95 ,"money_reward":110 ,"num_enemies":2 ,"rank":"Grau 4"},
{"name":"Coletar Objetos Amaldicoados","type":"fetch","difficulty":1 ,
"desc":"Recupere 3 objetos amaldicoados perdidos.",
"xp_reward":70 ,"money_reward":100 ,"items_required":3 ,
"rare":True },
],
"Grau 3":[
{"name":"Limpar Casa Amaldicoada","type":"dungeon","difficulty":2 ,
"desc":"Uma familia fugiu de casa assombrada. Limpe todas as maldicoes.",
"xp_reward":250 ,"money_reward":200 ,"min_danger":5 ,"max_danger":10 },
{"name":"Selar Maldicao Visceral","type":"combat","difficulty":2 ,
"desc":"Uma maldicao grau 3 esta atacando civis. Exorcize-a.",
"xp_reward":220 ,"money_reward":180 ,"num_enemies":2 ,"rank":"Grau 3"},
{"name":"Escoltar Feiticeiro Ferido","type":"dungeon","difficulty":2 ,
"desc":"Escolte um feiticeiro ferido de volta. Cuidado com emboscadas.",
"xp_reward":280 ,"money_reward":250 ,"min_danger":5 ,"max_danger":10 ,
"karma_bonus":4 },
{"name":"Investigar Rituais Suspeitos","type":"dungeon","difficulty":2 ,
"desc":"Rituais estranhos foram avistados. Investigue.",
"xp_reward":260 ,"money_reward":220 ,"min_danger":5 ,"max_danger":10 },
{"name":"Comboio de Civis","type":"combat","difficulty":2 ,
"desc":"Escolte um grupo de civis por uma area perigosa. 3v3.",
"xp_reward":290 ,"money_reward":230 ,"num_enemies":3 ,"rank":"Grau 3",
"allow_allies":True ,"karma_bonus":4 },
{"name":"Caçar Maldicao Veloz","type":"combat","difficulty":2 ,
"desc":"Uma maldicao grau 3 muito rapida esta fugindo. Ache e exorcize.",
"xp_reward":270 ,"money_reward":200 ,"num_enemies":1 ,"rank":"Grau 3"},
{"name":"Coletar Amuletos Antigos","type":"fetch","difficulty":2 ,
"desc":"Recupere 3 amuletos antigos perdidos em ruinas.",
"xp_reward":200 ,"money_reward":250 ,"items_required":3 ,
"rare":True },
],
"Grau 2":[
{"name":"Selar Maldicao Grau 2","type":"dungeon","difficulty":3 ,
"desc":"Uma maldicao grau 2 aterroriza um bairro.",
"xp_reward":500 ,"money_reward":400 ,"min_danger":10 ,"max_danger":20 },
{"name":"Recuperar Item Roubado","type":"dungeon","difficulty":3 ,
"desc":"Uma maldicao roubou um item valioso. Recupere-o.",
"xp_reward":550 ,"money_reward":500 ,"min_danger":10 ,"max_danger":20 ,
"special_reward":"Cristal de CE"},
{"name":"Investigar Surgimento de Dedo","type":"dungeon","difficulty":3 ,
"desc":"RUMORES de um Dedo de Sukuna na area. Recupere-o antes que outra maldicao o coma. (NAO GARANTIDO)",
"xp_reward":700 ,"money_reward":600 ,"min_danger":15 ,"max_danger":25 ,
"chance_sukuna_finger":0.08 ,"karma_bonus":5 },
{"name":"Combater Grupo de Maldicoes","type":"combat","difficulty":3 ,
"desc":"Um grupo de maldicoes grau 2 esta organizado. Combate 3v3!",
"xp_reward":600 ,"money_reward":450 ,"num_enemies":3 ,"rank":"Grau 2",
"allow_allies":True },
{"name":"Defender Escola","type":"combat","difficulty":3 ,
"desc":"Maldicoes estao atacando a escola Jujutsu. Defenda-a!",
"xp_reward":650 ,"money_reward":500 ,"num_enemies":3 ,"rank":"Grau 2",
"allow_allies":True ,"karma_bonus":6 },
{"name":"Investigar Laboratorio Abandonado","type":"dungeon","difficulty":3 ,
"desc":"Experimentos com CE ocorreram aqui. Maldicoes anormais podem existir.",
"xp_reward":700 ,"money_reward":550 ,"min_danger":15 ,"max_danger":25 },
{"name":"Resgate na Floresta","type":"dungeon","difficulty":3 ,
"desc":"Um estudante desapareceu na floresta amaldicoada. Encontre-o vivo.",
"xp_reward":600 ,"money_reward":480 ,"min_danger":10 ,"max_danger":20 ,
"karma_bonus":5 },
],
"Grau 1":[
{"name":"Selar Maldicao de Grau 1","type":"dungeon","difficulty":4 ,
"desc":"Uma maldicao grau 1 ameaca uma escola. Limpe-a.",
"xp_reward":1500 ,"money_reward":1000 ,"min_danger":20 ,"max_danger":35 },
{"name":"Recuperar Dedo de Sukuna","type":"dungeon","difficulty":4 ,
"desc":"Um Dedo de Sukuna foi avistado. OUTROS FEITICEIROS ESTAO CAÇANDO. (NAO GARANTIDO)",
"xp_reward":2000 ,"money_reward":1500 ,"min_danger":20 ,"max_danger":35 ,
"chance_sukuna_finger":0.15 ,"rival_sorcerer":True ,"karma_bonus":5 },
{"name":"Combater Maldicao Especial","type":"boss","difficulty":5 ,
"desc":"Uma maldicao grau especial surgiu. SOS!",
"xp_reward":3000 ,"money_reward":2000 ,
"boss":"Hanami","karma_bonus":8 },
{"name":"Caçar Feiticeiro Renegado","type":"boss","difficulty":4 ,
"desc":"Um feiticeiro renegado esta matando civis. Capture ou elimine.",
"xp_reward":2500 ,"money_reward":1800 ,
"boss":"Naoya Zenin","karma_bonus":3 },
{"name":"Investigar Templo Amaldicoado","type":"dungeon","difficulty":4 ,
"desc":"Um templo antigo pulsa com CE negativa. Maldicoes grau 1 foram avistadas.",
"xp_reward":1800 ,"money_reward":1300 ,"min_danger":25 ,"max_danger":35 },
{"name":"Selar Maldicao Mimica","type":"dungeon","difficulty":4 ,
"desc":"Uma maldicao grau 1 que imita feiticeiros esta solta. Cuidado.",
"xp_reward":1700 ,"money_reward":1100 ,"min_danger":20 ,"max_danger":30 },
{"name":"Operacao Clandestina","type":"dungeon","difficulty":4 ,
"desc":"Infiltra-se num covil de maldicoes organizadas. Sem aliados oficiais.",
"xp_reward":2200 ,"money_reward":1800 ,"min_danger":25 ,"max_danger":35 ,
"allow_allies":False },
],
"Grau Especial":[
{"name":"Combater Mahito","type":"boss","difficulty":5 ,
"desc":"Mahito esta aterrorizando civis. Ele eh perigoso.",
"xp_reward":5000 ,"money_reward":5000 ,
"boss":"Mahito","karma_bonus":15 },
{"name":"Combater Jogo","type":"boss","difficulty":5 ,
"desc":"Jogo, maldicao do fogo, declarou guerra aos feiticeiros.",
"xp_reward":6000 ,"money_reward":6000 ,
"boss":"Jogo","karma_bonus":15 },
{"name":"Selar Geto Suguru","type":"boss","difficulty":5 ,
"desc":"Geto Suguru esta reunindo maldicoes para uma Noite de Desfile.",
"xp_reward":7000 ,"money_reward":8000 ,
"boss":"Geto Suguru","karma_bonus":20 },
{"name":"CAÇAR SUKUNA","type":"boss","difficulty":5 ,
"desc":"O REI DAS MALDICOES SE MANIFESTOU. APENAS PELA HUMANIDADE.",
"xp_reward":20000 ,"money_reward":50000 ,
"boss":"Sukuna","karma_bonus":30 ,"rare":True },
{"name":"Caçar Toji","type":"boss","difficulty":5 ,
"desc":"Toji Fushiguro, o cacador, esta na area. Cuidado.",
"xp_reward":4000 ,"money_reward":3000 ,
"boss":"Toji Fushiguro","karma_bonus":0 },
{"name":"Caçar Mahoraga Selvagem","type":"boss","difficulty":5 ,
"desc":"Um Mahoraga foi avistado sem invocador. Impossivel de domar - precisa ser destruido.",
"xp_reward":8000 ,"money_reward":6000 ,
"boss":"Mahoraga","karma_bonus":10 },
{"name":"Noite de Desfile (100 Maldicoes)","type":"combat","difficulty":5 ,
"desc":"Geto lanou a Noite de Desfile. Combata ondas de maldicoes!",
"xp_reward":8000 ,"money_reward":7000 ,"num_enemies":3 ,"rank":"Grau 1",
"allow_allies":True ,"karma_bonus":25 },
{"name":"The Final Battle \"HEITOR\"","type":"boss","difficulty":5 ,
"desc":"Ele existe. Ninguem sabe como, ninguem sabe por que. So resta uma coisa a fazer: enfrenta-lo.",
"xp_reward":1000000 ,"money_reward":500000 ,
"boss":"Heitor Careca","karma_bonus":50 ,"rare":True ,"requires_heitor_unlock":True },
],
}

STORY_MISSIONS =[
{"id":"story_1","name":"Convite para Tokyo Jujutsu High",
"type":"story","trigger_level":1 ,
"desc":"Voce foi convidado para a escola de feiticeiros.",
"reward_item":"Convite da Escola Jujutsu","reward_xp":100 ,"karma":5 },
{"id":"story_5","name":"Encontro com Gojo",
"type":"story","trigger_level":5 ,
"desc":"Satoru Gojo quer te conhecer pessoalmente.",
"reward_xp":200 ,"karma":5 ,"gojo_met":True },
{"id":"story_10","name":"Teste de Grau 2",
"type":"story","trigger_level":10 ,
"desc":"Voce sera testado para promocao a Grau 2.",
"reward_xp":500 ,"auto_promote_sub":True },
{"id":"story_15","name":"Aliados Canonical",
"type":"story","trigger_level":15 ,
"desc":"Voce agora pode escolher aliados canonicos em missoes.",
"reward_xp":800 },
{"id":"story_20","name":"Desbloqueio de Dominio Completo",
"type":"story","trigger_level":20 ,
"desc":"Voce aprendeu a expandir seu dominio completo. (Dominio Simples ja estava disponivel desde o Level 10 com Gojo.)",
"reward_xp":1000 ,"unlock_domain":True },
{"id":"story_1100_heitor","name":"Um Rumor Impossivel",
"type":"story","trigger_level":1100 ,
"desc":("Feiticeiros veteranos contam, em voz baixa, sobre um homem careca que ninguem consegue derrotar. "
"Dizem que ele domina a tecnica de Gojo E a de Sukuna ao mesmo tempo, e que se adapta a qualquer golpe "
"antes mesmo dele terminar. Voce esta forte o suficiente agora para procura-lo. "
"'THE FINAL BATTLE \"HEITOR\"' apareceu no quadro de missoes."),
"reward_xp":0 ,"heitor_unlocked":True },
]

def get_available_missions (player ):

    rank =player .rank_system .rank 
    templates =[dict (t ,rank =t .get ("rank",rank ))for t in MISSION_TEMPLATES .get (rank ,[])]

    rank_order =["Grau 4","Grau 3","Grau 2","Grau 1","Grau Especial"]
    rank_idx =rank_order .index (rank )if rank in rank_order else 0 
    for r in rank_order [:rank_idx ]:
        templates =templates +[dict (t ,rank =t .get ("rank",r ))for t in MISSION_TEMPLATES .get (r ,[])]

    if player .karma .karma <50 :
        templates =[t for t in templates if not t .get ("rare")]
    if not getattr (player ,"heitor_unlocked",False ):
        templates =[t for t in templates if not t .get ("requires_heitor_unlock")]
    return templates 

def show_mission_board (player ,ui_module ):

    from mission_generator import (generate_procedural_mission ,tick_urgent_contract ,
    get_active_questline_mission ,maybe_offer_new_questline ,QUESTLINES ,
    format_mission_label ,mission_preview_lines )

    ui_module .clear_screen ()
    ui_module .title_box ("  QUADRO DE MISSOES  ")
    ui_module .tprint (c (f"Rank atual: {player .rank_system .full_rank_name ()}",Color .DIM ))

    questline_mission =get_active_questline_mission (player )
    if questline_mission is None :
        new_qid =maybe_offer_new_questline (player )
        if new_qid :
            player .questline_progress ={"id":new_qid ,"stage":0 }
            questline_mission =get_active_questline_mission (player )
            ui_module .tprint (c (f"\n>> Nova sequencia disponivel: {QUESTLINES [new_qid ]['name']}!",
            Color .BRIGHT_MAGENTA +Color .BOLD ))

    if getattr (player ,"urgent_contract",None ):
        tick_urgent_contract (player ,ui_module )
    elif random .random ()<0.12 :
        rank =player .rank_system .rank 
        player .urgent_contract =generate_procedural_mission (player ,rank ,force_urgent =True )

    available =get_available_missions (player )

    non_rare =[m for m in available if not m .get ("rare")]
    rare =[m for m in available if m .get ("rare")]
    if random .random ()<0.20 and rare :

        available =non_rare +[random .choice (rare )]
    else :
        available =non_rare 
    if not available :
        available =non_rare +rare 

    rank =player .rank_system .rank 
    procedural_count =random .randint (2 ,3 )
    procedural_missions =[generate_procedural_mission (player ,rank )for _ in range (procedural_count )]

    random .shuffle (available )
    shown =available [:3 ]+procedural_missions 
    random .shuffle (shown )

    if questline_mission :
        shown =[questline_mission ]+shown [:4 ]
    if getattr (player ,"urgent_contract",None ):
        shown =[player .urgent_contract ]+shown 

    shown =shown [:6 ]
    if not shown :
        ui_module .tprint (c ("\nNenhuma missao disponivel.",Color .YELLOW ))
        ui_module .pause ()
        return 

    if questline_mission :
        ui_module .tprint (c (f"\n>> SEQUENCIA ATIVA: {questline_mission ['questline_name']} "
        f"(parte {questline_mission ['questline_stage']+1 }/{questline_mission ['questline_total_stages']})",
        Color .BRIGHT_MAGENTA +Color .BOLD ))
    if getattr (player ,"urgent_contract",None ):
        uc =player .urgent_contract 
        ui_module .tprint (c (f">> CONTRATO URGENTE: {uc ['name']} (expira em {uc ['urgent_expires_in']}x)",
        Color .BRIGHT_RED +Color .BOLD ))

    ui_module .tprint (c ("\nEscolha uma missao (selecione para ver detalhes completos):",Color .DIM ))

    labels =[format_mission_label (m )for m in shown ]
    labels .append ("Voltar")

    idx =ui_module .arrow_menu (labels ,title =None )
    if idx <0 or idx ==len (labels )-1 :
        return 

    selected =shown [idx ]
    accept_mission (player ,selected ,ui_module )

def accept_mission (player ,mission ,ui_module ):

    title =mission ['name']
    if mission .get ("questline_id"):
        title =f"{mission ['questline_name']} ({mission ['questline_stage']+1 }/{mission ['questline_total_stages']}) - {title }" 
    ui_module .screen_header (ui_module .ASCII_MISSION ,title ,color =Color .BRIGHT_MAGENTA )

    type_labels ={"combat":"Combate","dungeon":"Exploracao","fetch":"Busca",
    "boss":"Chefe","procedural_boss":"Chefe"}
    panel_lines =[
    f"Tipo: {type_labels .get (mission .get ('type'),mission .get ('type','?'))}",
    f"Grau: {mission .get ('rank',mission .get ('boss_rank','?'))}",
    f"Recompensa XP: +{mission ['xp_reward']}",
    f"Recompensa ienes: +{mission ['money_reward']}",
    ]
    if mission .get ("client_name"):
        panel_lines .append (f"Cliente: {mission ['client_name']} ({mission .get ('client_role','')})") 
    if mission .get ("karma_bonus"):
        panel_lines .append (f"Karma: +{mission ['karma_bonus']}")
    if mission .get ("bonus_objective"):
        bo =mission ["bonus_objective"]
        desc =bo ["desc"].format (n =bo .get ("turn_limit",6 ))
        panel_lines .append (f"Objetivo bonus: {desc } (+{int (bo .get ('bonus_xp_mult',0.5 )*100 )}% XP/$)")
    if mission .get ("urgent"):
        panel_lines .append (f"URGENTE - recompensas dobradas, expira em {mission .get ('urgent_expires_in','?')}x")

    print ()
    ui_module .section ("Detalhes da Missao",panel_lines ,color =Color .BRIGHT_YELLOW )
    print ()

    if mission .get ("story_intro"):
        ui_module .tprint (c (mission ['story_intro'],Color .BRIGHT_MAGENTA ))
        print ()

    ui_module .tprint (c (mission ['desc'],Color .BRIGHT_CYAN ))

    if not ui_module .confirm ("\nAceitar missao?"):
        return 

    if mission .get ("urgent")and getattr (player ,"urgent_contract",None )is mission :
        player .urgent_contract =None 

    player ._last_combat_turns =None 
    player ._last_combat_techniques_used =[]
    result =execute_mission (player ,mission ,ui_module )
    if result =="died":
        ui_module .tprint (c ("\nVoce morreu na missao.",Color .BRIGHT_RED ))
        ui_module .pause ()
        return 
    elif result =="failed":
        ui_module .tprint (c ("\nMissao falhou.",Color .YELLOW ))
        ui_module .pause ()
        return 
    if result =="success":
        ui_module .tprint (c ("\n!! MISSAO COMPLETA !!",Color .BRIGHT_GREEN +Color .BOLD ))
        player .missions_completed +=1 

        if mission .get ("story_outro"):
            ui_module .tprint (c (f"\n{mission ['story_outro']}",Color .BRIGHT_MAGENTA ))

        bonus_xp ,bonus_money =0 ,0 
        if mission .get ("bonus_objective"):
            from mission_generator import check_bonus_objective 
            bonus_xp ,bonus_money =check_bonus_objective (mission ,player ,player ._last_combat_turns ,ui_module )

        total_xp =mission ["xp_reward"]+bonus_xp 
        total_money =mission ["money_reward"]+bonus_money 

        leveled ,lv =player .level_system .add_xp (total_xp )
        player .money +=total_money 
        if mission .get ("karma_bonus"):
            player .karma .add_karma (mission ["karma_bonus"])
        ui_module .tprint (c (f"+{total_xp } XP",Color .BRIGHT_YELLOW ))
        ui_module .tprint (c (f"+{total_money } ienes",Color .BRIGHT_YELLOW ))
        if leveled :
            ui_module .tprint (c (f"\nLEVEL UP! +{lv } nivel(s). Level atual: {player .level_system .level }",Color .BRIGHT_YELLOW +Color .BOLD ))
            ui_module .tprint (c (f"+{5 *lv } pontos de atributo disponiveis.",Color .BRIGHT_GREEN ))
        if mission .get ("special_reward"):
            player .add_item (mission ["special_reward"])
            ui_module .tprint (c (f"+ {mission ['special_reward']}",Color .BRIGHT_GREEN ))
        if mission .get ("guaranteed_sukuna_finger"):
            player .sukuna_fingers_in_inventory +=1 
            ui_module .tprint (c ("+ Dedo de Sukuna garantido!",Color .BRIGHT_RED ))
        elif mission .get ("chance_sukuna_finger"):

            if random .random ()<mission ["chance_sukuna_finger"]:
                player .sukuna_fingers_in_inventory +=1 
                ui_module .tprint (c ("+ Dedo de Sukuna encontrado!",Color .BRIGHT_RED ))
            else :
                ui_module .tprint (c ("(O dedo nao estava la - era um falso rumor.)",Color .DIM ))

        if mission .get ("questline_id"):
            _advance_questline (player ,mission ,ui_module )

        ui_module .pause ()

def _advance_questline (player ,mission ,ui_module ):
    from mission_generator import QUESTLINES 
    qid =mission ["questline_id"]
    questline =QUESTLINES .get (qid )
    if not questline :
        return 
    next_stage =mission ["questline_stage"]+1 
    if next_stage >=len (questline ["stages"]):
        ui_module .tprint (c (f"\n!! SEQUENCIA CONCLUIDA: {questline ['name']} !!",Color .BRIGHT_YELLOW +Color .BOLD ))
        if questline .get ("final_reward_item"):
            player .add_item (questline ["final_reward_item"])
            ui_module .tprint (c (f"+ {questline ['final_reward_item']}",Color .BRIGHT_GREEN ))
        if questline .get ("final_reward_karma"):
            player .karma .add_karma (questline ["final_reward_karma"])
        player .questline_progress =None 
        player .questlines_completed =player .questlines_completed +[qid ]
    else :
        player .questline_progress ={"id":qid ,"stage":next_stage }
        ui_module .tprint (c (f"\n(Proxima parte de '{questline ['name']}' disponivel no quadro de missoes)",
        Color .DIM ))

def execute_mission (player ,mission ,ui_module ):

    mtype =mission ["type"]

    if mtype =="dungeon":

        danger =random .randint (mission .get ("min_danger",1 ),mission .get ("max_danger",10 ))
        from dungeon import Dungeon 
        dungeon =Dungeon (player ,mission =mission ,danger_level =danger ,ui_module =ui_module )
        result =dungeon .explore ()
        if result =="completed":
            return "success"
        elif result =="died":
            return "died"
        elif result =="escaped":
            ui_module .tprint (c ("\nVoce fugiu da masmorra. Missao falhou.",Color .YELLOW ))
            return "failed"
        return "success"

    elif mtype =="combat":

        from generator import generate_procedural_curse
        from combat import Combat
        from allies import get_available_allies ,get_ally 
        rank =mission .get ("rank","Grau 4")
        num =mission .get ("num_enemies",1 )
        level_mult =1.0 +player .level_system .level *0.05 
        enemies =[]
        for _ in range (num ):
            enemies .append (generate_procedural_curse (rank ,level_mult ))

        allies =[]
        if mission .get ("allow_allies"):
            available =get_available_allies (player )
            if available and random .random ()<0.6 :
                n =min (2 ,len (available ))
                chosen =random .sample (available ,n )
                allies =[get_ally (name )for name in chosen ]
                ui_module .tprint (c ("\nAliados se juntam a voce!",Color .BRIGHT_GREEN ))
                for a in allies :
                    ui_module .tprint (f"  - {a ['name']}")
                ui_module .pause ()

        combat =Combat (player ,enemies ,allies ,ui_module =ui_module )
        result =combat .start ()
        player ._last_combat_turns =combat .turn 
        player ._last_combat_techniques_used =list (combat .techniques_used_this_combat )
        if result =="victory":
            return "success"
        elif result in ("defeat","permadeath","transformed"):
            return "died"
        elif result =="fled":
            return "failed"

    elif mtype =="boss":

        from combat import Combat 
        from allies import get_available_allies ,get_ally 
        from enemies import get_boss 
        boss_name =mission ["boss"]
        boss =get_boss (boss_name )
        if not boss :
            ui_module .tprint (c ("Erro: chefe nao encontrado.",Color .RED ))
            return "failed"

        if boss_name =="Sukuna"and player .rank_system .rank !="Grau Especial":
            ui_module .tprint (c ("\nSukuna aparece.",Color .BRIGHT_RED +Color .BOLD ))
            ui_module .tprint (c ("'Voce nao tem chance. O rei das maldicoes apenas sorri.'",Color .BRIGHT_RED ))
            ui_module .tprint (c ("Sukuna te aniquila em um golpe.",Color .BRIGHT_RED +Color .BLINK ))
            player .hp =0 
            ui_module .pause ()
            return "died"

        allies =[]
        available =get_available_allies (player )
        if available :
            n =min (2 ,len (available ))
            chosen =random .sample (available ,n )
            allies =[get_ally (name )for name in chosen ]
            ui_module .tprint (c ("\nSeus aliados estao com voce para essa batalha!",Color .BRIGHT_GREEN ))
            for a in allies :
                ui_module .tprint (f"  - {a ['name']}")

        if mission .get ("rival_sorcerer"):
            ui_module .tprint (c ("\nUm outro feiticeiro apareceu para competir pelo dedo!",Color .YELLOW ))
            from generator import generate_procedural_sorcerer 
            rival =generate_procedural_sorcerer ("Grau 1",1.0 +player .level_system .level *0.05 )

            ui_module .tprint (c (f"{rival ['name']} (rival) entra na batalha!",Color .BRIGHT_MAGENTA ))

        combat =Combat (player ,[boss ]+([rival ]if mission .get ("rival_sorcerer")else []),allies ,ui_module =ui_module ,allow_flee =False )
        result =combat .start ()
        player ._last_combat_turns =combat .turn 
        player ._last_combat_techniques_used =list (combat .techniques_used_this_combat )
        if result =="victory":
            return "success"
        elif result in ("defeat","permadeath","transformed"):
            return "died"

    elif mtype =="procedural_boss":

        from generator import generate_procedural_boss 
        from combat import Combat 
        from allies import get_available_allies ,get_ally 
        boss_rank =mission .get ("boss_rank","Grau 2")
        level_mult =1.0 +player .level_system .level *0.05 
        boss =generate_procedural_boss (boss_rank ,level_mult )

        allies =[]
        available =get_available_allies (player )
        if available :
            n =min (2 ,len (available ))
            chosen =random .sample (available ,n )
            allies =[get_ally (name )for name in chosen ]
            ui_module .tprint (c ("\nSeus aliados estao com voce para essa batalha!",Color .BRIGHT_GREEN ))
            for a in allies :
                ui_module .tprint (f"  - {a ['name']}")

        combat =Combat (player ,[boss ],allies ,ui_module =ui_module )
        result =combat .start ()
        player ._last_combat_turns =combat .turn 
        player ._last_combat_techniques_used =list (combat .techniques_used_this_combat )
        if result =="victory":
            return "success"
        elif result in ("defeat","permadeath","transformed"):
            return "died"
        elif result =="fled":
            return "failed"

    elif mtype =="fetch":

        from items import roll_loot 
        ui_module .tprint (c ("\nVoce procura pelos itens...",Color .DIM ))
        for _ in range (mission .get ("items_required",3 )):
            item =roll_loot (1.0 )
            player .add_item (item )
            ui_module .tprint (c (f"  Encontrou: {item }",Color .BRIGHT_GREEN ))
        ui_module .pause ()
        return "success"

    return "failed"

def check_story_missions (player ,ui_module ):

    for sm in STORY_MISSIONS :
        if sm ["id"]in player .completed_stories :
            continue 
        if player .level_system .level >=sm ["trigger_level"]:

            trigger_story (player ,sm ,ui_module )
            player .completed_stories .add (sm ["id"])

def trigger_story (player ,story ,ui_module ):

    ui_module .clear_screen ()
    ui_module .title_box ("  EVENTO DE HISTORIA  ")
    ui_module .tprint (c (f"\n{story ['name']}",Color .BRIGHT_YELLOW +Color .BOLD ))
    ui_module .tprint (c (story ["desc"],Color .BRIGHT_CYAN ))
    ui_module .pause ()

    if story .get ("reward_item"):
        player .add_item (story ["reward_item"])
        ui_module .tprint (c (f"+ {story ['reward_item']}",Color .BRIGHT_GREEN ))
    if story .get ("reward_xp"):
        player .level_system .add_xp (story ["reward_xp"])
        ui_module .tprint (c (f"+{story ['reward_xp']} XP",Color .BRIGHT_YELLOW ))
    if story .get ("karma"):
        player .karma .add_karma (story ["karma"])
        ui_module .tprint (c (f"+{story ['karma']} karma",Color .BRIGHT_GREEN ))
    if story .get ("gojo_met"):
        player .gojo_met =True 
        ui_module .tprint (c ("Voce conheceu Gojo!",Color .BRIGHT_CYAN ))
    if story .get ("heitor_unlocked"):
        player .heitor_unlocked =True 
        ui_module .tprint (c ("\n!! THE FINAL BATTLE \"HEITOR\" disponivel no quadro de missoes !!",
        Color .BRIGHT_RED +Color .BOLD +Color .BLINK ))
    if story .get ("auto_promote_sub"):
        if player .rank_system .can_promote_sub_rank ():
            player .rank_system .promote_sub_rank ()
            ui_module .tprint (c (f"Promovido a {player .rank_system .full_rank_name ()}!",Color .BRIGHT_MAGENTA ))
    if story .get ("unlock_domain"):

        ui_module .tprint (c ("Dominio Completo desbloqueado! (Level 20+)",Color .BRIGHT_MAGENTA ))
        ui_module .tprint (c ("Dica: Se ainda nao aprendeu, treine 'Aula sobre Dominios' com Gojo para ganhar o Dominio Simples.",Color .DIM ))
    ui_module .pause ()
