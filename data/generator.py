
import random 
import sys 
import os 

sys .path .insert (0 ,os .path .dirname (os .path .abspath (__file__ )))

from enemies import CURSE_TEMPLATES ,RANK_ORDER
from techniques import INNATE_TECHNIQUES ,BIRTH_TRAITS

CURSE_NOUNS =["Abissal","Antigo","Conceitual","Caotico","Distorcido",
"Eterno","Fetido","Gelado","Hipnotico","Imortal",
"Jovem","Letal","Mutante","Noturno","Oculto",
"Profano","Quimico","Sombrio","Torcido","Vingativo",
"Vermelho","Amarelo","Purpureo","Espectral","Infernal"]

CURSE_TYPES =["Sombra","Viscera","Esporo","Espelho","Cobra",
"Aranha","Mascara","Pulcao","Tumor","Vortice",
"Lamina","Cristal","Olho","Boca","Mao",
"Craneo","Coracao","Veia","Osso","Sangue"]

HUMAN_NAMES =["Akira","Botan","Chika","Daichi","Eiji","Fumiko",
"Goro","Hanae","Ietsugu","Junko","Kaoru","Leiko",
"Masahiro","Naoko","Osamu","Pen","Ryo","Saburo",
"Toshiro","Umeko","Wataru","Yukio","Zenjiro"]
SURNAMES =["Abe","Bando","Chiba","Doi","Endo","Fujita","Goto",
"Hara","Inoue","Jinbo","Kato","Lida","Mori","Nakamura",
"Ogata","Pon","Rei","Sato","Tani","Ueda","Wada","Yamada","Zenin"]

def generate_curse_name ():
    return f"Maldicao {random .choice (CURSE_NOUNS )} de {random .choice (CURSE_TYPES )}"

def generate_curse_name_and_type ():
    curse_type =random .choice (CURSE_TYPES )
    return f"Maldicao {random .choice (CURSE_NOUNS )} de {curse_type }",curse_type

def generate_sorcerer_name ():
    return f"{random .choice (SURNAMES )} {random .choice (HUMAN_NAMES )}"

CURSE_ABILITIES =[

{"name":"Garra Cortante","dmg_mult":1.2 ,"effect":"bleed","effect_value":2 ,"effect_chance":0.5 ,
"min_rank_idx":0 ,"desc":"Garras afiadas que causam sangramento"},
{"name":"Mordida Viciosa","dmg_mult":1.0 ,"effect":"bleed","effect_value":3 ,"effect_chance":0.7 ,
"min_rank_idx":0 ,"desc":"Mordida que sangra continuamente"},
{"name":"Investida Brutal","dmg_mult":1.5 ,"effect":None ,"effect_chance":0.0 ,
"min_rank_idx":0 ,"desc":"Investida fisica poderosa"},
{"name":"Bolha Toxica","dmg_mult":0.8 ,"effect":"poison","effect_value":3 ,"effect_chance":0.8 ,
"min_rank_idx":1 ,"desc":"Bolha que envenena o alvo"},
{"name":"Toque Paralisante","dmg_mult":0.7 ,"effect":"stun","effect_value":1 ,"effect_chance":0.4 ,
"min_rank_idx":1 ,"desc":"Toque que pode atordoar"},

{"name":"Lamina Sombria","dmg_mult":1.8 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.6 ,
"min_rank_idx":2 ,"desc":"Lamina de sombra que corta fundo"},
{"name":"Olho Amaldicoante","dmg_mult":1.3 ,"effect":"stun","effect_value":2 ,"effect_chance":0.5 ,
"min_rank_idx":2 ,"desc":"Olhar que paraliza"},
{"name":"Explosao de CE","dmg_mult":2.0 ,"effect":"burn","effect_value":3 ,"effect_chance":0.4 ,
"min_rank_idx":2 ,"desc":"Explosao de energia amaldicoada"},
{"name":"Dreno Vital","dmg_mult":1.4 ,"effect":"lifesteal","effect_value":0.3 ,"effect_chance":1.0 ,
"min_rank_idx":2 ,"desc":"Drena vida do alvo"},
{"name":"Garra Venenosa","dmg_mult":1.2 ,"effect":"poison","effect_value":5 ,"effect_chance":0.7 ,
"min_rank_idx":2 ,"desc":"Garras embebidas em veneno"},

{"name":"Corte Dimensional","dmg_mult":2.5 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.7 ,
"min_rank_idx":3 ,"desc":"Corte que distorce o espaco"},
{"name":"Visao Petrificante","dmg_mult":1.0 ,"effect":"stun","effect_value":3 ,"effect_chance":0.5 ,
"min_rank_idx":3 ,"desc":"Olhar que petrifica"},
{"name":"Inferno CE","dmg_mult":2.2 ,"effect":"burn","effect_value":5 ,"effect_chance":0.6 ,
"min_rank_idx":3 ,"desc":"Mar de chamas amaldicoadas"},
{"name":"Vampirismo Profundo","dmg_mult":1.8 ,"effect":"lifesteal","effect_value":0.5 ,"effect_chance":1.0 ,
"min_rank_idx":3 ,"desc":"Dreno massivo de vida"},

{"name":"Aniquilacao Conceitual","dmg_mult":3.0 ,"effect":"bleed","effect_value":7 ,"effect_chance":0.8 ,
"min_rank_idx":4 ,"desc":"Ataque que aniquila a existencia"},
{"name":"Dominio Paralisante","dmg_mult":1.5 ,"effect":"stun","effect_value":4 ,"effect_chance":0.6 ,
"min_rank_idx":4 ,"desc":"Campo que trava tudo"},
{"name":"Fornalha do Inferno","dmg_mult":2.8 ,"effect":"burn","effect_value":7 ,"effect_chance":0.7 ,
"min_rank_idx":4 ,"desc":"Calor infernal"},
{"name":"Sanguessuga Real","dmg_mult":2.0 ,"effect":"lifesteal","effect_value":0.7 ,"effect_chance":1.0 ,
"min_rank_idx":4 ,"desc":"Drena quase tudo"},
]

CURSE_ARCHETYPES ={
"Sombra":{
"ai_type":"speed_assassin",
"stat_bias":{"speed":1.25 ,"def":0.90 },
"abilities":[
{"name":"Corte nas Sombras","dmg_mult":1.3 ,"effect":"bleed","effect_value":3 ,"effect_chance":0.55 ,
"min_rank_idx":0 ,"desc":"Ataca a partir do escuro e some antes do golpe ser visto."},
{"name":"Manto de Breu","dmg_mult":1.7 ,"effect":"stun","effect_value":1 ,"effect_chance":0.35 ,
"min_rank_idx":2 ,"desc":"Envolve o alvo em trevas espessas, confundindo os sentidos."},
],
},
"Viscera":{
"ai_type":"adaptive_tank",
"stat_bias":{"hp":1.20 ,"speed":0.85 },
"abilities":[
{"name":"Investida Visceral","dmg_mult":1.4 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.6 ,
"min_rank_idx":0 ,"desc":"Massa de carne amaldicoada que esmaga e rasga ao mesmo tempo."},
{"name":"Regurgito Corrosivo","dmg_mult":1.6 ,"effect":"poison","effect_value":4 ,"effect_chance":0.5 ,
"min_rank_idx":2 ,"desc":"Cospe bile amaldicoada que corroi a carne."},
],
},
"Esporo":{
"ai_type":"basic_smart",
"stat_bias":{"hp":1.10 },
"abilities":[
{"name":"Nuvem de Esporos","dmg_mult":0.9 ,"effect":"poison","effect_value":5 ,"effect_chance":0.75 ,
"min_rank_idx":0 ,"desc":"Libera esporos toxicos que grudam na pele do alvo."},
{"name":"Floracao Parasitica","dmg_mult":1.5 ,"effect":"poison","effect_value":6 ,"effect_chance":0.6 ,
"min_rank_idx":3 ,"desc":"Esporos brotam de dentro do alvo, causando dano continuo severo."},
],
},
"Espelho":{
"ai_type":"smart",
"stat_bias":{"def":1.20 },
"abilities":[
{"name":"Reflexo Cortante","dmg_mult":1.2 ,"effect":None ,"effect_chance":0.0 ,
"min_rank_idx":0 ,"desc":"Devolve parte da forca do golpe recebido em forma de estilhacos."},
{"name":"Fractura Dimensional","dmg_mult":1.8 ,"effect":"stun","effect_value":1 ,"effect_chance":0.4 ,
"min_rank_idx":2 ,"desc":"O reflexo se parte, atacando de varios angulos ao mesmo tempo."},
],
},
"Cobra":{
"ai_type":"combo_swapper",
"stat_bias":{"speed":1.15 },
"abilities":[
{"name":"Presa Envenenada","dmg_mult":1.1 ,"effect":"poison","effect_value":4 ,"effect_chance":0.7 ,
"min_rank_idx":0 ,"desc":"Presas inoculam veneno amaldicoado a cada mordida."},
{"name":"Constricao Fatal","dmg_mult":1.5 ,"effect":"poison","effect_value":6 ,"effect_chance":0.65 ,
"min_rank_idx":2 ,"desc":"Enrosca o alvo e aperta enquanto injeta veneno."},
],
},
"Aranha":{
"ai_type":"speed_assassin",
"stat_bias":{"speed":1.20 ,"hp":0.90 },
"abilities":[
{"name":"Picada Paralisante","dmg_mult":1.0 ,"effect":"stun","effect_value":1 ,"effect_chance":0.45 ,
"min_rank_idx":0 ,"desc":"Ferrao rapido que trava os musculos do alvo."},
{"name":"Teia Amaldicoada","dmg_mult":1.3 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.55 ,
"min_rank_idx":2 ,"desc":"Prende o alvo em fios cortantes como lamina."},
],
},
"Mascara":{
"ai_type":"smart",
"stat_bias":{"ce":1.20 },
"abilities":[
{"name":"Rosto do Terror","dmg_mult":1.0 ,"effect":"stun","effect_value":2 ,"effect_chance":0.5 ,
"min_rank_idx":0 ,"desc":"Revela um rosto que quebra a sanidade de quem olha."},
{"name":"Mil Faces","dmg_mult":1.6 ,"effect":"stun","effect_value":2 ,"effect_chance":0.4 ,
"min_rank_idx":3 ,"desc":"Troca de rosto a cada golpe, confundindo os reflexos do alvo."},
],
},
"Pulcao":{
"ai_type":"combo_swapper",
"stat_bias":{"hp":1.15 },
"abilities":[
{"name":"Sucção Amaldicoada","dmg_mult":1.1 ,"effect":"lifesteal","effect_value":0.35 ,"effect_chance":1.0 ,
"min_rank_idx":0 ,"desc":"Gruda no alvo e drena a energia vital aos poucos."},
{"name":"Fartura Sangrenta","dmg_mult":1.6 ,"effect":"lifesteal","effect_value":0.55 ,"effect_chance":1.0 ,
"min_rank_idx":2 ,"desc":"Drena uma quantidade absurda de vida em um unico bote."},
],
},
"Tumor":{
"ai_type":"adaptive_tank",
"stat_bias":{"hp":1.30 ,"speed":0.75 },
"abilities":[
{"name":"Crescimento Descontrolado","dmg_mult":1.2 ,"effect":"poison","effect_value":3 ,"effect_chance":0.5 ,
"min_rank_idx":0 ,"desc":"Massa amaldicoada que incha e se multiplica ao atacar."},
{"name":"Metastase Amaldicoada","dmg_mult":1.7 ,"effect":"poison","effect_value":5 ,"effect_chance":0.6 ,
"min_rank_idx":3 ,"desc":"Espalha fragmentos de si mesma para dentro do alvo."},
],
},
"Vortice":{
"ai_type":"ranged_aggro",
"stat_bias":{"ce":1.25 ,"def":0.85 },
"abilities":[
{"name":"Sugao de CE","dmg_mult":1.3 ,"effect":None ,"effect_chance":0.0 ,
"min_rank_idx":0 ,"desc":"Um vortice de energia amaldicoada que puxa e esmaga o alvo."},
{"name":"Colapso Espacial","dmg_mult":2.0 ,"effect":"stun","effect_value":1 ,"effect_chance":0.35 ,
"min_rank_idx":3 ,"desc":"Comprime o espaco ao redor do alvo em um instante."},
],
},
"Lamina":{
"ai_type":"physical_striker",
"stat_bias":{"atk":1.15 },
"abilities":[
{"name":"Corte Preciso","dmg_mult":1.5 ,"effect":"bleed","effect_value":3 ,"effect_chance":0.6 ,
"min_rank_idx":0 ,"desc":"Um unico corte calculado, limpo e profundo."},
{"name":"Mil Cortes","dmg_mult":1.4 ,"effect":"bleed","effect_value":6 ,"effect_chance":0.7 ,
"min_rank_idx":2 ,"desc":"Uma rajada de cortes rapidos demais para acompanhar."},
],
},
"Cristal":{
"ai_type":"physical_striker",
"stat_bias":{"def":1.25 ,"speed":0.90 },
"abilities":[
{"name":"Estilhaco Cortante","dmg_mult":1.4 ,"effect":"bleed","effect_value":3 ,"effect_chance":0.5 ,
"min_rank_idx":0 ,"desc":"Fragmentos de cristal amaldicoado disparados a queima-roupa."},
{"name":"Prisma Fragmentado","dmg_mult":1.8 ,"effect":None ,"effect_chance":0.0 ,
"min_rank_idx":2 ,"desc":"Um golpe refratado que multiplica sua propria forca."},
],
},
"Olho":{
"ai_type":"smart",
"stat_bias":{"ce":1.15 },
"abilities":[
{"name":"Olhar Paralisante","dmg_mult":0.9 ,"effect":"stun","effect_value":2 ,"effect_chance":0.5 ,
"min_rank_idx":0 ,"desc":"Um unico olhar que trava o corpo do alvo por instantes."},
{"name":"Visao Absoluta","dmg_mult":1.5 ,"effect":"stun","effect_value":2 ,"effect_chance":0.45 ,
"min_rank_idx":3 ,"desc":"Enxerga cada fraqueza do alvo e ataca todas de uma vez."},
],
},
"Boca":{
"ai_type":"combo_swapper",
"stat_bias":{"atk":1.10 },
"abilities":[
{"name":"Mordida Voraz","dmg_mult":1.4 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.6 ,
"min_rank_idx":0 ,"desc":"Fileiras de dentes que rasgam carne e alma."},
{"name":"Devorar Vida","dmg_mult":1.6 ,"effect":"lifesteal","effect_value":0.4 ,"effect_chance":1.0 ,
"min_rank_idx":2 ,"desc":"Uma mordida profunda que rouba parte da vida do alvo."},
],
},
"Mao":{
"ai_type":"physical_striker",
"stat_bias":{"atk":1.20 },
"abilities":[
{"name":"Golpe Esmagador","dmg_mult":1.6 ,"effect":None ,"effect_chance":0.0 ,
"min_rank_idx":0 ,"desc":"Uma mao amaldicoada gigante que esmaga tudo em seu caminho."},
{"name":"Garra que Perfura","dmg_mult":1.5 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.65 ,
"min_rank_idx":2 ,"desc":"Dedos afiados como lanca que atravessam qualquer defesa."},
],
},
"Craneo":{
"ai_type":"adaptive_tank",
"stat_bias":{"hp":1.25 ,"def":1.15 },
"abilities":[
{"name":"Investida Cranial","dmg_mult":1.3 ,"effect":"stun","effect_value":1 ,"effect_chance":0.4 ,
"min_rank_idx":0 ,"desc":"Uma cabecada amaldicoada capaz de rachar pedra."},
{"name":"Grito da Caveira","dmg_mult":1.1 ,"effect":"stun","effect_value":2 ,"effect_chance":0.5 ,
"min_rank_idx":2 ,"desc":"Um grito que ressoa direto nos ossos do alvo."},
],
},
"Coracao":{
"ai_type":"combo_swapper",
"stat_bias":{"hp":1.15 ,"ce":1.10 },
"abilities":[
{"name":"Pulso Amaldicoado","dmg_mult":1.2 ,"effect":"lifesteal","effect_value":0.3 ,"effect_chance":1.0 ,
"min_rank_idx":0 ,"desc":"Cada batida bombeia energia amaldicoada para o ataque."},
{"name":"Parada Cardiaca Forcada","dmg_mult":1.7 ,"effect":"stun","effect_value":1 ,"effect_chance":0.4 ,
"min_rank_idx":3 ,"desc":"Forca o ritmo cardiaco do alvo a falhar por um instante."},
],
},
"Veia":{
"ai_type":"basic_smart",
"stat_bias":{"speed":1.10 },
"abilities":[
{"name":"Latigo de Veias","dmg_mult":1.3 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.6 ,
"min_rank_idx":0 ,"desc":"Filamentos vivos que se esticam e cortam a distancia."},
{"name":"Hemorragia Forcada","dmg_mult":1.5 ,"effect":"bleed","effect_value":7 ,"effect_chance":0.65 ,
"min_rank_idx":2 ,"desc":"Rompe vasos do alvo de dentro para fora."},
],
},
"Osso":{
"ai_type":"adaptive_tank",
"stat_bias":{"def":1.30 ,"speed":0.80 },
"abilities":[
{"name":"Lanca Ossea","dmg_mult":1.4 ,"effect":"bleed","effect_value":3 ,"effect_chance":0.55 ,
"min_rank_idx":0 ,"desc":"Projeta fragmentos de osso afiado como lancas."},
{"name":"Armadura de Ossos","dmg_mult":1.2 ,"effect":None ,"effect_chance":0.0 ,
"min_rank_idx":2 ,"desc":"Reveste o proprio corpo com placas osseas antes de atacar."},
],
},
"Sangue":{
"ai_type":"combo_swapper",
"stat_bias":{"atk":1.15 ,"speed":1.10 },
"abilities":[
{"name":"Chicote de Sangue","dmg_mult":1.3 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.6 ,
"min_rank_idx":0 ,"desc":"Controla o proprio sangue amaldicoado como arma."},
{"name":"Chuva Escarlate","dmg_mult":1.8 ,"effect":"bleed","effect_value":6 ,"effect_chance":0.65 ,
"min_rank_idx":3 ,"desc":"Uma explosao de sangue amaldicoado que corta tudo ao redor."},
],
},
}

CURSE_MODIFIERS =[
("enraged","+50% ATK, -20% DEF",{"atk":1.5 ,"def":0.8 }),
("armored","+100% DEF, -20% Speed",{"def":2.0 ,"speed":0.8 }),
("swift","+50% Speed, -20% HP",{"speed":1.5 ,"hp":0.8 }),
("vampiric","Lifesteal 30%",{"lifesteal_pct":0.30 }),
("explosive","Explode ao morrer (dano AOE)",{"explosive":True }),
("regenerating","Regenera 5% HP/turno",{"regen_pct":0.05 }),
("shielded","Imune ao primeiro ataque",{"shielded":True }),
("berserker","+100% ATK quando HP < 50%",{"berserker":True }),
("toxic","Ataques causam poison",{"always_poison":3 }),
("evasive","+30% esquiva",{"dodge_bonus":0.30 }),
("crit_master","+25% chance critica",{"crit_bonus":0.25 }),
("tank","+50% HP, -30% Speed",{"hp":1.5 ,"speed":0.7 }),
]

def _get_rank_idx (rank ):

    return RANK_ORDER .index (rank )if rank in RANK_ORDER else 0 

def _roll_curse_abilities (rank ,curse_type =None ,count =3 ):

    rank_idx =_get_rank_idx (rank )
    archetype =CURSE_ARCHETYPES .get (curse_type )

    signature =[]
    if archetype :
        signature =[a for a in archetype ["abilities"]if a ["min_rank_idx"]<=rank_idx ]

    eligible_generic =[a for a in CURSE_ABILITIES if a ["min_rank_idx"]<=rank_idx ]
    if not eligible_generic :
        eligible_generic =[CURSE_ABILITIES [0 ]]

    target_total =min (len (signature )+len (eligible_generic ),max (2 ,count +(rank_idx //2 )))
    n_generic =max (0 ,target_total -len (signature ))
    generic_pick =random .sample (eligible_generic ,min (n_generic ,len (eligible_generic )))

    moveset =list (signature )+generic_pick 
    if not moveset :
        moveset =[CURSE_ABILITIES [0 ]]
    random .shuffle (moveset )
    return moveset 

def _roll_curse_combat_capabilities (rank ):

    rank_idx =_get_rank_idx (rank )
    return {
    "can_dodge":True ,
    "can_defend":True ,
    "can_crit":True ,
    "can_use_skills":True ,
    "dodge_chance":min (0.40 ,0.05 +rank_idx *0.05 ),
    "defense_chance":min (0.40 ,0.10 +rank_idx *0.05 ),
    "crit_chance":min (0.30 ,0.05 +rank_idx *0.04 ),
    "crit_mult":1.5 +rank_idx *0.1 ,
    "stun_resist":min (0.55 ,0.05 +rank_idx *0.10 ),
    }

def generate_procedural_curse (rank =None ,level_mult =1.0 ,danger_mult =1.0 ):

    if rank is None :
        rank =random .choice (list (CURSE_TEMPLATES .keys ()))
    template =random .choice (CURSE_TEMPLATES [rank ])

    curse_name ,curse_type =generate_curse_name_and_type ()
    archetype =CURSE_ARCHETYPES .get (curse_type ,{})
    stat_bias =archetype .get ("stat_bias",{})

    variance =0.8 +random .random ()*0.4 
    total_mult =variance *level_mult *danger_mult 

    curse ={
    "name":curse_name ,
    "curse_type":curse_type ,
    "rank":rank ,
    "hp":int (template ["hp"]*total_mult *stat_bias .get ("hp",1.0 )),
    "max_hp":int (template ["hp"]*total_mult *stat_bias .get ("hp",1.0 )),
    "atk":int (template ["atk"]*total_mult *stat_bias .get ("atk",1.0 )),
    "def":int (template ["def"]*total_mult *stat_bias .get ("def",1.0 )),
    "speed":int (template ["speed"]*total_mult *stat_bias .get ("speed",1.0 )),
    "ce":int (template ["ce"]*total_mult *stat_bias .get ("ce",1.0 )),
    "max_ce":int (template ["ce"]*total_mult *stat_bias .get ("ce",1.0 )),
    "xp":int (template ["xp"]*level_mult ),
    "drops_mult":template ["drops_mult"],
    "is_boss":False ,
    "is_procedural":True ,
    "ai_type":archetype .get ("ai_type",random .choice (["physical_striker","combo_swapper","smart","basic_smart"])),
    "phases":[],
    "karma_reward":-1 ,
    }

    curse ["abilities"]=_roll_curse_abilities (rank ,curse_type =curse_type )

    caps =_roll_curse_combat_capabilities (rank )
    curse .update (caps )

    if random .random ()<0.10 and rank in ("Grau 1","Grau Especial"):
        curse ["technique"]=random .choice ([t for t in INNATE_TECHNIQUES .keys ()
        if INNATE_TECHNIQUES [t ].get ("weight",0 )>0 ])
        curse ["extensions_known"]=[ext ["name"]for ext in 
        INNATE_TECHNIQUES [curse ["technique"]]["extensions"][:2 ]]
    else :
        curse ["technique"]="Nenhuma"
        curse ["extensions_known"]=[]

    if random .random ()<0.20 :
        curse ["trait"]=random .choice ([n for n ,d in BIRTH_TRAITS .items ()if d .get ("weight",0 )>0 ])
    else :
        curse ["trait"]=None 

    if random .random ()<0.25 :
        mod_name ,mod_desc ,mod_effects =random .choice (CURSE_MODIFIERS )
        curse ["modifier"]=mod_name 
        curse ["modifier_desc"]=mod_desc 

        if "atk"in mod_effects :
            curse ["atk"]=int (curse ["atk"]*mod_effects ["atk"])
        if "def"in mod_effects :
            curse ["def"]=int (curse ["def"]*mod_effects ["def"])
        if "speed"in mod_effects :
            curse ["speed"]=int (curse ["speed"]*mod_effects ["speed"])
        if "hp"in mod_effects :
            curse ["hp"]=int (curse ["hp"]*mod_effects ["hp"])
            curse ["max_hp"]=curse ["hp"]
        if "lifesteal_pct"in mod_effects :
            curse ["lifesteal_pct"]=mod_effects ["lifesteal_pct"]
        if "regen_pct"in mod_effects :
            curse ["regen"]=int (curse ["max_hp"]*mod_effects ["regen_pct"])
        if "dodge_bonus"in mod_effects :
            curse ["dodge_chance"]=min (0.60 ,curse .get ("dodge_chance",0.05 )+mod_effects ["dodge_bonus"])
        if "crit_bonus"in mod_effects :
            curse ["crit_chance"]=min (0.50 ,curse .get ("crit_chance",0.05 )+mod_effects ["crit_bonus"])

        if mod_effects .get ("explosive"):
            curse ["explosive"]=True 
        if mod_effects .get ("shielded"):
            curse ["shielded"]=True 
        if mod_effects .get ("berserker"):
            curse ["berserker"]=True 
        if mod_effects .get ("always_poison"):
            curse ["always_poison"]=mod_effects ["always_poison"]
    else :
        curse ["modifier"]=None 
        curse ["modifier_desc"]=None 

    return curse 

def generate_procedural_sorcerer (rank =None ,level_mult =1.0 ):

    if rank is None :
        rank =random .choice (["Grau 3","Grau 2","Grau 1"])

    base_stats ={
    "Grau 4":{"hp":100 ,"atk":15 ,"def":8 ,"speed":10 ,"ce":50 },
    "Grau 3":{"hp":200 ,"atk":25 ,"def":12 ,"speed":15 ,"ce":100 },
    "Grau 2":{"hp":350 ,"atk":40 ,"def":18 ,"speed":20 ,"ce":200 },
    "Grau 1":{"hp":600 ,"atk":65 ,"def":25 ,"speed":25 ,"ce":350 },
    "Grau Especial":{"hp":1000 ,"atk":100 ,"def":40 ,"speed":30 ,"ce":600 },
    }
    stats =base_stats .get (rank ,base_stats ["Grau 2"])
    variance =0.85 +random .random ()*0.3 
    total_mult =variance *level_mult 

    sorcerer ={
    "name":generate_sorcerer_name (),
    "rank":rank ,
    "hp":int (stats ["hp"]*total_mult ),
    "max_hp":int (stats ["hp"]*total_mult ),
    "atk":int (stats ["atk"]*total_mult ),
    "def":int (stats ["def"]*total_mult ),
    "speed":int (stats ["speed"]*total_mult ),
    "ce":int (stats ["ce"]*total_mult ),
    "max_ce":int (stats ["ce"]*total_mult ),
    "xp":int (stats ["hp"]*0.5 ),
    "drops_mult":1.5 ,
    "is_boss":False ,
    "is_procedural":True ,
    "is_human":True ,
    "phases":[],
    "karma_reward":-5 ,
    }

    sorcerer ["technique"]=random .choice (list (INNATE_TECHNIQUES .keys ()))
    sorcerer ["extensions_known"]=[ext ["name"]for ext in 
    INNATE_TECHNIQUES [sorcerer ["technique"]]["extensions"][:3 ]]

    if random .random ()<0.30 :
        sorcerer ["trait"]=random .choice ([n for n ,d in BIRTH_TRAITS .items ()if d .get ("weight",0 )>0 ])
    else :
        sorcerer ["trait"]=None 

    sorcerer ["ai_type"]="smart_sorcerer"

    if random .random ()<0.05 :
        sorcerer ["heavenly_restriction"]=True 
        sorcerer ["hp"]=int (sorcerer ["hp"]*1.5 )
        sorcerer ["atk"]=int (sorcerer ["atk"]*1.5 )
        sorcerer ["speed"]=int (sorcerer ["speed"]*1.5 )
        sorcerer ["ce"]=0 
        sorcerer ["max_ce"]=0 

    return sorcerer 

def generate_procedural_boss (rank ="Grau Especial",level_mult =1.0 ):
    base =generate_procedural_curse (rank ,level_mult ,1.8 )
    base ["name"]=generate_curse_name ()+" (CHEFE)"
    base ["is_boss"]=True 
    base ["hp"]=int (base ["hp"]*1.8 )
    base ["max_hp"]=base ["hp"]
    base ["atk"]=int (base ["atk"]*1.5 )
    base ["def"]=int (base ["def"]*1.5 )
    base ["xp"]=int (base ["xp"]*4 )
    base ["stun_resist"]=min (0.65 ,0.25 +0.10 *4 )

    base ["technique"]=random .choice (list (INNATE_TECHNIQUES .keys ()))
    base ["extensions_known"]=[ext ["name"]for ext in 
    INNATE_TECHNIQUES [base ["technique"]]["extensions"]]

    base ["phases"]=[
    {"hp_pct_below":0.5 ,"buff":{"atk":1.3 ,"speed":1.2 },
    "msg":f"{base ['name']} entra em furia!","applied":False },
    ]

    return base 

def generate_enemy_group (player_level ,group_size =3 ,danger_mult =1.0 ):

    enemies =[]
    for i in range (group_size ):

        if player_level <5 :
            rank =random .choice (["Grau 4","Grau 4","Grau 3"])
        elif player_level <10 :
            rank =random .choice (["Grau 3","Grau 3","Grau 2"])
        elif player_level <20 :
            rank =random .choice (["Grau 2","Grau 2","Grau 1"])
        elif player_level <30 :
            rank =random .choice (["Grau 1","Grau 1","Grau 2"])
        else :
            rank =random .choice (["Grau 1","Grau Especial"])

        level_mult =1.0 +(player_level -1 )*0.05 
        e =generate_procedural_curse (rank ,level_mult ,danger_mult )

        if i >0 :
            e ["name"]=f"{e ['name']} {chr (65 +i )}"
        enemies .append (e )
    return enemies 

def generate_ally_sorcerer (player_level ,rank ="Grau 2"):

    s =generate_procedural_sorcerer (rank )
    s ["name"]=generate_sorcerer_name ()+" (Aliado)"
    s ["is_ally"]=True 
    s ["is_player"]=False 
    s ["is_enemy"]=False 
    s ["ai_type"]="smart_sorcerer"
    s ["dialogue"]=["Vamos la!","Cuidei desse!","Bom trabalho!"]
    return s
