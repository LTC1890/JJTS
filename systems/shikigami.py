
import random
import sys
import os

sys .path .insert (0 ,os .path .dirname (os .path .abspath (__file__ )))

import mahoraga as mahoraga_mod

SHIKIGAMI_DB ={
"Divine Dogs":{
"name":"Cachorros Divinos",
"rank":"Grau 3",
"desc":"Dois lobos geminados de sombra. Rápidos e ferozes, atacam em sincronia.",
"hp_mult":0.8 ,
"atk_mult":0.7 ,
"ce_cost_per_turn":12 ,
"invoke_ce_cost":35 ,
"duration":None ,
"tamed":True ,
"attacks":[
{"name":"Mordida Dupla","dmg_pct":1.0 ,"effect":None ,"hits":2 },
{"name":"Investida Sincronizada","dmg_pct":1.3 ,"effect":None ,"hits":1 },
{"name":"Garra das Sombras","dmg_pct":0.9 ,"effect":"bleed","hits":1 },
],
"on_invoke":None ,
},
"Nue":{
"name":"Nue (Ave Eletrica)",
"rank":"Grau 3",
"desc":"Ave-serpente eletrica que voa pelo ar e dispara raios paralisantes.",
"hp_mult":0.7 ,
"atk_mult":0.8 ,
"ce_cost_per_turn":15 ,
"invoke_ce_cost":40 ,
"duration":None ,
"tamed":True ,
"attacks":[
{"name":"Bico Perfurante","dmg_pct":1.1 ,"effect":None ,"hits":1 },
{"name":"Raio Paralisante","dmg_pct":0.8 ,"effect":"stun","hits":1 },
{"name":"Investida Eletrica","dmg_pct":1.2 ,"effect":"stun_chance","hits":1 },
],
"on_invoke":None ,
},
"Great Serpent":{
"name":"Grande Serpente",
"rank":"Grau 2",
"desc":"Serpente colosal de sombra. Estrangula o inimigo e cospe veneno.",
"hp_mult":1.0 ,
"atk_mult":0.9 ,
"ce_cost_per_turn":18 ,
"invoke_ce_cost":50 ,
"duration":None ,
"tamed":True ,
"attacks":[
{"name":"Constricao","dmg_pct":1.3 ,"effect":None ,"hits":1 },
{"name":"Mordida Venenosa","dmg_pct":0.9 ,"effect":"poison","hits":1 },
{"name":"Engolir","dmg_pct":1.6 ,"effect":None ,"hits":1 },
],
"on_invoke":None ,
},
"Toad":{
"name":"Sapo",
"rank":"Grau 4",
"desc":"Sapo gigante de sombra. Pula no inimigo e o atordoa com a lingua pegajosa.",
"hp_mult":0.6 ,
"atk_mult":0.5 ,
"ce_cost_per_turn":8 ,
"invoke_ce_cost":25 ,
"duration":2 ,
"tamed":True ,
"attacks":[
{"name":"Lingua Pegajosa","dmg_pct":0.7 ,"effect":"stun","hits":1 },
{"name":"Pulo Esmagador","dmg_pct":1.0 ,"effect":None ,"hits":1 },
],
"on_invoke":"stun_inimigo_2turnos",
},
"Max Elephant":{
"name":"Max Elefante",
"rank":"Grau 2",
"desc":"Elefante colossal de sombra que cai em cima do inimigo e jorra agua devastadora.",
"hp_mult":1.5 ,
"atk_mult":1.2 ,
"ce_cost_per_turn":25 ,
"invoke_ce_cost":70 ,
"duration":None ,
"tamed":True ,
"attacks":[
{"name":"Pisada Esmagadora","dmg_pct":1.5 ,"effect":None ,"hits":1 },
{"name":"Jato de Agua","dmg_pct":1.3 ,"effect":"knockback","hits":1 },
{"name":"Investida do Elefante","dmg_pct":1.7 ,"effect":None ,"hits":1 },
],
"on_invoke":"dano_queda_31_a_60",
},
"Rabbit Escape":{
"name":"Fuga dos Coelhos",
"rank":"Grau 4",
"desc":"Invoca uma horda de coelhos de sombra que permitem fugir da batalha.",
"hp_mult":0.3 ,
"atk_mult":0.1 ,
"ce_cost_per_turn":0 ,
"invoke_ce_cost":30 ,
"duration":2 ,
"tamed":True ,
"attacks":[],
"on_invoke":"fuga_garantida_2turnos",
},
"Round Deer":{
"name":"Cervo Redondo",
"rank":"Grau 2",
"desc":"Cervo de sombra que cura o invocador com sua luz benevolente.",
"hp_mult":1.0 ,
"atk_mult":0.6 ,
"ce_cost_per_turn":0 ,
"invoke_ce_cost":80 ,
"duration":1 ,
"tamed":True ,
"attacks":[],
"on_invoke":"cura_100_hp",
},
"Piercing Ox":{
"name":"Touro Perfurante",
"rank":"Grau 1",
"desc":"Touro colosal de sombra que caminha reto e da uma chifrada devastadora.",
"hp_mult":1.8 ,
"atk_mult":1.5 ,
"ce_cost_per_turn":22 ,
"invoke_ce_cost":65 ,
"duration":3 ,
"tamed":True ,
"attacks":[
{"name":"Chifrada","dmg_pct":1.8 ,"effect":None ,"hits":1 },
{"name":"Investida Retilinea","dmg_pct":2.0 ,"effect":None ,"hits":1 },
],
"on_invoke":None ,
},
"Eight-Handled Sword Mahoraga":{
"name":"Mahoraga",
"rank":"Grau Especial",
"desc":("O shikigami mais poderoso das Dez Sombras. Adaptase a qualquer ataque. "
"PRIMEIRA INVOCACAO: voce precisa derrota-lo para domina-lo. "
"Se falhar, voce morre. Apos domado, fica disponivel para futuras batalhas."),
"hp_mult":2.0 ,
"atk_mult":2.0 ,
"ce_cost_per_turn":50 ,
"invoke_ce_cost":150 ,
"duration":None ,
"tamed":False ,
"attacks":[
{"name":"Espada da Roda","dmg_pct":2.0 ,"effect":None ,"hits":1 },
{"name":"Adaptacao Destrutiva","dmg_pct":2.5 ,"effect":"adapt","hits":1 },
{"name":"Punho Adaptativo","dmg_pct":1.8 ,"effect":None ,"hits":1 },
],
"on_invoke":None ,
"ritual":True ,
},

"Merged Beast":{
"name":"Besta Fundida (Chimera)",
"rank":"Grau Especial",
"desc":("Fusao de multiplos shikigamis numa unica aberracao. "
"Disponivel apenas apos dominar Mahoraga. Ataques devastadores."),
"hp_mult":2.5 ,
"atk_mult":2.5 ,
"ce_cost_per_turn":60 ,
"invoke_ce_cost":200 ,
"duration":5 ,
"tamed":False ,
"attacks":[
{"name":"Mordida da Quimera","dmg_pct":2.2 ,"effect":"bleed","hits":1 },
{"name":"Investida Apocaliptica","dmg_pct":2.8 ,"effect":None ,"hits":1 },
{"name":"Rugido Destrutivo","dmg_pct":2.0 ,"effect":"stun","hits":1 },
],
"on_invoke":None ,
},
}

def get_shikigami (name ):

    return SHIKIGAMI_DB .get (name )

def list_available_shikigami (player ):

    available =[]
    for name ,data in SHIKIGAMI_DB .items ():
        if name =="Eight-Handled Sword Mahoraga":

            available .append (name )
        elif name =="Merged Beast":

            if "Eight-Handled Sword Mahoraga"in player .tamed_shikigami :
                available .append (name )
        else :
            available .append (name )
    return available 

def calculate_shikigami_stats (shikigami_name ,player_level ):

    shikigami =SHIKIGAMI_DB .get (shikigami_name )
    if not shikigami :
        return 0 ,0 

    rank_hp ={
    "Grau 4":120 ,
    "Grau 3":220 ,
    "Grau 2":420 ,
    "Grau 1":750 ,
    "Grau Especial":1500 ,
    }
    base_hp =rank_hp .get (shikigami ["rank"],150 )
    hp =int (base_hp *shikigami ["hp_mult"]*(1 +player_level *0.07 ))

    rank_atk ={
    "Grau 4":18 ,
    "Grau 3":32 ,
    "Grau 2":55 ,
    "Grau 1":95 ,
    "Grau Especial":170 ,
    }
    base_atk =rank_atk .get (shikigami ["rank"],22 )
    atk =int (base_atk *shikigami ["atk_mult"]*(1 +player_level *0.07 ))

    return hp ,atk 

def create_active_shikigami (shikigami_name ,player_level ):

    shikigami =SHIKIGAMI_DB .get (shikigami_name )
    if not shikigami :
        return None 

    hp ,atk =calculate_shikigami_stats (shikigami_name ,player_level )

    return {
    "name":shikigami ["name"],
    "shikigami_id":shikigami_name ,
    "rank":shikigami ["rank"],
    "hp":hp ,
    "max_hp":hp ,
    "atk":atk ,
    "speed":20 +(player_level //2 ),
    "def":10 +(player_level //4 ),
    "ce_cost_per_turn":shikigami ["ce_cost_per_turn"],
    "duration":shikigami ["duration"],
    "attacks":shikigami ["attacks"],
    "on_invoke":shikigami ["on_invoke"],
    "tamed":shikigami ["tamed"],
    "is_shikigami":True ,
    "is_ally":True ,
    "is_player":False ,
    "is_enemy":False ,
    "buffs":[],
    "debuffs":[],
    "bleed_stacks":0 ,
    "stunned_turns":0 ,
    "adapt_stacks":0 ,
    "adaptive":shikigami_name =="Eight-Handled Sword Mahoraga",
    }

def shikigami_take_turn (shikigami ,enemies ,player ,ui_module =None ):

    from player import calculate_damage

    msgs =[]
    alive_enemies =[e for e in enemies if e .get ("hp",0 )>0 ]
    if not alive_enemies :
        return msgs 

    if not shikigami .get ("attacks"):
        return msgs 

    target =random .choice (alive_enemies )
    attack =random .choice (shikigami ["attacks"])

    atk =shikigami .get ("atk",20 )
    hits =attack .get ("hits",1 )
    total_dmg =0 

    for i in range (hits ):
        dmg =int (atk *attack ["dmg_pct"]*random .uniform (0.85 ,1.15 ))
        defense =target .get ("def",0 )
        actual =calculate_damage (dmg ,defense )
        target ["hp"]-=actual 
        total_dmg +=actual 

    if hits >1 :
        msgs .append (f"  {shikigami ['name']} usa {attack ['name']} - {hits } hits! Total: {total_dmg } dano em {target ['name']}.")
    else :
        msgs .append (f"  {shikigami ['name']} usa {attack ['name']} - {total_dmg } dano em {target ['name']}.")

    effect =attack .get ("effect")
    if effect =="bleed":
        target ["bleed_stacks"]=target .get ("bleed_stacks",0 )+2 
        msgs .append (f"  {target ['name']} esta sangrando!")
    elif effect =="stun":
        target ["stunned_turns"]=target .get ("stunned_turns",0 )+1 
        msgs .append (f"  {target ['name']} foi atordoado!")
    elif effect =="stun_chance":
        if random .random ()<0.5 :
            target ["stunned_turns"]=target .get ("stunned_turns",0 )+1 
            msgs .append (f"  {target ['name']} foi atordoado!")
    elif effect =="poison":
        target ["bleed_stacks"]=target .get ("bleed_stacks",0 )+3 
        msgs .append (f"  {target ['name']} foi envenenado!")
    elif effect =="knockback":

        if random .random ()<0.4 :
            target ["stunned_turns"]=target .get ("stunned_turns",0 )+1 
            msgs .append (f"  {target ['name']} foi derrubado!")
    elif effect =="adapt":

        msgs .append (f"  {shikigami ['name']} observa o golpe, registrando o padrao de movimento.")

    return msgs 

def tick_shikigami (shikigami ,player ,ui_module =None ):

    msgs =[]

    ce_cost =shikigami .get ("ce_cost_per_turn",0 )
    if ce_cost >0 :
        if player .ce_current <ce_cost :

            msgs .append (f"  CE insuficiente! {shikigami ['name']} se dissipa.")
            return msgs ,False 
        player .ce_current -=ce_cost 

    if shikigami .get ("duration")is not None :
        shikigami ["duration"]-=1 
        if shikigami ["duration"]<=0 :
            msgs .append (f"  {shikigami ['name']} cumpriu seu proposito e se dissipa.")
            return msgs ,False 

    if shikigami .get ("hp",0 )<=0 :
        msgs .append (f"  {shikigami ['name']} foi destruido!")
        return msgs ,False 

    return msgs ,True
