
import random 
import sys 
import os 

sys .path .insert (0 ,os .path .dirname (os .path .abspath (__file__ )))

import ui
from ui import Color ,c
from enemies import get_boss ,random_boss
from items import ITEMS_DB ,roll_loot ,roll_chest_loot
from generator import generate_procedural_curse ,generate_procedural_boss

ROOM_TYPES ={
"vazia":{"weight":25 ,"desc":"Uma sala vazia. Silencio total."},
"bau":{"weight":12 ,"desc":"Um bau repousa no centro da sala."},
"bau_amaldicoado":{"weight":6 ,"desc":"Um bau estranho pulsa com energia amaldicoada."},
"armadilha":{"weight":10 ,"desc":"Algo nao cheira bem aqui..."},
"descanso":{"weight":8 ,"desc":"Uma sala calma. Boa para descansar."},
"inimigo":{"weight":20 ,"desc":"Voce ouve rugidos vindos da sala."},
"elite":{"weight":8 ,"desc":"Uma maldicao poderosa te espera!"},
"evento":{"weight":8 ,"desc":"Algo interessante chama sua atencao."},
"chefe":{"weight":1 ,"desc":"Uma presenca esmagadora. O CHEFE desta masmorra."},
"escada":{"weight":2 ,"desc":"Uma escada leva ao proximo andar."},
}

class Dungeon :

    def __init__ (self ,player ,mission =None ,danger_level =None ,ui_module =None ):
        self .player =player 
        self .mission =mission 
        self .ui =ui_module or ui 

        if danger_level :
            self .danger_level =danger_level 
        else :
            if random .random ()<0.75 :
                self .danger_level =max (1 ,player .level_system .level )
            else :
                self .danger_level =random .randint (1 ,max (2 ,player .level_system .level *2 ))

        self .size =random .randint (5 ,12 )+(self .danger_level //5 )
        self .size =min (self .size ,25 )

        self .rooms =self .generate_rooms ()

        self .current_room =0 
        self .visited =set ()
        self .cleared =set ()
        self .escaped =False 
        self .completed =False 
        self .player_died =False 
        self .floor =1 

    def generate_rooms (self ):

        rooms =[]
        for i in range (self .size ):
            if i ==0 :

                room ={"type":"vazia","desc":"Entrada da masmorra.","explored":False ,"id":i }
            elif i ==self .size -1 :

                room ={"type":"chefe","desc":"Sala do chefe.","explored":False ,"id":i }
                rank ="Grau Especial"if self .danger_level >15 else "Grau 1"
                if self .mission and self .mission .get ("boss"):
                    room ["boss"]=get_boss (self .mission ["boss"])
                else :
                    if random .random ()<0.20 :
                        room ["boss"]=random_boss (rank )
                    else :
                        room ["boss"]=generate_procedural_boss (rank ,1.0 +self .danger_level *0.05 )
            else :

                types =list (ROOM_TYPES .keys ())
                weights =[ROOM_TYPES [t ]["weight"]for t in types ]
                rtype =random .choices (types ,weights =weights )[0 ]
                room ={
                "type":rtype ,
                "desc":ROOM_TYPES [rtype ]["desc"],
                "explored":False ,
                "id":i ,
                }

                if rtype =="bau":
                    room ["loot"]=roll_chest_loot (False )
                elif rtype =="bau_amaldicoado":
                    room ["loot"]=roll_chest_loot (True )
                elif rtype =="armadilha":
                    room ["trap_type"]=random .choice (["dano","veneno","ce_drain","teleport"])
                elif rtype in ("inimigo","elite"):
                    rank ="Grau 4"if self .danger_level <5 else "Grau 3"if self .danger_level <10 else "Grau 2"if self .danger_level <20 else "Grau 1"if self .danger_level <30 else "Grau Especial"
                    if rtype =="elite":
                        rank ="Grau 1"if rank =="Grau 2"else "Grau Especial"if rank =="Grau 1"else rank 
                    num_enemies =random .randint (1 ,3 )
                    room ["enemies"]=[]
                    for _ in range (num_enemies ):
                        room ["enemies"].append (generate_procedural_curse (
                        rank ,1.0 +self .danger_level *0.05 ,1.0 if rtype =="inimigo"else 1.5 
                        ))
                elif rtype =="chefe":
                    rank ="Grau Especial"if self .danger_level >15 else "Grau 1"
                    if self .mission and self .mission .get ("boss"):
                        room ["boss"]=get_boss (self .mission ["boss"])
                    else :
                        if random .random ()<0.20 :
                            room ["boss"]=random_boss (rank )
                        else :
                            room ["boss"]=generate_procedural_boss (rank ,1.0 +self .danger_level *0.05 )
                elif rtype =="evento":
                    room ["event"]=self .generate_dungeon_event ()
            rooms .append (room )
        return rooms 

    def generate_dungeon_event (self ):

        events =[
        "feiticeiro_morto",
        "dedo_sukuna",
        "altar_amaldicoado",
        "sangue_velho",
        "talisma_perdido",
        "maldicao_especial_cedo",
        "reflexo_espectral",
        "porta_selada",
        "npc_ferido",
        "tesouro_antigo",
        ]
        return random .choice (events )

    def explore (self ):

        self .ui .screen_header (self .ui .ASCII_DUNGEON ,f"MASMORRA - PERIGO: {self .danger_level }",
        color =Color .BRIGHT_RED )
        if self .mission :
            self .ui .tprint (c (f"\nMissao: {self .mission .get ('name','Investigar')}",Color .BRIGHT_CYAN ))
            self .ui .tprint (c (f"Objetivo: {self .mission .get ('desc','')}",Color .DIM ))
        self .ui .tprint (c (f"\nSalas: {self .size } | Andar: {self .floor }",Color .YELLOW ))
        self .ui .tprint (c ("Voce entra na masmorra...",Color .DIM ))
        self .ui .pause ()

        while True :
            if self .player_died :
                return "died"
            if self .escaped :
                return "escaped"
            if self .completed :
                return "completed"

            if self .size <=0 or not self .rooms :
                self .ui .tprint (c ("Erro: masmorra sem salas!",Color .RED ))
                return "escaped"
            self .current_room =max (0 ,min (self .current_room ,self .size -1 ))

            room =self .rooms [self .current_room ]

            room_id_before =self .current_room 

            self .enter_room (room )

            if self .player_died :
                return "died"

            if self .current_room !=room_id_before :
                continue 

            self .room_menu (room )

    def enter_room (self ,room ):

        if room ["id"]in self .cleared :
            return 

        self .ui .clear_screen ()
        self .ui .tprint (c (f"\n=== Sala {room ['id']+1 } ===",Color .BRIGHT_YELLOW +Color .BOLD ))
        self .ui .tprint (c (room ["desc"],Color .DIM ))

        rtype =room ["type"]

        if rtype =="vazia"or rtype =="escada":
            self .ui .tprint ("Nada de interessante aqui.")
            self .cleared .add (room ["id"])

        elif rtype =="bau":
            self .ui .tprint (c ("\nUm bau comum repousa aqui.",Color .BRIGHT_GREEN ))
            self .ui .pause ()
            self .open_chest (room ,cursed =False )

        elif rtype =="bau_amaldicoado":
            self .ui .tprint (c ("\nUm bau PULSA com energia amaldicoada.",Color .BRIGHT_MAGENTA +Color .BLINK ))
            self .ui .tprint (c ("Abrir pode ter consequencias...",Color .YELLOW ))
            self .ui .pause ()
            self .open_chest (room ,cursed =True )

        elif rtype =="armadilha":
            self .trigger_trap (room )

        elif rtype =="descanso":
            self .ui .tprint (c ("\nEsta sala parece segura. Voce pode descansar.",Color .GREEN ))
            self .player .rest_partial ()
            self .ui .tprint (c ("Voce descansou. HP e CE restaurados parcialmente.",Color .BRIGHT_GREEN ))
            self .cleared .add (room ["id"])
            self .ui .pause ()

        elif rtype =="inimigo":
            self .ui .tprint (c ("\n!! MALDICOES APARECEM !!",Color .BRIGHT_RED +Color .BOLD ))
            self .ui .pause ()
            result =self .fight_enemies (room )
            if result =="died":
                self .player_died =True 
                return 
            self .cleared .add (room ["id"])

        elif rtype =="elite":
            self .ui .tprint (c ("\n!! MALDICAÇÃO ELITE !!",Color .BRIGHT_RED +Color .BLINK ))
            self .ui .pause ()
            result =self .fight_enemies (room )
            if result =="died":
                self .player_died =True 
                return 
            self .cleared .add (room ["id"])

        elif rtype =="chefe":
            self .ui .tprint (c ("\n!! SALA DO CHEFE !!",Color .BRIGHT_RED +Color .BOLD +Color .BLINK ))
            if room .get ("boss"):
                boss =room ["boss"]
                self .ui .tprint (c (f"{boss ['name']} - {boss .get ('rank','?')}",Color .BRIGHT_RED +Color .BOLD ))
                if boss .get ("desc"):
                    self .ui .tprint (c (boss ["desc"],Color .DIM ))
                if boss .get ("intro"):
                    self .ui .tprint (c (f"\n{boss ['intro']}",Color .BRIGHT_YELLOW ))
            self .ui .pause ()
            result =self .fight_boss (room )
            if result =="died":
                self .player_died =True 
                return 

            self .cleared .add (room ["id"])
            if result =="victory"and room ["id"]==self .size -1 :
                self .completed =True 
                self .player .dungeons_explored +=1 

        elif rtype =="evento":
            self .trigger_event (room )
            self .cleared .add (room ["id"])

    def open_chest (self ,room ,cursed ):

        loot_type ,loot_name =room .get ("loot",(None ,None ))
        if loot_type =="trap":
            self .ui .tprint (c ("\n!! ARMADILHA !! O bau explode!",Color .BRIGHT_RED +Color .BOLD ))
            dmg =random .randint (20 ,50 )
            self .player .hp -=dmg 
            if self .player .hp <=0 :
                self .player .hp =0 
                self .player_died =True 
                self .ui .tprint (c ("Voce morreu pela armadilha!",Color .BRIGHT_RED +Color .BOLD ))
                self .ui .pause ()
                return 
            self .ui .tprint (c (f"-{dmg } HP",Color .RED ))
            if cursed :

                curse =generate_procedural_curse ("Grau 2",1.0 ,1.0 )
                self .ui .tprint (c (f"\n{curse ['name']} emerge do bau!",Color .BRIGHT_RED ))
                self .ui .pause ()
                result =self .fight_enemies ({"enemies":[curse ]})
                if result =="died":
                    self .player_died =True 
                    return 
            self .cleared .add (room ["id"])
            self .ui .pause ()
            return 

        if loot_name :
            self .ui .tprint (c (f"\nVoce abre o bau e encontra: {loot_name }!",Color .BRIGHT_GREEN +Color .BOLD ))
            item =ITEMS_DB .get (loot_name ,{})
            if item :
                self .ui .tprint (c (f"  {item .get ('desc','')}",Color .DIM ))
            if loot_name =="Dedo de Sukuna":
                self .player .sukuna_fingers_in_inventory +=1 
                self .ui .tprint (c ("!! DEDO DE SUKUNA !!",Color .BRIGHT_RED +Color .BOLD ))
            else :
                self .player .add_item (loot_name )

            money =random .randint (20 ,200 )
            self .player .money +=money 
            self .ui .tprint (c (f"+{money } ienes",Color .BRIGHT_YELLOW ))
        else :
            self .ui .tprint (c ("\nO bau esta vazio.",Color .DIM ))

        if cursed and random .random ()<0.30 :

            self .ui .tprint (c ("\nMas espera... uma maldicao espreitava!",Color .BRIGHT_RED ))
            self .ui .pause ()

            curse =generate_procedural_curse ("Grau 3",1.0 ,1.0 )
            result =self .fight_enemies ({"enemies":[curse ]})
            if result =="died":
                self .player_died =True 
                return 

        self .cleared .add (room ["id"])
        self .ui .pause ()

    def trigger_trap (self ,room ):

        trap_type =room .get ("trap_type","dano")
        self .ui .tprint (c ("\n!! ARMADILHA !!",Color .BRIGHT_RED +Color .BOLD ))

        if trap_type =="dano":
            dmg =random .randint (15 ,40 )
            self .player .hp -=dmg 
            if self .player .hp <=0 :
                self .player .hp =0 
                self .player_died =True 
                self .ui .tprint (c ("Voce morreu pela armadilha!",Color .BRIGHT_RED +Color .BOLD ))
                self .ui .pause ()
                return 
            self .ui .tprint (c (f"Espinhos saem do chao! -{dmg } HP",Color .RED ))
        elif trap_type =="veneno":
            self .player .add_debuff ("poison",5 ,5 ,"Veneno")
            self .ui .tprint (c ("Gas toxico! Voce foi envenenado por 5 turnos.",Color .GREEN ))
        elif trap_type =="ce_drain":
            drain =random .randint (20 ,50 )
            self .player .ce_current =max (0 ,self .player .ce_current -drain )
            self .ui .tprint (c (f"Selo drena {drain } de CE!",Color .BLUE ))
        elif trap_type =="teleport":
            self .ui .tprint (c ("Uma runa brilha e voce eh teleportado!",Color .BRIGHT_MAGENTA ))
            self .ui .pause ()
            self .cleared .add (room ["id"])

            self .current_room =random .randint (0 ,self .size -1 )
            self .ui .tprint (c (f"Voce esta agora na sala {self .current_room +1 }.",Color .YELLOW ))
            self .ui .pause ()
            return 

        from techniques import BIRTH_TRAITS 
        trait =BIRTH_TRAITS .get (self .player .birth_trait ,{})
        if "detection_range"in trait .get ("effects",{}):
            self .ui .tprint (c ("(Sua Percepcao de Energia te avisou cedo! Dano reduzido.)",Color .DIM ))

        self .cleared .add (room ["id"])
        self .ui .pause ()

    def fight_enemies (self ,room ):

        from combat import Combat 
        enemies =room .get ("enemies",[])
        if not enemies :
            return "victory"

        allies =[]
        if self .mission and self .mission .get ("allow_allies",True ):
            from allies import get_available_allies ,get_ally 
            available =get_available_allies (self .player )
            if available and random .random ()<0.50 :

                n_allies =min (2 ,len (available ))
                chosen =random .sample (available ,n_allies )
                allies =[get_ally (name )for name in chosen ]
                self .ui .tprint (c ("\nAliados aparecem para ajudar!",Color .BRIGHT_GREEN ))
                for a in allies :
                    self .ui .tprint (f"  - {a ['name']}")
                self .ui .pause ()

        combat =Combat (self .player ,enemies ,allies ,ui_module =self .ui )
        result =combat .start ()

        if result =="victory":
            self .ui .tprint (c ("\nInimigos derrotados!",Color .BRIGHT_GREEN ))
            return "victory"
        elif result =="defeat"or result =="permadeath":
            self .player_died =True 
            return "died"
        elif result =="fled":
            self .ui .tprint (c ("\nVoce fugiu! Mas a masmorra continua.",Color .YELLOW ))
            return "fled"
        elif result =="transformed":
            self .player_died =True 
            return "died"
        return "victory"

    def fight_boss (self ,room ):

        from combat import Combat 
        boss =room .get ("boss")
        if not boss :
            return "victory"

        allies =[]
        from allies import get_available_allies ,get_ally 
        available =get_available_allies (self .player )
        if available :
            n_allies =min (2 ,len (available ))
            chosen =random .sample (available ,n_allies )
            allies =[get_ally (name )for name in chosen ]
            self .ui .tprint (c ("\nSeus aliados estao com voce!",Color .BRIGHT_GREEN ))
            for a in allies :
                self .ui .tprint (f"  - {a ['name']}")

        combat =Combat (self .player ,[boss ],allies ,ui_module =self .ui ,allow_flee =False )
        result =combat .start ()

        if result =="victory":
            self .ui .tprint (c ("\n!! CHEFE DERROTADO !!",Color .BRIGHT_GREEN +Color .BOLD ))
            self .ui .tprint (c ("A masmorra esta completa!",Color .GREEN ))
            self .ui .pause ()
            return "victory"
        elif result in ("defeat","permadeath","transformed"):
            self .player_died =True 
            return "died"
        return "victory"

    def trigger_event (self ,room ):

        event =room .get ("event","feiticeiro_morto")
        self .ui .tprint (c ("\n=== EVENTO ===",Color .BRIGHT_CYAN +Color .BOLD ))

        if event =="feiticeiro_morto":
            self .ui .tprint (c ("Voce encontra o corpo de um feiticeiro morto.",Color .DIM ))
            self .ui .tprint (c ("Saques possiveis: itens, dinheiro...",Color .DIM ))
            self .ui .pause ()

            for _ in range (random .randint (1 ,3 )):
                item =roll_loot (1.0 )
                if item =="Dedo de Sukuna":
                    self .player .sukuna_fingers_in_inventory +=1 
                else :
                    self .player .add_item (item )
                self .ui .tprint (c (f"  + {item }",Color .BRIGHT_GREEN ))
            money =random .randint (50 ,300 )
            self .player .money +=money 
            self .ui .tprint (c (f"  + {money } ienes",Color .BRIGHT_YELLOW ))

        elif event =="dedo_sukuna":

            self .ui .tprint (c ("Voce encontra um objeto estranho no chao.",Color .DIM ))
            self .ui .tprint (c ("Um DEDO. Seco. Podre. Mas pulsando com poder.",Color .BRIGHT_RED ))
            self .ui .pause ()
            options =[
            "Pegar o dedo (com cuidado)",
            "Tentar comer o dedo (PERIGOSO)",
            "Ignorar e seguir",
            ]
            idx =self .ui .arrow_menu (options ,title ="O que fazer?")
            if idx ==0 :
                self .player .sukuna_fingers_in_inventory +=1 
                self .ui .tprint (c ("Voce pega o dedo. Ele esta no seu inventario.",Color .YELLOW ))
            elif idx ==1 :
                self .player .sukuna_fingers_in_inventory +=1 
                result =self .player .eat_sukuna_finger (ui_module =self .ui )
                if result in ("death","transformed"):
                    self .player_died =True 
                    self .ui .pause ()
                    return 
            else :
                self .ui .tprint (c ("Voce ignora o dedo. Melhor prevenir.",Color .DIM ))

        elif event =="altar_amaldicoado":
            self .ui .tprint (c ("Um altar amaldicoado pulsa no centro da sala.",Color .BRIGHT_MAGENTA ))
            options =[
            "Orar no altar (ganho de poder, perda de HP)",
            "Destruir o altar (+karma)",
            "Ignorar",
            ]
            idx =self .ui .arrow_menu (options ,title ="O que fazer?")
            if idx ==0 :
                self .player .hp =int (self .player .hp *0.7 )
                self .player .attributes ["ce"]+=2 
                self .player .karma .add_karma (-3 )
                self .ui .tprint (c ("Voce sente poder fluir... mas algo foi tomado.",Color .MAGENTA ))
                self .player .recalculate_derived ()
            elif idx ==1 :
                self .player .karma .add_karma (5 )
                self .player .add_item ("Cristal de CE")
                self .ui .tprint (c ("Altar destruido! +5 karma.",Color .BRIGHT_GREEN ))

        elif event =="sangue_velho":

            self .ui .tprint (c ("Voce encontra sangue amaldicoado antigo.",Color .RED ))
            if self .player .innate_technique =="Manipulacao de Sangue":
                self .ui .tprint (c ("Sua tecnica reage! Voce pode absorver o sangue.",Color .BRIGHT_RED ))
                self .player .attributes ["ce"]+=3 
                self .player .hp =self .player .max_hp 
                self .player .recalculate_derived ()
                self .player .hp =self .player .max_hp 
                self .ui .tprint (c ("+3 CE, HP maximo!",Color .BRIGHT_GREEN ))
            else :
                self .player .add_item ("Sangue Amaldicoado")
                self .ui .tprint (c ("Voce coleta o sangue.",Color .YELLOW ))

        elif event =="talisma_perdido":
            self .ui .tprint (c ("Um talisma antigo esta cravado na parede.",Color .CYAN ))
            self .player .add_item ("Cristal de CE Amaldicoado")
            self .ui .tprint (c ("+ Cristal de CE Amaldicoado!",Color .BRIGHT_GREEN ))

        elif event =="maldicao_especial_cedo":
            self .ui .tprint (c ("!! MALDICAÇÃO DE GRAU ESPECIAL APARECE SUBITAMENTE !!",Color .BRIGHT_RED +Color .BLINK ))
            self .ui .tprint (c ("Voce nao esperava por isso. Correr ou lutar?",Color .YELLOW ))
            options =[
            "Lutar (extrema dificuldade)",
            "Correr desesperadamente",
            ]
            idx =self .ui .arrow_menu (options ,title ="Decisao:")
            if idx ==0 :
                boss =random_boss ("Grau Especial")
                from combat import Combat 
                allies =[]
                from allies import get_available_allies ,get_ally 
                available =get_available_allies (self .player )
                if available :
                    allies =[get_ally (random .choice (available ))]
                combat =Combat (self .player ,[boss ],allies ,ui_module =self .ui )
                result =combat .start ()
                if result in ("defeat","permadeath","transformed"):
                    self .player_died =True 
            else :

                player_speed =self .player .get_total_speed ()
                if random .random ()<0.5 +player_speed *0.01 :
                    self .ui .tprint (c ("Voce consegue fugir!",Color .BRIGHT_GREEN ))
                else :
                    self .ui .tprint (c ("Nao consegue fugir! Lute!",Color .RED ))
                    self .ui .pause ()
                    boss =random_boss ("Grau Especial")
                    from combat import Combat 
                    combat =Combat (self .player ,[boss ],[],ui_module =self .ui )
                    result =combat .start ()
                    if result in ("defeat","permadeath","transformed"):
                        self .player_died =True 

        elif event =="reflexo_espectral":
            self .ui .tprint (c ("Um espelho magico reflete uma versao sombria de voce.",Color .BRIGHT_BLUE ))
            self .ui .tprint (c ("Seu reflexo ataca!",Color .RED ))

            clone ={
            "name":f"{self .player .name } (Sombra)",
            "rank":self .player .rank_system .rank ,
            "hp":self .player .max_hp ,
            "max_hp":self .player .max_hp ,
            "atk":self .player .get_total_str (),
            "def":self .player .get_total_def (),
            "speed":self .player .get_total_speed (),
            "ce":self .player .max_ce ,
            "max_ce":self .player .max_ce ,
            "xp":200 ,
            "is_boss":False ,
            "ai_type":"smart_sorcerer",
            "extensions_known":[],
            "phases":[],
            }
            from combat import Combat 
            combat =Combat (self .player ,[clone ],[],ui_module =self .ui )
            result =combat .start ()
            if result in ("defeat","permadeath","transformed"):
                self .player_died =True 

        elif event =="porta_selada":
            self .ui .tprint (c ("Uma porta selada por talismas.",Color .CYAN ))

            from techniques import BIRTH_TRAITS 
            trait =BIRTH_TRAITS .get (self .player .birth_trait ,{})
            if "detection_range"in trait .get ("effects",{}):
                self .ui .tprint (c ("Sua Percepcao desvenda o selo.",Color .GREEN ))

                for _ in range (3 ):
                    item =roll_loot (1.5 )
                    self .player .add_item (item )
                    self .ui .tprint (c (f"  + {item }",Color .BRIGHT_GREEN ))
            else :

                control =self .player .get_total_control ()
                if random .random ()<control *0.02 :
                    self .ui .tprint (c ("Seu controle de CE abre o selo.",Color .GREEN ))
                    for _ in range (2 ):
                        item =roll_loot (1.0 )
                        self .player .add_item (item )
                        self .ui .tprint (c (f"  + {item }",Color .BRIGHT_GREEN ))
                else :
                    self .ui .tprint (c ("Nao consegue abrir. Segue em frente.",Color .DIM ))

        elif event =="npc_ferido":
            self .ui .tprint (c ("Um feiticeiro ferido esta aqui. Maldicoes o atacaram.",Color .DIM ))
            options =[
            "Salvar o feiticeiro (+karma)",
            "Saquear o feiticeiro (-karma, +itens)",
            "Ignorar",
            ]
            idx =self .ui .arrow_menu (options ,title ="O que fazer?")
            if idx ==0 :
                self .player .karma .on_civil_salvo ()
                self .ui .tprint (c ("Voce cuida do feiticeiro. Ele te da itens em gratidao.",Color .BRIGHT_GREEN ))
                self .player .add_item ("Selo de CE Basico")
                self .player .add_item ("Selo de Cura")
                self .player .money +=100 
            elif idx ==1 :
                self .player .karma .add_karma (-5 )
                self .player .add_item ("Cristal de CE")
                self .player .money +=200 
                self .ui .tprint (c ("Voce saqueia o ferido. Que vergonha.",Color .RED ))

        elif event =="tesouro_antigo":
            self .ui .tprint (c ("Um tesouro antigo escondido!",Color .BRIGHT_YELLOW +Color .BOLD ))
            for _ in range (random .randint (2 ,5 )):
                item =roll_loot (2.0 )
                self .player .add_item (item )
                self .ui .tprint (c (f"  + {item }",Color .BRIGHT_GREEN ))
            money =random .randint (200 ,800 )
            self .player .money +=money 
            self .ui .tprint (c (f"  + {money } ienes",Color .BRIGHT_YELLOW ))

        self .ui .pause ()

    def room_menu (self ,room ):

        if self .player_died or self .completed or self .escaped :
            return 

        cur =self .current_room 

        options =[]

        if self .completed :
            options .append ("Sair da masmorra")

        if cur <self .size -1 :
            options .append ("Avancar para proxima sala (Leste)")
        if cur >0 :
            options .append ("Voltar para sala anterior (Oeste)")

        options .append ("Ver Status")
        options .append ("Ver Inventario")
        options .append ("Usar Item")
        if self .player .sukuna_fingers_in_inventory >0 :
            options .append ("Comer Dedo de Sukuna")
        if self .player .has_item ("Selo de CE Basico")or self .player .has_item ("Selo de CE Avancado"):
            options .append ("Usar Selo de CE")
        if self .player .has_item ("Selo de Cura"):
            options .append ("Usar Selo de Cura")
        options .append ("Fugir da masmorra")

        idx =self .ui .arrow_menu (options ,title =f"Sala {cur +1 }/{self .size } - O que fazer?")
        if idx <0 :
            return 

        action =options [idx ]

        if action =="Avancar para proxima sala (Leste)":
            self .current_room =min (self .size -1 ,self .current_room +1 )
        elif action =="Voltar para sala anterior (Oeste)":
            self .current_room =max (0 ,self .current_room -1 )
        elif action =="Sair da masmorra"or action =="Fugir da masmorra":
            self .escaped =True 
        elif action =="Ver Status":
            self .player .display_status (ui_module =self .ui )
        elif action =="Ver Inventario":
            self .show_inventory ()
        elif action =="Usar Item":
            self .use_item_menu ()
        elif action =="Comer Dedo de Sukuna":
            result =self .player .eat_sukuna_finger (ui_module =self .ui )
            if result in ("death","transformed"):
                self .player_died =True 
            self .ui .pause ()
        elif action =="Usar Selo de CE":
            if self .player .has_item ("Selo de CE Avancado"):
                self .player .use_consumable ("Selo de CE Avancado",ui_module =self .ui )
            else :
                self .player .use_consumable ("Selo de CE Basico",ui_module =self .ui )
            self .ui .pause ()
        elif action =="Usar Selo de Cura":
            self .player .use_consumable ("Selo de Cura",ui_module =self .ui )
            self .ui .pause ()

    def show_inventory (self ):

        from items import RARITY_COLORS
        self .ui .screen_header (self .ui .ASCII_INVENTORY ,"INVENTARIO",color =Color .BRIGHT_GREEN )
        if not self .player .inventory :
            self .ui .tprint (c ("Vazio.",Color .DIM ))
        else :
            for item_name ,qty in self .player .inventory .items ():
                item =ITEMS_DB .get (item_name ,{})
                rarity =item .get ("rarity","comum")
                color_name =RARITY_COLORS .get (rarity ,"WHITE")
                rarity_color =getattr (Color ,color_name ,Color .WHITE )
                print (f"  {c (item_name ,rarity_color )} x{qty }")
        print ()
        print (c (f"Dinheiro: {self .player .money } ienes",Color .BRIGHT_YELLOW ))
        if self .player .sukuna_fingers_in_inventory >0 :
            print (c (f"Dedos de Sukuna: {self .player .sukuna_fingers_in_inventory }",Color .BRIGHT_RED +Color .BOLD ))
        cursed =self .player .get_items_by_type ("amaldicoado")
        if cursed :
            print (c (f"Itens Amaldicoados: {sum (cursed .values ())}",Color .BRIGHT_MAGENTA ))
        self .ui .pause ()

    def use_item_menu (self ):

        consumables =self .player .get_items_by_type ("consumivel")
        if not consumables :
            self .ui .tprint (c ("Voce nao tem consumiveis.",Color .YELLOW ))
            self .ui .pause ()
            return 
        opts =list (consumables .keys ())+["Voltar"]
        idx =self .ui .arrow_menu (opts ,title ="Usar:")
        if idx <0 or idx ==len (opts )-1 :
            return 
        self .player .use_consumable (opts [idx ],ui_module =self .ui )
        self .ui .pause ()
