
import random 

ALLIES_DB ={
"Yuji Itadori":{
"name":"Yuji Itadori",
"rank":"Grau 1",
"hp":350 ,"max_hp":350 ,
"atk":50 ,"def":18 ,"speed":22 ,"ce":200 ,"max_ce":200 ,
"technique":"Reforco Corporal + Divergent Fist",
"extensions_known":["Divergent Fist","Black Flash","Reforco Total"],
"personality":"heroico",
"desc":"Estudante de Jujutsu. Hospedeiro de Sukuna. Corpo divino.",
"dialogue":[
"Vamos la! Eu protejo meus amigos!",
"Sukuna, me de poder...",
"Eu nao vou deixar ninguem morrer!",
"Sou eu quem decide como vou morrer!",
],
"ai_type":"aggressive_tank",
"black_flash_chance":0.20 ,
"dmg_taken_mult":0.9 ,
"lives_sukuna":True ,
"available_after_rank":"Grau 4",
"available_if_karma_min":-30 ,
},
"Megumi Fushiguro":{
"name":"Megumi Fushiguro",
"rank":"Grau 1",
"hp":280 ,"max_hp":280 ,
"atk":38 ,"def":15 ,"speed":20 ,"ce":250 ,"max_ce":250 ,
"technique":"Dez Sombras",
"extensions_known":["Cachorros Divinos","Nue","Max Elefante","Mahoraga (risco)"],
"personality":"estratega",
"desc":"Herdou Dez Sombras do cla Zenin. Tatico, frio em combate.",
"dialogue":[
"Nao perca tempo. Aja.",
"Eu tenho um plano.",
"Nao eh sobre ganhar. Eh sobre nao perder.",
"Vou chamar Mahoraga... se precisar.",
],
"ai_type":"summoner_tactician",
"black_flash_chance":0.10 ,
"can_summon_mahoraga":True ,
"available_after_rank":"Grau 4",
"available_if_karma_min":-20 ,
},
"Nobara Kugisaki":{
"name":"Nobara Kugisaki",
"rank":"Grau 2",
"hp":220 ,"max_hp":220 ,
"atk":42 ,"def":12 ,"speed":19 ,"ce":180 ,"max_ce":180 ,
"technique":"Straw Doll Technique",
"extensions_known":["Pregos de CE","Martelo Kugisaki","Resonance"],
"personality":"provocadora",
"desc":"Feiticeira do interior. Marretada e direta.",
"dialogue":[
"Eu sou a mais forte daqui!",
"Vou te dar um presente... no seu cranio.",
"Eu vou viver do meu jeito.",
"Esses caras sao pateticos.",
],
"ai_type":"ranged_aggro",
"black_flash_chance":0.15 ,
"available_after_rank":"Grau 4",
"available_if_karma_min":-10 ,
},
"Maki Zenin":{
"name":"Maki Zenin",
"rank":"Grau 1",
"hp":300 ,"max_hp":300 ,
"atk":55 ,"def":20 ,"speed":24 ,"ce":0 ,"max_ce":0 ,
"technique":"Nenhuma (Restricao Celestial)",
"extensions_known":["Ataque Fisico","Arma Amaldicoada"],
"personality":"guerreira",
"desc":"Cla Zenin. Restricao Celestial parcial. Forca fisica sobre-humana.",
"dialogue":[
"Saia do meu caminho.",
"Eu nao preciso de CE.",
"Fraqueza nao eh desculpa.",
"Eu vou provar a eles.",
],
"ai_type":"physical_striker",
"heavenly_restriction":True ,
"black_flash_chance":0.25 ,
"available_after_rank":"Grau 3",
"available_if_karma_min":0 ,
},
"Toge Inumaki":{
"name":"Toge Inumaki",
"rank":"Grau 1",
"hp":250 ,"max_hp":250 ,
"atk":45 ,"def":14 ,"speed":22 ,"ce":220 ,"max_ce":220 ,
"technique":"Discurso Amaldicoado",
"extensions_known":["Pare","Sangre","Exploda","Durma","Morra"],
"personality":"silencioso",
"desc":"Cla Inumaki. Fala em ingredientes de onigiri pra nao amaldicoar.",
"dialogue":[
"Sake...",
"Bonito (ate logo).",
"Tuna (oi).",
"... (gesticula)",
],
"ai_type":"debuff_crowd_control",
"black_flash_chance":0.05 ,
"available_after_rank":"Grau 3",
"available_if_karma_min":-10 ,
},
"Panda":{
"name":"Panda",
"rank":"Grau 2",
"hp":400 ,"max_hp":400 ,
"atk":45 ,"def":25 ,"speed":15 ,"ce":150 ,"max_ce":150 ,
"technique":"Mutacao Abrupta (Gorilla Mode)",
"extensions_known":["Golpe de Panda","Gorilla Mode"],
"personality":"amigavel",
"desc":"Mutacao criada pelo Diretor Yaga. Tem 3 modos: Panda, Gorila, Triceratops.",
"dialogue":[
"Eu sou o Panda. Prazer!",
"Vamos cuidar disso juntos.",
"Gorila MODE!",
"Relax, da pra resolver.",
],
"ai_type":"tank_switcher",
"black_flash_chance":0.10 ,
"available_after_rank":"Grau 4",
"available_if_karma_min":-10 ,
},
"Kento Nanami":{
"name":"Kento Nanami",
"rank":"Grau 1",
"hp":380 ,"max_hp":380 ,
"atk":60 ,"def":22 ,"speed":20 ,"ce":280 ,"max_ce":280 ,
"technique":"Razao Proporcional (Ratio)",
"extensions_known":["Ratio: Ponto Fraco","Collapse","7:3 Critical"],
"personality":"profissional",
"desc":"Feiticeiro office-worker. Calmo, calculista, eficiente.",
"dialogue":[
"Eu sou um profissional. Vou resolver.",
"Razao 7 para 3. Ponto fraco.",
"Eu odeio horas extras.",
"Acabou. Vou pra casa.",
],
"ai_type":"precise_striker",
"black_flash_chance":0.30 ,
"weakpoint_bonus":0.50 ,
"available_after_rank":"Grau 2",
"available_if_karma_min":0 ,
},
"Aoi Todo":{
"name":"Aoi Todo",
"rank":"Grau 1",
"hp":420 ,"max_hp":420 ,
"atk":65 ,"def":24 ,"speed":23 ,"ce":250 ,"max_ce":250 ,
"technique":"Boogie Woogie",
"extensions_known":["Troca de Posicao","Combo de Troca","Soco Brutal"],
"personality":"excentrico",
"desc":"Estudante de Kyoto. Adora perguntar sobre gostos em mulheres.",
"dialogue":[
"Qual o seu tipo de mulher?",
"Boogie Woogie!",
"ISSO eh o que eu chamo de batalha!",
"Voce eh meu melhor amigo, Itadori!",
],
"ai_type":"combo_swapper",
"black_flash_chance":0.20 ,
"available_after_rank":"Grau 2",
"available_if_karma_min":0 ,
},
"Yuta Okkotsu":{
"name":"Yuta Okkotsu",
"rank":"Grau Especial",
"hp":700 ,"max_hp":700 ,
"atk":90 ,"def":35 ,"speed":25 ,"ce":800 ,"max_ce":800 ,
"technique":"Copia + Rika",
"extensions_known":["Copia de Tecnica","Rika (Esposa Amaldicoada)","RCT","Multiple CE"],
"personality":"gentil_poderoso",
"desc":"Feiticeiro de Grau Especial. Hospedeiro de Rika. Poder imenso.",
"dialogue":[
"Eu vou proteger todos.",
"Rika... me ajude.",
"Eu posso copiar tudo.",
"Nao vou perder ninguem de novo.",
],
"ai_type":"versatile_elite",
"black_flash_chance":0.15 ,
"can_rct":True ,
"available_after_rank":"Grau 1",
"available_if_karma_min":20 ,
},
"Satoru Gojo":{
"name":"Satoru Gojo",
"rank":"Grau Especial",
"hp":1500 ,"max_hp":1500 ,
"atk":200 ,"def":100 ,"speed":35 ,"ce":2000 ,"max_ce":2000 ,
"technique":"Limitless + Six Eyes",
"extensions_known":["Infinity","Blue","Red","Hollow Purple","Unlimited Void"],
"personality":"deus",
"desc":"O feiticeiro mais forte. Seis Olhos + Limitless. Dominio: Unlimited Void.",
"dialogue":[
"Voce eh fraco. Mas eu gosto de voce.",
"Vamos, tente me atingir.",
"Eu sou o mais forte. Isso eh fato.",
"Nao, nao. Ainda nao.",
],
"ai_type":"god_mode",
"black_flash_chance":0.40 ,
"dmg_taken_mult":0.0 ,
"domain":"Unlimited Void",
"available_after_rank":"Grau 1",
"available_if_karma_min":0 ,
"rare_ally":True ,
},
}

def get_ally (name ):

    data =ALLIES_DB .get (name )
    if not data :
        return None 
    ally =dict (data )
    ally ["is_ally"]=True 
    ally ["is_player"]=False 
    ally ["is_enemy"]=False 
    ally ["buffs"]=[]
    ally ["debuffs"]=[]
    ally ["bleed_stacks"]=0 
    ally ["stunned_turns"]=0 
    ally ["exhausted_turns"]=0 
    ally ["domain_used_count"]=0 
    ally ["domain_active_turns"]=0 
    ally ["lives_used"]=0 
    return ally 

def get_available_allies (player ):

    rank_order =["Grau 4","Grau 3","Grau 2","Grau 1","Grau Especial"]
    player_rank_idx =rank_order .index (player .rank_system .rank )if player .rank_system .rank in rank_order else 0 
    available =[]
    for name ,data in ALLIES_DB .items ():
        required_rank =data .get ("available_after_rank","Grau 4")
        req_idx =rank_order .index (required_rank )if required_rank in rank_order else 0 
        if player_rank_idx <req_idx :
            continue 
        if player .karma .karma <data .get ("available_if_karma_min",-100 ):
            continue 
        if data .get ("rare_ally")and not player .gojo_met :
            continue 
        available .append (name )
    return available 

def random_ally (rank_required ="Grau 4"):

    rank_order =["Grau 4","Grau 3","Grau 2","Grau 1","Grau Especial"]
    req_idx =rank_order .index (rank_required )if rank_required in rank_order else 0 
    candidates =[]
    for name ,data in ALLIES_DB .items ():
        required_rank =data .get ("available_after_rank","Grau 4")
        ally_idx =rank_order .index (required_rank )
        if ally_idx <=req_idx :
            candidates .append (name )
    if not candidates :
        return get_ally ("Yuji Itadori")
    return get_ally (random .choice (candidates ))

def as_combatant (combatant_dict ,is_player =False ,is_ally =False ,is_enemy =False ):

    c =dict (combatant_dict )
    c ["is_player"]=is_player 
    c ["is_ally"]=is_ally 
    c ["is_enemy"]=is_enemy 
    if "buffs"not in c :
        c ["buffs"]=[]
    if "debuffs"not in c :
        c ["debuffs"]=[]
    if "bleed_stacks"not in c :
        c ["bleed_stacks"]=0 
    if "stunned_turns"not in c :
        c ["stunned_turns"]=0 
    if "exhausted_turns"not in c :
        c ["exhausted_turns"]=0 
    if "domain_used_count"not in c :
        c ["domain_used_count"]=0 
    if "domain_active_turns"not in c :
        c ["domain_active_turns"]=0 
    if "max_hp"not in c :
        c ["max_hp"]=c .get ("hp",100 )
    if "max_ce"not in c :
        c ["max_ce"]=c .get ("ce",0 )
    return c 

def ally_take_turn (ally ,enemies ,player ,ui_module ):

    msgs =[]
    alive_enemies =[e for e in enemies if e ["hp"]>0 ]
    if not alive_enemies :
        return msgs 

    if ally .get ("stunned_turns",0 )>0 :
        ally ["stunned_turns"]-=1 
        msgs .append (f"{ally ['name']} esta imovel.")
        return msgs 

    target =min (alive_enemies ,key =lambda e :e ["hp"])

    ai_type =ally .get ("ai_type","aggressive")

    if ai_type =="aggressive_tank":

        dmg =int (ally ["atk"]*1.2 )
        target ["hp"]-=dmg 
        msgs .append (f"{ally ['name']} golpeia {target ['name']} ({dmg } dano).")

        if random .random ()<ally .get ("black_flash_chance",0.1 ):
            bf_dmg =int (dmg *2.5 )
            target ["hp"]-=bf_dmg 
            msgs .append (f"!! BLACK FLASH do {ally ['name']}! +{bf_dmg } dano.")

    elif ai_type =="summoner_tactician":

        if random .random ()<0.5 and ally ["ce"]>=30 :
            ally ["ce"]-=30 
            dmg =int (ally ["atk"]*1.5 )
            target ["hp"]-=dmg 
            msgs .append (f"{ally ['name']} invoca Cachorros Divinos contra {target ['name']} ({dmg } dano).")
        else :
            dmg =int (ally ["atk"]*0.8 )
            target ["hp"]-=dmg 
            msgs .append (f"{ally ['name']} ataca {target ['name']} ({dmg } dano).")

    elif ai_type =="ranged_aggro":

        dmg =int (ally ["atk"]*1.3 )
        target ["hp"]-=dmg 
        msgs .append (f"{ally ['name']} arremessa pregos em {target ['name']} ({dmg } dano).")
        if random .random ()<0.3 and ally ["ce"]>=40 :
            ally ["ce"]-=40 
            extra =int (ally ["atk"]*2.0 )
            target ["hp"]-=extra 
            msgs .append (f"{ally ['name']} usa Resonance! +{extra } dano.")

    elif ai_type =="physical_striker":

        dmg =int (ally ["atk"]*1.5 )
        target ["hp"]-=dmg 
        msgs .append (f"{ally ['name']} golpeia com forca brutal {target ['name']} ({dmg } dano).")
        if random .random ()<ally .get ("black_flash_chance",0.2 ):
            bf_dmg =int (dmg *2.5 )
            target ["hp"]-=bf_dmg 
            msgs .append (f"!! BLACK FLASH de Maki! +{bf_dmg } dano.")

    elif ai_type =="debuff_crowd_control":

        if random .random ()<0.4 and ally ["ce"]>=20 :
            ally ["ce"]-=20 
            target ["stunned_turns"]=target .get ("stunned_turns",0 )+1 
            msgs .append (f"{ally ['name']} sussurra 'Pare!' - {target ['name']} congela!")
        elif random .random ()<0.2 and ally ["ce"]>=40 :
            ally ["ce"]-=40 
            dmg =int (ally ["atk"]*2.5 )
            target ["hp"]-=dmg 
            msgs .append (f"{ally ['name']} grita 'Exploda!' - {target ['name']} toma {dmg } dano!")
        else :
            dmg =int (ally ["atk"]*0.5 )
            target ["hp"]-=dmg 
            msgs .append (f"{ally ['name']} golpeia {target ['name']} ({dmg } dano).")

    elif ai_type =="tank_switcher":

        if random .random ()<0.3 :
            ally ["atk"]=int (ally ["atk"]*1.4 )
            dmg =int (ally ["atk"]*1.2 )
            target ["hp"]-=dmg 
            ally ["atk"]=int (ally ["atk"]/1.4 )
            msgs .append (f"{ally ['name']} ativa GORILLA MODE! Golpe devastador ({dmg } dano).")
        else :
            dmg =int (ally ["atk"]*0.9 )
            target ["hp"]-=dmg 
            msgs .append (f"{ally ['name']} golpeia {target ['name']} ({dmg } dano).")

    elif ai_type =="precise_striker":

        dmg =int (ally ["atk"]*1.0 )
        crit_chance =0.5 +ally .get ("weakpoint_bonus",0 )
        if random .random ()<crit_chance :
            dmg =int (dmg *2.0 )
            msgs .append (f"{ally ['name']} encontra o PONTO FRACO! ({dmg } dano CRITICO!)")
        else :
            msgs .append (f"{ally ['name']} golpeia {target ['name']} ({dmg } dano).")
        target ["hp"]-=dmg 
        if random .random ()<ally .get ("black_flash_chance",0.3 ):
            bf_dmg =int (dmg *2.5 )
            target ["hp"]-=bf_dmg 
            msgs .append (f"!! BLACK FLASH de Nanami! +{bf_dmg } dano.")

    elif ai_type =="combo_swapper":

        if random .random ()<0.4 and len (alive_enemies )>1 :
            other =random .choice ([e for e in alive_enemies if e !=target ])
            target ["hp"],other ["hp"]=other ["hp"],target ["hp"]
            msgs .append (f"{ally ['name']} aplaude: Boogie Woogie! Posicoes trocadas!")
        dmg =int (ally ["atk"]*1.3 )
        target ["hp"]-=dmg 
        msgs .append (f"{ally ['name']} da um soco brutal em {target ['name']} ({dmg } dano).")

    elif ai_type =="versatile_elite":

        if ally ["ce"]>=100 and random .random ()<0.3 :
            ally ["ce"]-=100 

            for e in alive_enemies [:3 ]:
                dmg =int (ally ["atk"]*1.2 )
                e ["hp"]-=dmg 
                msgs .append (f"{ally ['name']} ataca {e ['name']} ({dmg } dano).")
        elif ally .get ("can_rct")and ally ["hp"]<ally ["max_hp"]*0.4 and ally ["ce"]>=80 :
            ally ["ce"]-=80 
            heal =int (ally ["max_hp"]*0.3 )
            ally ["hp"]=min (ally ["max_hp"],ally ["hp"]+heal )
            msgs .append (f"{ally ['name']} usa RCT e cura {heal } HP!")
        else :
            dmg =int (ally ["atk"]*1.5 )
            target ["hp"]-=dmg 
            msgs .append (f"{ally ['name']} invoca Rika! ({dmg } dano a {target ['name']}).")

    elif ai_type =="god_mode":

        if random .random ()<0.3 and ally ["ce"]>=200 :
            ally ["ce"]-=200 
            dmg =int (ally ["atk"]*3.0 )
            for e in alive_enemies :
                e ["hp"]-=dmg 
            msgs .append (f"{ally ['name']} usa RED! Explosao massiva ({dmg } em todos).")
        elif random .random ()<0.5 and ally ["ce"]>=100 :
            ally ["ce"]-=100 
            dmg =int (ally ["atk"]*2.0 )
            target ["hp"]-=dmg 
            msgs .append (f"{ally ['name']} usa BLUE! {target ['name']} esmagado ({dmg } dano).")
        else :
            dmg =int (ally ["atk"]*1.5 )
            target ["hp"]-=dmg 
            msgs .append (f"{ally ['name']} golpeia casualmente {target ['name']} ({dmg } dano).")

    elif ai_type =="rika_random":

        rika_moves =[
        {"name":"Braco Espectral","mult":1.4 ,"line":"Rika esmaga {t} com um braco espectral"},
        {"name":"Garra Amaldicoada","mult":1.1 ,"line":"Rika rasga {t} com garras espectrais"},
        {"name":"Investida Colossal","mult":1.7 ,"line":"Rika avanca e atropela {t}"},
        {"name":"Grito Amaldicoado","mult":0.9 ,"line":"Rika solta um grito que sacode {t}"},
        ]
        move =random .choice (rika_moves )
        dmg =int (ally ["atk"]*move ["mult"])
        target ["hp"]-=dmg 
        msgs .append (f"{move ['line'].format (t =target ['name'])} ({dmg } dano).")
        if random .random ()<ally .get ("black_flash_chance",0.1 ):
            bf_dmg =int (dmg *2.5 )
            target ["hp"]-=bf_dmg 
            msgs .append (f"!! BLACK FLASH de Rika! +{bf_dmg } dano.")

    else :
        dmg =int (ally ["atk"]*1.0 )
        target ["hp"]-=dmg 
        msgs .append (f"{ally ['name']} ataca {target ['name']} ({dmg } dano).")

    ally ["ce"]=min (ally .get ("max_ce",0 ),ally .get ("ce",0 )+10 )

    return msgs
