import random 

ITEM_TYPES ={
"consumivel":"Consumivel",
"arma":"Arma Amaldicoada",
"amuleto":"Amuleto",
"recurso":"Recurso",
"especial":"Especial",
"amaldicoado":"Objeto Amaldicoado",
}

ITEMS_DB ={
"Selo de CE Basico":{
"type":"consumivel","price":60 ,"rarity":"comum",
"desc":"Restaura 35 de Energia Amaldicoada.",
"effect":{"ce_restore":35 },
},
"Selo de CE Avancado":{
"type":"consumivel","price":180 ,"rarity":"incomum",
"desc":"Restaura 85 de Energia Amaldicoada.",
"effect":{"ce_restore":85 },
},
"Selo de CE MAX":{
"type":"consumivel","price":500 ,"rarity":"raro",
"desc":"Restaura toda a Energia Amaldicoada.",
"effect":{"ce_restore_full":True },
},
"Selo de Cura":{
"type":"consumivel","price":90 ,"rarity":"comum",
"desc":"Restaura 55 HP.",
"effect":{"hp_restore":55 },
},
"Selo de Cura Avancado":{
"type":"consumivel","price":240 ,"rarity":"incomum",
"desc":"Restaura 155 HP.",
"effect":{"hp_restore":155 },
},
"Selo de Cura MAX":{
"type":"consumivel","price":650 ,"rarity":"raro",
"desc":"Restaura todo HP.",
"effect":{"hp_restore_full":True },
},
"Pedra de Vida":{
"type":"consumivel","price":1200 ,"rarity":"epico",
"desc":"Revive com 50% HP se morrer na proxima batalha.",
"effect":{"revive_pct":0.50 },
},
"Selo de Forca":{
"type":"consumivel","price":300 ,"rarity":"incomum",
"desc":"+40% de dano em golpes fisicos/tecnicas na proxima batalha.",
"effect":{"dmg_buff_next_battle":0.40 },
},
"Pergaminho de Fuga":{
"type":"consumivel","price":120 ,"rarity":"comum",
"desc":"Fuga garantida de batalha.",
"effect":{"guaranteed_flee":True },
},
"Fralda Abencoada":{
"type":"consumivel","price":800 ,"rarity":"epico",
"desc":"Remove 1 Dedo de Sukuna do estomago com seguranca.",
"effect":{"remove_sukuna_finger":True },
},

"Inverted Spear of Heaven":{
"type":"arma","price":0 ,"rarity":"lendario",
"desc":("Arma amaldicoada que anula tecnicas. Atravessa o Infinito de Gojo. "
"+65% velocidade, +45% chance de critico."),
"effect":{
"str_bonus":35 ,"dmg_bonus":70 ,
"speed_bonus_pct":0.65 ,"crit_bonus":0.45 ,
"infinity_bypass":True ,"technique_nullify":True ,
},
},
"Playful Cloud":{
"type":"arma","price":3500 ,"rarity":"lendario",
"desc":("Bastao amaldicoado. A cada 5 de forca efetiva, "
"ganha +2% de forca ao usar (alem do bonus base)."),
"effect":{
"str_bonus":30 ,"dmg_bonus":50 ,
"dynamic_str_pct_per_5":0.02 ,
},
},
"Split Soul Katana":{
"type":"arma","price":2500 ,"rarity":"lendario",
"desc":("Katana que corta a alma. +status, regenera 15 CE por turno, "
"ignora 60% da defesa inimiga."),
"effect":{
"str_bonus":28 ,"dmg_bonus":45 ,
"ce_regen":15 ,"armor_pierce_pct":0.60 ,
"soul_attack":True ,
},
},
"Black Rope":{
"type":"arma","price":1800 ,"rarity":"epico",
"desc":"Corda amaldicoada. Tem 25% de chance de atordoar por 2 turnos.",
"effect":{
"str_bonus":18 ,"dmg_bonus":30 ,
"stun_chance":0.25 ,"stun_turns":2 ,
},
},
"Dragon Bone":{
"type":"arma","price":2200 ,"rarity":"epico",
"desc":("Osso de dragao amaldicoado. Acumula dano recebido por 4 turnos "
"e libera multiplicado por 2.5x aos inimigos."),
"effect":{
"str_bonus":22 ,"dmg_bonus":35 ,
"damage_accumulator":True ,"accumulator_turns":4 ,"accumulator_mult":2.5 ,
},
},
"Slaughter Demon":{
"type":"arma","price":1500 ,"rarity":"epico",
"desc":"Lamina simples porem amaldicoada. Bom status bruto.",
"effect":{
"str_bonus":20 ,"dmg_bonus":30 ,
},
},
"Katana Amaldicoada Comum":{
"type":"arma","price":600 ,"rarity":"raro",
"desc":"Katana imbuída com CE. Corte que sangra.",
"effect":{"str_bonus":12 ,"dmg_bonus":18 ,"bleed_chance":0.20 },
},
"Punho de Ferro":{
"type":"arma","price":250 ,"rarity":"incomum",
"desc":"Soco ingles amaldicoado. +8 de forca.",
"effect":{"str_bonus":8 ,"dmg_bonus":5 },
},

"Pingente de Sorte":{
"type":"amuleto","price":320 ,"rarity":"raro",
"desc":"+12 de sorte.",
"effect":{"luck_bonus":12 },
},
"Pingente de Forca":{
"type":"amuleto","price":350 ,"rarity":"raro",
"desc":"+8 de forca.",
"effect":{"str_bonus":8 },
},
"Pingente de Vigor":{
"type":"amuleto","price":380 ,"rarity":"raro",
"desc":"+50 HP maximo e +3 de vigor.",
"effect":{"hp_bonus":50 ,"vigor_bonus":3 },
},
"Essencia de Alma do Yuji":{
"type":"amuleto","price":1500 ,"rarity":"lendario",
"desc":"+5% de chance de acertar Black Flash.",
"effect":{"black_flash_bonus":0.05 },
},
"Camada de Protecao Reforcada de CE":{
"type":"amuleto","price":700 ,"rarity":"epico",
"desc":"+15 de defesa.",
"effect":{"def_bonus":15 },
},
"Bandana do Gojo":{
"type":"amuleto","price":1800 ,"rarity":"lendario",
"desc":"+10% de HP maximo enquanto equipado.",
"effect":{"hp_max_pct_bonus":0.10 },
},
"Talisma de Gojo":{
"type":"amuleto","price":1500 ,"rarity":"lendario",
"desc":"Reflete 30% do dano de tecnicas inimigas.",
"effect":{"reflect_pct":0.30 },
},
"Olho de Maldicao":{
"type":"amuleto","price":700 ,"rarity":"epico",
"desc":"Permite ver HP exato de maldicoes.",
"effect":{"see_enemy_hp":True },
},
"Amuleto do Vazio":{
"type":"amuleto","price":800 ,"rarity":"epico",
"desc":"Gera 5 de CE por turno.",
"effect":{"ce_regen":5 },
},
"Cristal de CE Amaldicoado":{
"type":"amuleto","price":600 ,"rarity":"epico",
"desc":"Reduz dano amaldicoado em 15%.",
"effect":{"ce_dmg_reduce":0.15 },
},

"Prego Comum":{
"type":"recurso","price":15 ,"rarity":"comum",
"desc":"Prego de ferro. Material para Straw Doll.",
"effect":{},
},
"Osso de Maldicao":{
"type":"recurso","price":65 ,"rarity":"incomum",
"desc":"Osso de maldicao morta. Material de crafting.",
"effect":{},
},
"Cristal de CE":{
"type":"recurso","price":160 ,"rarity":"raro",
"desc":"Cristal puro de energia amaldicoada.",
"effect":{},
},
"Sangue Amaldicoado":{
"type":"recurso","price":140 ,"rarity":"raro",
"desc":"Sangue puro de maldicao grau 1.",
"effect":{},
},
"Papel Talisma":{
"type":"recurso","price":35 ,"rarity":"comum",
"desc":"Papel usado em selos e barreiras.",
"effect":{},
},

"Dedo de Sukuna":{
"type":"especial","price":0 ,"rarity":"lendario",
"desc":("Um dos 20 dedos do Rei das Maldicoes. Ingerir da poder imenso, "
"mas pode matar instantaneamente, transformar em maldicao, "
"ou desencadear Sukuna."),
"effect":{"sukuna_finger":True },
},
"Coracao de Maldicao Especial":{
"type":"especial","price":0 ,"rarity":"lendario",
"desc":"Coracao de uma maldicao grau especial. Item de missao.",
"effect":{},
},
"Selo de Aprisionamento":{
"type":"especial","price":0 ,"rarity":"epico",
"desc":"Selo que aprisiona maldicoes vivas.",
"effect":{},
},
"Convite da Escola Jujutsu":{
"type":"especial","price":0 ,"rarity":"epico",
"desc":"Convite oficial para a Tokyo Jujutsu High.",
"effect":{},
},
"Parte do Alvo":{
"type":"especial","price":0 ,"rarity":"raro",
"desc":"Parte do corpo de uma maldicao. Necessaria para usar Resonance (Straw Doll).",
"effect":{},
},

"Caixa Amaldicoada":{
"type":"amaldicoado","price":0 ,"rarity":"raro",
"desc":"Caixa que pode conter itens OU uma maldicao.",
"effect":{"random_curse_or_item":True },
},
"Selo de Status":{
"type":"amaldicoado","price":0 ,"rarity":"epico",
"desc":"Concede 3 a 5 pontos de status aleatorios em atributos diversos.",
"effect":{"random_status_points":True },
},
"Anel do Caos":{
"type":"amaldicoado","price":0 ,"rarity":"lendario",
"desc":"Invoca um chefe canonico aleatorio para voce lutar.",
"effect":{"summon_random_canon_boss":True },
},
"Espelho de Rika":{
"type":"amaldicoado","price":0 ,"rarity":"epico",
"desc":"Espelho que mostra o futuro sombrio do usuario. Dano mental.",
"effect":{"mental_damage":True },
},
"Anel de Sukuna":{
"type":"amaldicoado","price":0 ,"rarity":"lendario",
"desc":"Anel amaldicoado por Sukuna. Poder mas perda de controle.",
"effect":{"possession_risk":True },
},
"Olho Roubado de Mahoraga":{
"type":"amuleto","price":0 ,"rarity":"lendario",
"desc":"Um fragmento arrancado do corpo de Mahoraga por Sukuna, ainda pulsando com CE adaptativo. "
"+40 de velocidade e +35 de defesa enquanto equipado.",
"effect":{"speed_bonus":40 ,"def_bonus":35 },
},
"Kamutoke":{
"type":"amuleto","price":0 ,"rarity":"lendario",
"desc":"Uma das duas ferramentas amaldicoadas originais de Sukuna, em forma de vajra. Capaz de invocar "
"torrentes de raios do ceu. +60 de forca enquanto equipado.",
"effect":{"str_bonus":60 },
},
"Hiten":{
"type":"amuleto","price":0 ,"rarity":"lendario",
"desc":"O triadente amaldicoado de Sukuna, ligado a sua Chama Divina. Uma das duas ferramentas que ele "
"carregava na era Heian. +55 de velocidade e +30 de defesa enquanto equipado.",
"effect":{"speed_bonus":55 ,"def_bonus":30 },
},
}

RARITY_COLORS ={
"comum":"WHITE",
"incomum":"GREEN",
"raro":"BLUE",
"epico":"MAGENTA",
"lendario":"YELLOW",
}

RARITY_GRAU ={
"comum":"Grau 4",
"incomum":"Grau 3",
"raro":"Grau 2",
"epico":"Grau 1",
"lendario":"Grau Especial",
}

RARITY_WEIGHTS ={
"comum":50 ,
"incomum":25 ,
"raro":15 ,
"epico":7 ,
"lendario":3 ,
}

SHOP_CATEGORIES =[
("Consumiveis","consumivel"),
("Armas","arma"),
("Amuletos","amuleto"),
("Recursos","recurso"),
]

def get_item (name ):
    return ITEMS_DB .get (name )

def get_items_by_type (type_name ):
    return {name :data for name ,data in ITEMS_DB .items ()if data ["type"]==type_name }

def get_shop_items ():
    shop_names =[]
    for _ ,type_name in SHOP_CATEGORIES :
        for name ,data in ITEMS_DB .items ():
            if data ["type"]==type_name and data .get ("price",0 )>0 :
                shop_names .append (name )
    return {name :ITEMS_DB [name ]for name in shop_names if name in ITEMS_DB }

def get_shop_items_by_category ():
    cats ={}
    for label ,type_name in SHOP_CATEGORIES :
        cats [label ]={name :data for name ,data in ITEMS_DB .items ()
        if data ["type"]==type_name and data .get ("price",0 )>0 }
    return cats 

def roll_loot (difficulty_mult =1.0 ,special =False ):
    roll =random .random ()*difficulty_mult
    if special and random .random ()<0.01 :
        return "Dedo de Sukuna"

    EXCLUDED_FROM_LOOT ={
    "Dedo de Sukuna",
    "Coracao de Maldicao Especial",
    "Selo de Aprisionamento",
    "Convite da Escola Jujutsu",
    "Inverted Spear of Heaven",
    "Caixa Amaldicoada",
    "Selo de Status",
    "Anel do Caos",
    "Espelho de Rika",
    "Anel de Sukuna",
    }
    items_by_rarity ={r :[]for r in RARITY_WEIGHTS}
    for name ,data in ITEMS_DB .items ():
        if name in EXCLUDED_FROM_LOOT :
            continue
        if data .get ("price",0 )==0 :
            continue
        items_by_rarity [data ["rarity"]].append (name )

    if roll >0.95 :
        rarity ="lendario"
    elif roll >0.85 :
        rarity ="epico"
    elif roll >0.65 :
        rarity ="raro"
    elif roll >0.35 :
        rarity ="incomum"
    else :
        rarity ="comum"

    pool =items_by_rarity .get (rarity ,items_by_rarity ["comum"])
    if not pool :
        pool =items_by_rarity ["comum"]
    return random .choice (pool )

def roll_chest_loot (cursed_chest =False ):
    if cursed_chest :
        if random .random ()<0.30 :
            return ("trap",None )
        rarity ="raro"if random .random ()<0.4 else "epico"
        pool =[n for n ,d in ITEMS_DB .items ()if d ["rarity"]==rarity and d ["price"]>0 ]
        if pool :
            return ("item",random .choice (pool ))
        return ("item","Cristal de CE")
    else :
        rarity ="comum"if random .random ()<0.5 else "incomum"
        pool =[n for n ,d in ITEMS_DB .items ()if d ["rarity"]==rarity and d ["price"]>0 ]
        if pool :
            return ("item",random .choice (pool ))
        return ("item","Selo de CE Basico")

def get_rarity_color (rarity ):
    return RARITY_COLORS .get (rarity ,"WHITE")

def get_rarity_grau (rarity ):
    return RARITY_GRAU .get (rarity ,"Grau 4")

def get_item_info_string (item_name ):
    item =ITEMS_DB .get (item_name )
    if not item :
        return f"{item_name } (desconhecido)"

    rarity =item .get ("rarity","comum")
    grau =get_rarity_grau (rarity )
    itype =item .get ("type","?")
    price =item .get ("price",0 )
    desc =item .get ("desc","")
    eff =item .get ("effect",{})

    lines =[f"{item_name }"]
    price_str =str (price )if price >0 else "nao vendivel"
    lines .append (f"  Tipo: {itype } | Raridade: {rarity } ({grau }) | Preco: {price_str } ienes")
    lines .append (f"  Descricao: {desc }")

    if eff :
        effect_descs =[]
        for k ,v in eff .items ():
            if k =="hp_restore":
                effect_descs .append (f"Restaura {v } HP")
            elif k =="hp_restore_full":
                effect_descs .append ("Restaura TODO HP")
            elif k =="ce_restore":
                effect_descs .append (f"Restaura {v } CE")
            elif k =="ce_restore_full":
                effect_descs .append ("Restaura TODA CE")
            elif k =="revive_pct":
                effect_descs .append (f"Revive com {int (v *100 )}% HP se morrer em batalha")
            elif k =="guaranteed_flee":
                effect_descs .append ("Fuga garantida de batalha")
            elif k =="dmg_buff_next_battle":
                effect_descs .append (f"+{int (v *100 )}% dano na proxima batalha")
            elif k =="remove_sukuna_finger":
                effect_descs .append ("Remove 1 Dedo de Sukuna ingerido com seguranca")
            elif k =="sukuna_finger":
                effect_descs .append ("!! Dedo de Sukuna - comer pode dar poder ou matar !!")
            elif k =="random_status_points":
                effect_descs .append ("Concede 3 a 5 pontos de status aleatorios")
            elif k =="summon_random_canon_boss":
                effect_descs .append ("Invoca um chefe canonico aleatorio")
            elif k =="str_bonus":
                effect_descs .append (f"+{v } Forca quando equipado")
            elif k =="def_bonus":
                effect_descs .append (f"+{v } Defesa quando equipado")
            elif k =="hp_bonus":
                effect_descs .append (f"+{v } HP maximo quando equipado")
            elif k =="vigor_bonus":
                effect_descs .append (f"+{v } Vigor quando equipado")
            elif k =="luck_bonus":
                effect_descs .append (f"+{v } Sorte quando equipado")
            elif k =="dmg_bonus":
                effect_descs .append (f"+{v } dano quando equipado")
            elif k =="crit_bonus":
                effect_descs .append (f"+{int (v *100 )}% chance critica quando equipado")
            elif k =="bleed_chance":
                effect_descs .append (f"{int (v *100 )}% chance de sangramento quando equipado")
            elif k =="lifesteal_pct":
                effect_descs .append (f"{int (v *100 )}% lifesteal quando equipado")
            elif k =="weakpoint_bonus":
                effect_descs .append (f"+{int (v *100 )}% dano em pontos fracos quando equipado")
            elif k =="bonus_vs_curse":
                effect_descs .append (f"+{int (v *100 )}% dano vs maldicoes quando equipado")
            elif k =="ce_dmg_reduce":
                effect_descs .append (f"-{int (v *100 )}% dano amaldicoado recebido")
            elif k =="ce_regen":
                effect_descs .append (f"+{v } CE por turno")
            elif k =="reflect_pct":
                effect_descs .append (f"Reflete {int (v *100 )}% do dano recebido")
            elif k =="see_enemy_hp":
                effect_descs .append ("Mostra HP exato dos inimigos")
            elif k =="ranged":
                effect_descs .append ("Arma de longo alcance")
            elif k =="technique_synergy":
                effect_descs .append (f"Sinergia com tecnica: {v }")
            elif k =="armor_pierce":
                effect_descs .append ("Ignora defesa do alvo")
            elif k =="armor_pierce_pct":
                effect_descs .append (f"Ignora {int (v *100 )}% da defesa do alvo")
            elif k =="speed_bonus":
                effect_descs .append (f"+{v } Velocidade quando equipado")
            elif k =="speed_bonus_pct":
                effect_descs .append (f"+{int (v *100 )}% Velocidade quando equipado")
            elif k =="infinity_bypass":
                effect_descs .append ("Atravessa o Infinito (Gojo)")
            elif k =="technique_nullify":
                effect_descs .append ("Anula tecnicas do alvo atingido")
            elif k =="dynamic_str_pct_per_5":
                effect_descs .append (f"+{int (v *100 )}% de forca a cada 5 de forca efetiva")
            elif k =="stun_chance":
                effect_descs .append (f"{int (v *100 )}% chance de atordoar")
            elif k =="stun_turns":
                effect_descs .append (f"Atordoa por {v } turnos")
            elif k =="damage_accumulator":
                effect_descs .append ("Acumula dano recebido por 4 turnos")
            elif k =="accumulator_turns":
                effect_descs .append (f"Duracao do acumulo: {v } turnos")
            elif k =="accumulator_mult":
                effect_descs .append (f"Libera dano multiplicado por {v }x")
            elif k =="soul_attack":
                effect_descs .append ("Ataca a alma (ignora defesa fisica)")
            elif k =="black_flash_bonus":
                effect_descs .append (f"+{int (v *100 )}% chance de Black Flash")
            elif k =="hp_max_pct_bonus":
                effect_descs .append (f"+{int (v *100 )}% HP maximo")
            elif k =="karma_penalty":
                effect_descs .append (f"-{v } karma por uso (item amaldicoado)")
            elif k =="mental_damage":
                effect_descs .append ("Causa dano mental ao usuario")
            elif k =="possession_risk":
                effect_descs .append ("Risco de possessao de Sukuna")
            elif k =="random_curse_or_item":
                effect_descs .append ("Contem item aleatorio ou maldicao")
        if effect_descs :
            lines .append ("  Efeitos:")
            for ed in effect_descs :
                lines .append (f"    - {ed }")

    return "\n".join (lines )

def roll_enemy_drop (enemy_rank ,has_luck =0 ,difficulty_mult =1.0 ):
    luck_mult =(1.0 +(has_luck *0.01 ))*max (0.1 ,difficulty_mult )
    rank_mult ={
    "Grau 4":0.5 ,
    "Grau 3":0.8 ,
    "Grau 2":1.0 ,
    "Grau 1":1.5 ,
    "Grau Especial":3.0 ,
    }.get (enemy_rank ,1.0 )*luck_mult 

    items =[]
    n_items =random .randint (1 ,3 )
    for _ in range (n_items ):
        if random .random ()<0.7 :
            items .append (roll_loot (rank_mult ))

    if random .random ()<0.4 *rank_mult :
        items .append (random .choice (["Osso de Maldicao","Cristal de CE","Sangue Amaldicoado"]))

    if enemy_rank =="Grau Especial"and random .random ()<0.02 *luck_mult :
        items .append ("Dedo de Sukuna")

    if random .random ()<0.10 *rank_mult :
        items .append ("Parte do Alvo")

    return items
