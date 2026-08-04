
import os 
import sys 
import random 
import time 

sys .path .insert (0 ,os .path .dirname (os .path .abspath (__file__ )))
for _sub in ("data","systems","interface"):
    sys .path .insert (0 ,os .path .join (os .path .dirname (os .path .abspath (__file__ )),_sub ))

import config 
from config import CONFIG ,check_admin_privileges 
import ui 
from ui import Color ,c 
import keyboard_input 
from auto_updater import updater 
from player import Player 
from techniques import (roulette_innate_technique ,roulette_birth_trait ,
TECHNIQUE_ROULETTE_COST ,TRAIT_ROULETTE_COST )
from items import ITEMS_DB ,SHOP_CATEGORIES 
from save_system import (show_load_menu ,show_save_menu ,save_game ,
quicksave )
from missions import show_mission_board ,check_story_missions 
from events import trigger_random_event 
from mentors import show_mentor_menu 

def setup_terminal ():

    ui .clear_screen ()

    try :
        sys .stdout .reconfigure (encoding ="utf-8")
    except (AttributeError ,IOError ):
        pass 

def show_admin_warning (ui_module ):

    if not CONFIG .admin_mode :
        ui_module .tprint (c ("\n[AVISO] O jogo NAO esta rodando com privilegios de administrador.",
        Color .YELLOW ))
        ui_module .tprint (c ("Alguns recursos podem estar limitados (acesso a pastas protegidas).",
        Color .DIM ))
        ui_module .tprint (c ("Para elevar privilegios:",Color .DIM ))
        if os .name =="nt":
            ui_module .tprint (c ("  Execute como Administrador (clique direito > Executar como admin).",
            Color .DIM ))
        else :
            ui_module .tprint (c ("  Rode com sudo (sudo python main.py).",Color .DIM ))
        ui_module .tprint (c ("\nO jogo funcionara normalmente, apenas com recursos limitados.\n",
        Color .DIM ))

def show_settings (ui_module ):

    while True :
        ui_module .clear_screen ()
        ui_module .title_box ("  CONFIGURACOES  ")

        print (c ("\n  Configuracoes atuais:",Color .BRIGHT_CYAN ))
        print (f"    Text Speed: {c (CONFIG .text_speed ,Color .BRIGHT_YELLOW )}")
        print (f"    Difficulty: {c (CONFIG .difficulty ,Color .BRIGHT_YELLOW )}")
        print (f"    ASCII Art: {c ('ON'if CONFIG .ascii_art else 'OFF',Color .BRIGHT_YELLOW )}")
        print (f"    Color: {c ('ON'if CONFIG .color_enabled else 'OFF',Color .BRIGHT_YELLOW )}")
        print (f"    Auto Save: {c ('ON'if CONFIG .auto_save else 'OFF',Color .BRIGHT_YELLOW )}")
        print (f"    Auto Update: {c ('ON'if CONFIG .auto_update else 'OFF',Color .BRIGHT_YELLOW )}")
        print (f"    Admin Mode: {c ('YES'if CONFIG .admin_mode else 'NO',Color .BRIGHT_YELLOW +Color .BOLD )}")
        if not CONFIG .admin_mode :
            print (c ("    (Sem admin: pasta de saves e local)",Color .DIM ))
        print ()

        options =[
        f"Text Speed: {CONFIG .text_speed }",
        f"Difficulty: {CONFIG .difficulty }",
        f"ASCII Art: {'ON'if CONFIG .ascii_art else 'OFF'}",
        f"Color: {'ON'if CONFIG .color_enabled else 'OFF'}",
        f"Auto Save: {'ON'if CONFIG .auto_save else 'OFF'}",
        f"Auto Update: {'ON'if CONFIG .auto_update else 'OFF'}",
        "Verificar Atualizacao Agora",
        f"Modo de Input: {c ('MOBILE (numeros)'if CONFIG .is_mobile ()else 'PC (setas)',Color .BRIGHT_CYAN )}",
        "Voltar",
        ]
        idx =ui_module .arrow_menu (options ,title ="Ajustar:")
        if idx <0 or idx ==len (options )-1 :
            return 

        if idx ==0 :
            speeds =list (config .TEXT_SPEEDS .keys ())
            new_idx =ui_module .arrow_menu (speeds ,title =f"Text Speed (atual: {CONFIG .text_speed }):")
            if new_idx >=0 :
                CONFIG .text_speed =speeds [new_idx ]
                ui_module .tprint (c (f"Text Speed: {CONFIG .text_speed }",Color .BRIGHT_GREEN ))
                ui_module .pause ()
        elif idx ==1 :
            diffs =list (config .DIFFICULTY_MODS .keys ())
            new_idx =ui_module .arrow_menu (diffs ,title =f"Difficulty (atual: {CONFIG .difficulty }):")
            if new_idx >=0 :
                CONFIG .difficulty =diffs [new_idx ]
                if CONFIG .difficulty =="Selo de Dedo":
                    ui_module .tprint (c ("\n!! SELO DE DEDO - PERMADEATH !!",Color .BRIGHT_RED +Color .BOLD ))
                    ui_module .tprint (c ("Se morrer, o save sera apagado.",Color .RED ))
                    if not ui_module .confirm ("Continuar com Permadeath?",default_yes =False ):
                        CONFIG .difficulty ="Normal"
                ui_module .tprint (c (f"Difficulty: {CONFIG .difficulty }",Color .BRIGHT_GREEN ))
                ui_module .pause ()
        elif idx ==2 :
            CONFIG .ascii_art =not CONFIG .ascii_art 
        elif idx ==3 :
            CONFIG .color_enabled =not CONFIG .color_enabled 
        elif idx ==4 :
            CONFIG .auto_save =not CONFIG .auto_save 
        elif idx ==5 :
            CONFIG .auto_update =not CONFIG .auto_update 
        elif idx ==6 :
            ui_module .clear_screen ()
            ui_module .tprint (c ("\nVerificando atualizacoes...",Color .BRIGHT_CYAN ))
            if updater .check_and_update (force =True ,silent =False ):
                sys .exit (0 )
            ui_module .pause ()
        elif idx ==7 :
            from mobile import select_input_mode 
            select_input_mode (ui_module =ui_module )

        CONFIG .save ()

def main_menu ():

    setup_terminal ()
    CONFIG .admin_mode =check_admin_privileges ()

    if not hasattr (main_menu ,"_input_mode_asked"):
        from mobile import select_input_mode 
        select_input_mode (ui_module =ui )
        main_menu ._input_mode_asked =True 

    ui .banner ()
    show_admin_warning (ui )
    ui .pause ()

    while True :
        ui .clear_screen ()
        ui .banner ()
        print ()

        options =["Continue","New Game","Settings","Sair"]
        idx =ui .arrow_menu (options ,title ="JUJUTSU TEXTSEN")

        if idx <0 or idx ==3 :

            ui .clear_screen ()
            ui .tprint (c ("Obrigado por jogar JJTS!",Color .BRIGHT_CYAN ))
            ui .tprint (c ("A maldicao do terminal acaba... por agora.",Color .DIM ))
            time .sleep (1 )
            return 
        elif idx ==0 :

            player =show_load_menu (ui )
            if player :
                game_loop (player )
        elif idx ==1 :

            player =new_game ()
            if player :
                game_loop (player )
        elif idx ==2 :

            show_settings (ui )

def new_game ():

    ui .clear_screen ()
    ui .title_box ("  NEW GAME - DESPERTAR  ")

    ui .tprint (c ("\nBem-vindo, jovem feiticeiro.",Color .BRIGHT_CYAN ))
    ui .tprint (c ("Antes de despertar seu poder amaldicoado, diga seu nome.",Color .DIM ))
    ui .tprint (c ("\n(Digite seu nome e pressione ENTER)",Color .DIM ))

    name =input (c ("\n> ",Color .BRIGHT_YELLOW )).strip ()
    if not name :
        name ="Despertado"

    player =Player (name )

    ui .clear_screen ()
    ui .title_box ("  AWAKENING SEQUENCE  ")
    ui .tprint (c ("\nA energia amaldicoada dentro de voce finalmente desperta...",Color .BRIGHT_MAGENTA ))
    ui .tprint (c ("Sera que voce nasceu com uma tecnica inata? Um traco especial?",Color .DIM ))
    ui .tprint (c ("Ou talvez... uma Restricao Celestial?",Color .DIM ))
    ui .pause ()

    player .generate_character (ui_module =ui )

    ui .clear_screen ()
    ui .title_box ("  A ESCOLA JUJUTSU  ")
    ui .tprint (c ("\nVoce chega a Tokyo Jujutsu High, a escola de feiticeiros.",Color .BRIGHT_CYAN ))
    ui .tprint (c ("O Diretor Yaga te recebe na entrada.",Color .DIM ))
    ui .tprint (c ("\nYaga: 'Bem-vindo. Voce agora eh um feiticeiro de Jujutsu.'",Color .YELLOW ))
    ui .tprint (c ("Yaga: 'Sua missao eh proteger os civis das maldicoes.'",Color .YELLOW ))
    ui .tprint (c ("Yaga: 'Va ao quadro de missoes quando estiver pronto.'",Color .YELLOW ))
    ui .pause ()

    player .add_item ("Convite da Escola Jujutsu")
    player .add_item ("Selo de CE Basico",3 )
    player .add_item ("Selo de Cura",2 )

    success ,_ =save_game (player ,name .replace (" ","_"))
    if success :
        ui .tprint (c (f"\n[Jogo salvo: {name }]",Color .DIM ))
    ui .pause ()

    return player 

def game_loop (player ):

    while True :
        if player .is_dead ():

            ui .tprint (c ("\nVoce morreu.",Color .BRIGHT_RED ))
            ui .pause ()
            return 

        check_story_missions (player ,ui )

        if player .sukuna_control_pct >=100 :
            ui .clear_screen ()
            ui .tprint (c ("Sukuna assumiu controle total do seu corpo.",Color .BRIGHT_RED +Color .BOLD +Color .BLINK ))
            ui .tprint (c ("GAME OVER.",Color .RED ))
            ui .pause ()
            return 

        ui .clear_screen ()
        ui .screen_header (ui .ASCII_SCHOOL ,f"ESCOLA JUJUTSU - {player .name }",color =Color .BRIGHT_CYAN )
        print ()
        show_player_brief (player )
        print ()

        options =[
        "Quadro de Missoes",
        "Treinar com Mentores",
        "Loja da Escola",
        "Inventario & Equipamentos",
        "Ver Status",
        "Distribuir Atributos",
        "Descansar (400 ienes - full HP/CE)",
        "Comer Dedo de Sukuna"+(f" ({player .sukuna_fingers_in_inventory })"if player .sukuna_fingers_in_inventory else ""),
        "Save Game",
        "Configuracoes",
        "Sair para o Menu",
        ]

        idx =ui .arrow_menu (options ,title ="O que fazer?")
        if idx <0 or idx ==len (options )-1 :

            if ui .confirm ("Salvar antes de sair?",default_yes =True ):
                show_save_menu (player ,ui )
            return 

        action =options [idx ]

        if action =="Quadro de Missoes":
            show_mission_board (player ,ui )
            if player .is_dead ():
                return 
            if random .random ()<0.4 :
                trigger_random_event (player ,ui )
            if player .is_dead ():
                return 
            if CONFIG .auto_save :
                quicksave (player ,ui )

        elif action =="Treinar com Mentores":
            show_mentor_menu (player ,ui )

        elif action =="Loja da Escola":
            school_shop (player ,ui )

        elif action =="Inventario & Equipamentos":
            result =inventory_menu (player ,ui )
            if result =="game_over":
                return 

        elif action =="Ver Status":
            player .display_status (ui_module =ui )

        elif action =="Distribuir Atributos":
            distribute_attributes (player ,ui )

        elif action .startswith ("Descansar"):
            rest_at_school (player ,ui )

        elif action .startswith ("Comer Dedo de Sukuna"):
            if player .sukuna_fingers_in_inventory >0 :
                ui .tprint (c ("\n!! COMER DEDO DE SUKUNA !!",Color .BRIGHT_RED +Color .BOLD ))
                ui .tprint (c ("Risco de morte, transformacao, ou poder.",Color .YELLOW ))
                if ui .confirm ("Continuar com risco extremo?",default_yes =False ):
                    result =player .eat_sukuna_finger (ui_module =ui )
                    if result in ("death","transformed"):
                        ui .tprint (c ("\nGAME OVER.",Color .RED ))
                        ui .pause ()
                        return 
            else :
                ui .tprint (c ("\nVoce nao tem dedos de Sukuna.",Color .YELLOW ))
                ui .pause ()

        elif action =="Save Game":
            show_save_menu (player ,ui )

        elif action =="Configuracoes":
            show_settings (ui )

def rest_at_school (player ,ui_module ):

    REST_COST =400 

    ui_module .clear_screen ()
    ui_module .title_box ("  DESCANSAR NA ESCOLA  ")

    print (c (f"\n  Dinheiro atual: {player .money } ienes",Color .BRIGHT_YELLOW ))
    print (c (f"  Custo do descanso: {REST_COST } ienes",Color .BRIGHT_CYAN ))
    print ()
    print (c ("  HP atual: ",Color .WHITE )+ui_module .hp_bar (player .hp ,player .max_hp ,length =25 ))
    print (c ("  CE atual: ",Color .WHITE )+ui_module .ce_bar (player .ce_current ,player .max_ce ,length =25 ))
    print ()
    print (c ("  Descansar recupera 100% do HP e CE.",Color .DIM ))
    print (c ("  Nao cura debuffs permanentes nem remove dedos de Sukuna.",Color .DIM ))
    print ()

    if player .hp >=player .max_hp and player .ce_current >=player .max_ce :
        print (c ("  Voce ja esta com HP e CE cheios. Nao precisa descansar.",Color .YELLOW ))
        ui_module .pause ()
        return 

    if player .money <REST_COST :
        print (c (f"  Dinheiro insuficiente! Faltam {REST_COST -player .money } ienes.",Color .RED ))
        ui_module .pause ()
        return 

    if not ui_module .confirm (f"Pagar {REST_COST } ienes para descansar?",default_yes =True ):
        return 

    player .money -=REST_COST 
    player .hp =player .max_hp 
    player .ce_current =player .max_ce 
    player .stamina =player .max_stamina 

    print ()
    print (c ("  Voce descansa nos dormitorios da escola.",Color .BRIGHT_CYAN ))
    print (c ("  Zzz...",Color .DIM ))
    ui_module .pause ()
    print ()
    print (c ("  Voce acorda revitalizado!",Color .BRIGHT_GREEN ))
    print (c ("  HP: ",Color .WHITE )+ui_module .hp_bar (player .hp ,player .max_hp ,length =25 ))
    print (c ("  CE: ",Color .WHITE )+ui_module .ce_bar (player .ce_current ,player .max_ce ,length =25 ))
    print (c (f"  -{REST_COST } ienes (saldo: {player .money })",Color .YELLOW ))
    ui_module .pause ()

def show_player_brief (player ):
    print (c ("  Level: ",Color .WHITE )+c (f"{player .level_system .level }",Color .BRIGHT_YELLOW )+
    c ("  |  Rank: ",Color .WHITE )+c (f"{player .rank_system .full_rank_name ()}",Color .BRIGHT_MAGENTA )+
    c ("  |  Karma: ",Color .WHITE )+c (f"{player .karma .karma } ({player .karma .get_alinhamento ()})",Color .BRIGHT_CYAN ))
    print (c ("  HP: ",Color .WHITE )+ui .hp_bar (player .hp ,player .max_hp ,length =30 ))
    print (c ("  CE: ",Color .WHITE )+ui .ce_bar (player .ce_current ,player .max_ce ,length =30 ))
    xp_now =player .level_system .xp 
    xp_next =player .level_system .xp_to_next_level ()
    print (c ("  XP: ",Color .WHITE )+ui .xp_bar (xp_now ,xp_next ,length =30 ))
    if player .has_technique_evolution ():
        tech_xp_now =player .technique_xp 
        tech_xp_next =player .xp_to_next_technique_level ()
        stage_label =player .get_technique_stage_label ()
        print (c ("  Tecnica: ",Color .WHITE )+c (f"{stage_label } (Lv.{player .technique_level })",Color .BRIGHT_MAGENTA ))
        print (c ("  XP Tecnica: ",Color .WHITE )+ui .xp_bar (tech_xp_now ,tech_xp_next ,length =30 ))
    if player .sukuna_fingers_eaten >0 :
        print (c (f"  Dedos ingeridos: {player .sukuna_fingers_eaten } | Controle Sukuna: {player .sukuna_control_pct }%",
        Color .BRIGHT_RED ))
    if player .sukuna_mastered :
        print (c ("  >> Sukuna despertou! Use 'Cleave and Dismantle' em batalha. <<",Color .BRIGHT_RED +Color .BOLD ))
    if player .level_system .attribute_points >0 :
        print (c (f"  >> {player .level_system .attribute_points } pontos de atributo disponiveis! <<",
        Color .BRIGHT_YELLOW +Color .BOLD ))

def school_shop (player ,ui_module ):
    while True :
        ui_module .clear_screen ()
        ui_module .screen_header (ui_module .ASCII_SHOP ,"LOJA DA ESCOLA",color =Color .BRIGHT_YELLOW )
        print (c (f"\n  Seu dinheiro: {player .money } ienes\n",Color .BRIGHT_YELLOW ))

        cat_labels =[label for label ,_ in SHOP_CATEGORIES ]
        cat_labels .append ("Vender Itens")
        cat_labels .append ("Roleta de Tecnica (6000 ienes)")
        cat_labels .append ("Roleta de Traco (3800 ienes)")
        cat_labels .append ("Voltar")

        idx =ui_module .arrow_menu (cat_labels ,title ="Categorias:")
        if idx <0 or idx ==len (cat_labels )-1 :
            return 

        if idx ==len (SHOP_CATEGORIES ):
            sell_menu (player ,ui_module )
            continue 
        if idx ==len (SHOP_CATEGORIES )+1 :
            roulette_menu (player ,ui_module ,kind ="technique")
            continue 
        if idx ==len (SHOP_CATEGORIES )+2 :
            roulette_menu (player ,ui_module ,kind ="trait")
            continue 

        cat_label ,cat_type =SHOP_CATEGORIES [idx ]
        category_shop (player ,ui_module ,cat_label ,cat_type )

def category_shop (player ,ui_module ,cat_label ,cat_type ):
    items_in_cat ={name :data for name ,data in ITEMS_DB .items ()
    if data ["type"]==cat_type and data .get ("price",0 )>0 }
    if not items_in_cat :
        ui_module .tprint (c (f"\nNenhum item em {cat_label }.",Color .YELLOW ))
        ui_module .pause ()
        return 

    while True :
        ui_module .clear_screen ()
        ui_module .title_box (f"  LOJA - {cat_label .upper ()}  ")
        print (c (f"\n  Seu dinheiro: {player .money } ienes\n",Color .BRIGHT_YELLOW ))

        item_names =list (items_in_cat .keys ())
        labels =[]
        for name in item_names :
            item =items_in_cat [name ]
            can_buy =player .money >=item ["price"]
            prefix =""if can_buy else c ("[SEM $] ",Color .RED )
            owned =player .inventory .get (name ,0 )
            owned_str =f" (tem: {owned })"if owned >0 else ""
            labels .append (f"{prefix }{name } - {item ['price']} ienes ({item ['rarity']}){owned_str }")
        labels .append ("Voltar")

        idx =ui_module .arrow_menu (labels ,title ="Comprar:")
        if idx <0 or idx ==len (labels )-1 :
            return 

        item_name =item_names [idx ]
        item =items_in_cat [item_name ]
        if player .money <item ["price"]:
            ui_module .tprint (c ("Dinheiro insuficiente!",Color .RED ))
            ui_module .pause ()
            continue 

        qty =ask_purchase_quantity (player ,item ,ui_module )
        if qty <=0 :
            continue 

        total_cost =item ["price"]*qty 
        if player .money <total_cost :
            ui_module .tprint (c (f"\nDinheiro insuficiente para {qty }x! Precisa {total_cost }.",Color .RED ))
            ui_module .pause ()
            continue 

        if not ui_module .confirm (f"Comprar {qty }x {item_name } por {total_cost } ienes?",default_yes =True ):
            continue 

        player .money -=total_cost 
        player .add_item (item_name ,qty )
        ui_module .tprint (c (f"\nComprou {qty }x {item_name } por {total_cost } ienes!",Color .BRIGHT_GREEN ))
        ui_module .pause ()

def ask_purchase_quantity (player ,item ,ui_module ):
    price =item ["price"]
    max_affordable =player .money //price if price >0 else 999 
    if max_affordable <=0 :
        return 0 
    options =[f"Comprar 1 ({price } ienes)"]
    if max_affordable >=5 :
        options .append (f"Comprar 5 ({price *5 } ienes)")
    if max_affordable >=10 :
        options .append (f"Comprar 10 ({price *10 } ienes)")
    options .append (f"Comprar maximo possivel ({max_affordable }x = {price *max_affordable } ienes)")
    options .append ("Quantidade customizada")
    options .append ("Voltar")
    idx =ui_module .arrow_menu (options ,title ="Quantidade:")
    if idx <0 or idx ==len (options )-1 :
        return 0 
    if idx ==0 :
        return 1 
    if idx ==1 and max_affordable >=5 :
        return min (5 ,max_affordable )
    if idx ==2 and max_affordable >=10 :
        return min (10 ,max_affordable )
    if (idx ==3 )or (idx ==2 and max_affordable <10 and max_affordable >=5 )or (idx ==1 and max_affordable <5 ):
        if "maximo"in options [idx ].lower ():
            return max_affordable 
        if "customizada"in options [idx ].lower ():
            return _ask_custom_buy_quantity (max_affordable ,ui_module )
    if "maximo"in options [idx ].lower ():
        return max_affordable 
    if "customizada"in options [idx ].lower ():
        return _ask_custom_buy_quantity (max_affordable ,ui_module )
    return 1 

def _ask_custom_buy_quantity (max_qty ,ui_module ):
    ui_module .tprint (c (f"\n  Digite a quantidade (1 a {max_qty }):",Color .BRIGHT_YELLOW ))
    try :
        choice =input (c ("  > ",Color .BRIGHT_YELLOW )).strip ()
        if not choice .isdigit ():
            ui_module .tprint (c ("  Quantidade invalida.",Color .RED ))
            ui_module .pause ()
            return 0 
        qty =int (choice )
        if qty <1 or qty >max_qty :
            ui_module .tprint (c (f"  Quantidade deve ser entre 1 e {max_qty }.",Color .RED ))
            ui_module .pause ()
            return 0 
        return qty 
    except (EOFError ,KeyboardInterrupt ):
        return 0 

def roulette_menu (player ,ui_module ,kind ="technique"):
    ui_module .clear_screen ()
    if kind =="technique":
        ui_module .title_box ("  ROLETA DE TECNICA INATA  ")
        cost =TECHNIQUE_ROULETTE_COST 
        current =player .innate_technique 
        ui_module .tprint (c (f"\n  Tecnica atual: {current }",Color .BRIGHT_MAGENTA ))
        ui_module .tprint (c (f"  Custo: {cost } ienes",Color .BRIGHT_CYAN ))
        ui_module .tprint (c (f"  Seu dinheiro: {player .money } ienes",Color .BRIGHT_YELLOW ))
        ui_module .tprint (c ("\n  A tecnica atual sera TROCADA por uma nova sorteada.",Color .DIM ))
        ui_module .tprint (c ("  Pesos iguais ao sorteio inicial do jogo.",Color .DIM ))
        print ()
        if not ui_module .confirm ("Rerolar tecnica inata?"):
            return 
        roulette_innate_technique (player ,ui_module =ui_module )
    else :
        ui_module .title_box ("  ROLETA DE TRACO DE NASCIMENTO  ")
        cost =TRAIT_ROULETTE_COST 
        current =player .birth_trait 
        ui_module .tprint (c (f"\n  Traco atual: {current }",Color .BRIGHT_BLUE ))
        ui_module .tprint (c (f"  Custo: {cost } ienes",Color .BRIGHT_CYAN ))
        ui_module .tprint (c (f"  Seu dinheiro: {player .money } ienes",Color .BRIGHT_YELLOW ))
        ui_module .tprint (c ("\n  O traco atual sera TROCADO por um novo sorteado.",Color .DIM ))
        print ()
        if not ui_module .confirm ("Rerolar traco de nascimento?"):
            return 
        roulette_birth_trait (player ,ui_module =ui_module )

def sell_menu (player ,ui_module ):

    while True :
        sellable_items =[n for n in player .inventory .keys ()
        if ITEMS_DB .get (n ,{}).get ("price",0 )>0 ]
        if not sellable_items :
            ui_module .tprint (c ("Voce nao tem itens vendaveis no inventario.",Color .YELLOW ))
            ui_module .pause ()
            return 

        ui_module .clear_screen ()
        ui_module .title_box ("  VENDER ITENS  ")
        print (c (f"\n  Dinheiro atual: {player .money } ienes",Color .BRIGHT_YELLOW ))
        print ()

        labels =[]
        items =sellable_items 
        for name in items :
            item =ITEMS_DB .get (name ,{})
            sell_price =max (5 ,item .get ("price",0 )//2 )
            qty =player .inventory [name ]
            total_value =sell_price *qty 
            labels .append (f"{name } ({qty }x) - {sell_price } ienes/un. (total: {total_value })")
        labels .append ("Voltar")

        idx =ui_module .arrow_menu (labels ,title ="Vender:")
        if idx <0 or idx ==len (items ):
            return 

        item_name =items [idx ]
        item =ITEMS_DB .get (item_name ,{})
        sell_price =max (5 ,item .get ("price",0 )//2 )
        qty_owned =player .inventory [item_name ]

        ui_module .clear_screen ()
        ui_module .title_box (f"  VENDER {item_name .upper ()}  ")
        print (c (f"\n  Voce tem: {qty_owned }x {item_name }",Color .BRIGHT_WHITE ))
        print (c (f"  Preco unitario: {sell_price } ienes",Color .BRIGHT_CYAN ))
        print (c (f"  Valor maximo ({qty_owned }x): {sell_price *qty_owned } ienes",Color .BRIGHT_YELLOW ))
        print ()
        print (c ("  Escolha a quantidade:",Color .BRIGHT_CYAN ))

        qty_options =[]
        if qty_owned >=5 :
            qty_options .append (f"Vender 1 ({sell_price } ienes)")
            qty_options .append (f"Vender 5 ({sell_price *5 } ienes)")
            if qty_owned >=10 :
                qty_options .append (f"Vender 10 ({sell_price *10 } ienes)")
            qty_options .append (f"Vender TODOS ({qty_owned }x = {sell_price *qty_owned } ienes)")
            qty_options .append ("Vender quantidade customizada")
        elif qty_owned >=2 :
            qty_options .append (f"Vender 1 ({sell_price } ienes)")
            qty_options .append (f"Vender TODOS ({qty_owned }x = {sell_price *qty_owned } ienes)")
            qty_options .append ("Vender quantidade customizada")
        else :
            qty_options .append (f"Vender 1 ({sell_price } ienes)")
        qty_options .append ("Voltar")

        q_idx =ui_module .arrow_menu (qty_options ,title ="Quantidade:")
        if q_idx <0 or q_idx ==len (qty_options )-1 :
            continue 

        if qty_owned >=5 :
            if q_idx ==0 :
                qty_to_sell =1 
            elif q_idx ==1 :
                qty_to_sell =min (5 ,qty_owned )
            elif q_idx ==2 and qty_owned >=10 :
                qty_to_sell =min (10 ,qty_owned )
            elif (q_idx ==3 and qty_owned >=10 )or (q_idx ==2 and qty_owned <10 and qty_owned >=5 ):
                qty_to_sell =qty_owned 
            elif (q_idx ==4 and qty_owned >=10 )or (q_idx ==3 and qty_owned <10 ):

                qty_to_sell =_ask_custom_quantity (qty_owned ,ui_module )
                if qty_to_sell <=0 :
                    continue 
            else :
                qty_to_sell =qty_owned 
        elif qty_owned >=2 :
            if q_idx ==0 :
                qty_to_sell =1 
            elif q_idx ==1 :
                qty_to_sell =qty_owned 
            elif q_idx ==2 :
                qty_to_sell =_ask_custom_quantity (qty_owned ,ui_module )
                if qty_to_sell <=0 :
                    continue 
            else :
                qty_to_sell =1 
        else :
            qty_to_sell =1 

        total =sell_price *qty_to_sell 
        if not ui_module .confirm (f"Vender {qty_to_sell }x {item_name } por {total } ienes?"):
            continue 

        for _ in range (qty_to_sell ):
            player .remove_item (item_name )
        player .money +=total 
        ui_module .tprint (c (f"\nVendeu {qty_to_sell }x {item_name } por {total } ienes!",
        Color .BRIGHT_GREEN +Color .BOLD ))
        ui_module .pause ()

def _ask_custom_quantity (max_qty ,ui_module ):

    ui_module .tprint (c (f"\n  Digite a quantidade (1 a {max_qty }):",Color .BRIGHT_YELLOW ))
    try :
        choice =input (c ("  > ",Color .BRIGHT_YELLOW )).strip ()
        if not choice .isdigit ():
            ui_module .tprint (c ("  Quantidade invalida.",Color .RED ))
            ui_module .pause ()
            return 0 
        qty =int (choice )
        if qty <1 or qty >max_qty :
            ui_module .tprint (c (f"  Quantidade deve ser entre 1 e {max_qty }.",Color .RED ))
            ui_module .pause ()
            return 0 
        return qty 
    except (EOFError ,KeyboardInterrupt ):
        return 0 

def inventory_menu (player ,ui_module ):
    while True :
        ui_module .clear_screen ()
        ui_module .screen_header (ui_module .ASCII_INVENTORY ,"INVENTARIO",color =Color .BRIGHT_GREEN )
        status_lines =[f"Dinheiro: {player .money } ienes"]
        if player .sukuna_fingers_in_inventory >0 :
            status_lines .append (f"Dedos de Sukuna: {player .sukuna_fingers_in_inventory }")
        cursed_items =player .get_items_by_type ("amaldicoado")
        if cursed_items :
            status_lines .append (f"Itens Amaldicoados: {sum (cursed_items .values ())}")
        if player .auto_sell_list :
            status_lines .append (f"Auto-Sell ativo: {len (player .auto_sell_list )} item(s)")
        ui_module .section ("Resumo",status_lines ,color =Color .BRIGHT_GREEN )
        print ()

        if not player .inventory :
            ui_module .tprint (c ("Inventario vazio.",Color .DIM ))
            ui_module .pause ()
            return None 

        options =[
        "Equipar Arma",
        "Equipar Amuleto (5 slots)",
        "Usar Item (consumivel/amaldicoado)",
        "Ver Detalhes de Item",
        "Configurar Auto-Sell",
        "Voltar",
        ]
        idx =ui_module .arrow_menu (options ,title ="Acao:")
        if idx <0 or idx ==len (options )-1 :
            return None 

        if idx ==0 :
            equip_menu (player ,"arma",ui_module )
        elif idx ==1 :
            equip_amulet_menu (player ,ui_module )
        elif idx ==2 :
            result =use_consumable_menu (player ,ui_module )
            if result =="game_over":
                return "game_over"
        elif idx ==3 :
            view_item_details (player ,ui_module )
        elif idx ==4 :
            auto_sell_menu (player ,ui_module )

def equip_menu (player ,slot ,ui_module ):
    items =player .get_items_by_type (slot )
    if not items :
        ui_module .tprint (c (f"\nVoce nao tem {slot }s.",Color .YELLOW ))
        ui_module .pause ()
        return 

    labels =list (items .keys ())
    if player .equipped .get ("arma"):
        labels .append (f"Remover {player .equipped ['arma']}")
    labels .append ("Voltar")

    idx =ui_module .arrow_menu (labels ,title =f"Equipar {slot }:")
    if idx <0 or idx ==len (labels )-1 :
        return 

    if idx ==len (items ):
        player .equipped ["arma"]=None 
        ui_module .tprint (c ("Item removido.",Color .DIM ))
    else :
        item_name =list (items .keys ())[idx ]
        player .equipped ["arma"]=item_name 
        ui_module .tprint (c (f"\nEquipou: {item_name }",Color .BRIGHT_GREEN ))

    player .recalculate_derived ()
    ui_module .pause ()

def equip_amulet_menu (player ,ui_module ):
    items =player .get_items_by_type ("amuleto")
    if not items and not any (player .equipped .get ("amuletos",[])):
        ui_module .tprint (c ("\nVoce nao tem amuletos.",Color .YELLOW ))
        ui_module .pause ()
        return 

    while True :
        ui_module .clear_screen ()
        ui_module .title_box ("  EQUIPAR AMULETOS (5 SLOTS)  ")
        amuletos =player .equipped .get ("amuletos")or [None ]*5 
        print ()
        for i ,amul in enumerate (amuletos [:5 ],1 ):
            if amul :
                print (c (f"  Slot {i }: {amul }",Color .BRIGHT_GREEN ))
            else :
                print (c (f"  Slot {i }: (vazio)",Color .DIM ))
        print ()

        labels =[]
        for i ,amul in enumerate (amuletos [:5 ],1 ):
            if amul :
                labels .append (f"Trocar Slot {i } ({amul })")
            else :
                labels .append (f"Equipar no Slot {i } (vazio)")
        labels .append ("Remover todos")
        labels .append ("Voltar")

        idx =ui_module .arrow_menu (labels ,title ="Slot:")
        if idx <0 or idx ==len (labels )-1 :
            return 
        if idx ==5 :
            player .equipped ["amuletos"]=[None ,None ,None ,None ,None ]
            player .recalculate_derived ()
            ui_module .tprint (c ("Todos os amuletos removidos.",Color .DIM ))
            ui_module .pause ()
            continue 

        slot_idx =idx 
        available ={n :q for n ,q in items .items ()if n not in amuletos or n ==amuletos [slot_idx ]}
        if not available :
            ui_module .tprint (c ("\nVoce nao tem outros amuletos para equipar.",Color .YELLOW ))
            ui_module .pause ()
            continue 

        item_labels =list (available .keys ())
        if amuletos [slot_idx ]:
            item_labels .append (f"Remover {amuletos [slot_idx ]}")
        item_labels .append ("Voltar")
        s_idx =ui_module .arrow_menu (item_labels ,title =f"Slot {slot_idx +1 }:")
        if s_idx <0 or s_idx ==len (item_labels )-1 :
            continue 
        if s_idx ==len (available ):
            amuletos [slot_idx ]=None 
            ui_module .tprint (c ("Amuleto removido.",Color .DIM ))
        else :
            chosen =list (available .keys ())[s_idx ]
            if chosen in amuletos :
                old_idx =amuletos .index (chosen )
                amuletos [old_idx ]=amuletos [slot_idx ]
            amuletos [slot_idx ]=chosen 
            ui_module .tprint (c (f"\nEquipou: {chosen } no Slot {slot_idx +1 }",Color .BRIGHT_GREEN ))
        player .equipped ["amuletos"]=amuletos 
        player .recalculate_derived ()
        ui_module .pause ()

def auto_sell_menu (player ,ui_module ):

    while True :
        ui_module .clear_screen ()
        ui_module .title_box ("  CONFIGURAR AUTO-SELL  ")
        print (c ("\n  Itens marcados para Auto-Sell sao vendidos automaticamente",Color .DIM ))
        print (c ("  assim que voce os ganha em batalha/dungeon.",Color .DIM ))
        print (c ("  Voce define sua propria lista - sem presets.",Color .DIM ))
        print ()
        if player .auto_sell_list :
            print (c ("  Atualmente marcados:",Color .BRIGHT_CYAN ))
            for name in player .auto_sell_list :
                print (f"    - {name }")
        else :
            print (c ("  Nenhum item marcado.",Color .DIM ))
        print ()

        options =[
        "Adicionar item por nome (digite)",
        "Adicionar todos itens de uma raridade",
        "Adicionar todos itens de um tipo",
        "Remover item da lista",
        "Limpar lista",
        "Voltar",
        ]
        idx =ui_module .arrow_menu (options ,title ="Acao:")
        if idx <0 or idx ==5 :
            return 
        if idx ==0 :
            add_auto_sell_by_name (player ,ITEMS_DB ,ui_module )
        elif idx ==1 :
            add_auto_sell_by_rarity (player ,ITEMS_DB ,ui_module )
        elif idx ==2 :
            add_auto_sell_by_type (player ,ITEMS_DB ,ui_module )
        elif idx ==3 :
            if not player .auto_sell_list :
                ui_module .tprint (c ("\nLista vazia.",Color .YELLOW ))
                ui_module .pause ()
                continue 
            labels =list (player .auto_sell_list )+["Voltar"]
            s_idx =ui_module .arrow_menu (labels ,title ="Remover:")
            if s_idx <0 or s_idx ==len (labels )-1 :
                continue 
            chosen =player .auto_sell_list [s_idx ]
            player .auto_sell_list .remove (chosen )
            ui_module .tprint (c (f"\n{chosen } removido da Auto-Sell.",Color .DIM ))
            ui_module .pause ()
        elif idx ==4 :
            player .auto_sell_list .clear ()
            ui_module .tprint (c ("\nLista de Auto-Sell limpa.",Color .DIM ))
            ui_module .pause ()

def add_auto_sell_by_name (player ,items_db ,ui_module ):
    ui_module .clear_screen ()
    ui_module .title_box ("  ADICIONAR POR NOME  ")
    print (c ("\n  Digite o nome EXATO do item.",Color .DIM ))
    print (c ("  Use a opcao por raridade/tipo se nao souber o nome.",Color .DIM ))
    print ()
    try :
        name =input (c ("  Nome do item > ",Color .BRIGHT_YELLOW )).strip ()
    except (EOFError ,KeyboardInterrupt ):
        return 
    if not name :
        return 
    if name in player .auto_sell_list :
        ui_module .tprint (c (f"\n{name } ja esta na lista.",Color .YELLOW ))
        ui_module .pause ()
        return 
    if name not in items_db :
        ui_module .tprint (c (f"\nItem '{name }' nao existe no banco de itens.",Color .RED ))
        ui_module .tprint (c ("Verifique a ortografia ou use outra opcao.",Color .DIM ))
        ui_module .pause ()
        return 
    if items_db [name ].get ("price",0 )<=0 :
        ui_module .tprint (c (f"\n{name } eh um item de missao/especial e nao pode ser vendido.",Color .RED ))
        ui_module .pause ()
        return 
    player .auto_sell_list .append (name )
    ui_module .tprint (c (f"\n{name } adicionado a Auto-Sell.",Color .BRIGHT_GREEN ))
    ui_module .pause ()

def add_auto_sell_by_rarity (player ,items_db ,ui_module ):
    rarities =["comum","incomum","raro","epico","lendario"]
    options =[f"Adicionar TODOS itens raros: {r }"for r in rarities ]
    options .append ("Voltar")
    idx =ui_module .arrow_menu (options ,title ="Raridade:")
    if idx <0 or idx ==len (rarities ):
        return 
    chosen_rarity =rarities [idx ]
    added =0 
    for name ,data in items_db .items ():
        if data .get ("rarity")==chosen_rarity and name not in player .auto_sell_list :
            if data .get ("price",0 )>0 :
                player .auto_sell_list .append (name )
                added +=1 
    ui_module .tprint (c (f"\n{added } item(ns) raros '{chosen_rarity }' adicionados a Auto-Sell.",Color .BRIGHT_GREEN ))
    ui_module .pause ()

def add_auto_sell_by_type (player ,items_db ,ui_module ):

    options =[f"Adicionar TODOS itens do tipo: {label }"for label ,_ in SHOP_CATEGORIES ]
    options .append ("Voltar")
    idx =ui_module .arrow_menu (options ,title ="Tipo:")
    if idx <0 or idx ==len (SHOP_CATEGORIES ):
        return 
    chosen_type =SHOP_CATEGORIES [idx ][1 ]
    added =0 
    for name ,data in items_db .items ():
        if data .get ("type")==chosen_type and name not in player .auto_sell_list :
            if data .get ("price",0 )>0 :
                player .auto_sell_list .append (name )
                added +=1 
    ui_module .tprint (c (f"\n{added } item(ns) do tipo '{chosen_type }' adicionados a Auto-Sell.",Color .BRIGHT_GREEN ))
    ui_module .pause ()

def use_consumable_menu (player ,ui_module ):
    usable =player .get_usable_items ()
    if not usable :
        ui_module .tprint (c ("\nVoce nao tem itens usaveis.",Color .YELLOW ))
        ui_module .pause ()
        return None 

    labels =list (usable .keys ())+["Voltar"]
    idx =ui_module .arrow_menu (labels ,title ="Usar:")
    if idx <0 or idx ==len (labels )-1 :
        return None 

    item_name =list (usable .keys ())[idx ]

    item =ITEMS_DB .get (item_name ,{})
    if item .get ("type")=="amaldicoado":

        ui_module .tprint (c (f"\n!! {item_name } eh um item AMALDICOADO !!",Color .BRIGHT_MAGENTA +Color .BOLD ))
        ui_module .tprint (c (f"  {item .get ('desc','')}",Color .DIM ))
        if not ui_module .confirm ("Usar mesmo com os riscos?",default_yes =False ):
            return None 
        result =player .use_cursed_item (item_name ,ui_module =ui_module )
        if result =="transformed":
            ui_module .tprint (c ("\nGAME OVER.",Color .RED ))
            ui_module .pause ()
            return "game_over"
    else :
        player .use_consumable (item_name ,ui_module =ui_module )
    ui_module .pause ()
    return None 

def view_item_details (player ,ui_module ):

    if not player .inventory :
        return 
    labels =list (player .inventory .keys ())+["Voltar"]
    idx =ui_module .arrow_menu (labels ,title ="Ver detalhes:")
    if idx <0 or idx ==len (labels )-1 :
        return 
    item_name =list (player .inventory .keys ())[idx ]
    ui_module .clear_screen ()
    ui_module .title_box (f"  {item_name }  ")
    from items import get_item_info_string 
    info =get_item_info_string (item_name )
    print ()
    for line in info .split ("\n")[1 :]:
        print (f"  {line }")
    print (f"\n  Quantidade: {player .inventory [item_name ]}")
    ui_module .pause ()

def distribute_attributes (player ,ui_module ):
    if player .level_system .attribute_points <=0 and not player .auto_allocate_build :
        ui_module .tprint (c ("\nVoce nao tem pontos para distribuir.",Color .YELLOW ))
        ui_module .tprint (c ("Suba de level para ganhar mais pontos.",Color .DIM ))
        ui_module .pause ()
        return 

    attrs =list (player .attributes .keys ())
    attr_labels ={
    "forca":"Forca Fisica",
    "ce":"Energia Amaldicoada (CE)",
    "controle":"Controle de CE",
    "velocidade":"Velocidade",
    "vigor":"Vigor (HP)",
    "sorte":"Sorte",
    }

    while True :
        ui_module .clear_screen ()
        ui_module .title_box ("  DISTRIBUIR ATRIBUTOS  ")
        print (c (f"\n  Pontos disponiveis: {player .level_system .attribute_points }",Color .BRIGHT_YELLOW +Color .BOLD ))
        if player .auto_allocate_build :
            scheme_str =format_scheme (player .auto_allocate_build ,attr_labels )
            print (c (f"  Auto-Alocate ATIVO: {scheme_str }",Color .BRIGHT_CYAN ))
            print (c ("  (pontos serao distribuidos automaticamente ao upar de level)",Color .DIM ))
        print ()
        for attr in attrs :
            label =attr_labels .get (attr ,attr )
            value =player .attributes [attr ]
            print (f"    {label }: {value }")
        print ()

        if player .auto_allocate_build :
            build_label =f"Configurar Auto-Alocate: {format_scheme (player .auto_allocate_build ,attr_labels )}"
        else :
            build_label ="Configurar Auto-Alocate (desativado)"
        options =[f"+1 {attr_labels [a ]} (atual: {player .attributes [a ]})"for a in attrs ]
        options .append ("+5 em um atributo (gasta 5 pontos de uma vez)")
        options .append ("Aplicar Auto-Alocate agora (usa todos os pontos)")
        options .append (build_label )
        options .append ("Voltar")

        idx =ui_module .arrow_menu (options ,title ="Aumentar:")
        if idx <0 or idx ==len (options )-1 :
            return 

        if idx <len (attrs ):
            attr =attrs [idx ]
            if player .level_system .spend_point (attr ,player ):
                ui_module .tprint (c (f"\n+1 em {attr_labels [attr ]}!",Color .BRIGHT_GREEN ))
                ui_module .pause ()
            else :
                ui_module .tprint (c ("Erro ao gastar ponto.",Color .RED ))
                ui_module .pause ()
        elif idx ==len (attrs ):
            plus_five_attribute (player ,attrs ,attr_labels ,ui_module )
        elif idx ==len (attrs )+1 :
            apply_auto_allocate_now (player ,ui_module )
        elif idx ==len (attrs )+2 :
            configure_auto_allocate (player ,ui_module )

def format_scheme (scheme ,attr_labels ):
    if not scheme :
        return "desativado"
    parts =[]
    for attr ,weight in scheme .items ():
        label =attr_labels .get (attr ,attr )
        parts .append (f"{weight } {label }")
    return " / ".join (parts )

def plus_five_attribute (player ,attrs ,attr_labels ,ui_module ):
    if player .level_system .attribute_points <5 :
        ui_module .tprint (c ("\nVoce precisa de pelo menos 5 pontos.",Color .YELLOW ))
        ui_module .pause ()
        return 
    options =[f"+5 {attr_labels [a ]} (atual: {player .attributes [a ]})"for a in attrs ]
    options .append ("Voltar")
    idx =ui_module .arrow_menu (options ,title ="Escolha o atributo:")
    if idx <0 or idx ==len (attrs ):
        return 
    attr =attrs [idx ]
    for _ in range (5 ):
        if not player .level_system .spend_point (attr ,player ):
            break 
    ui_module .tprint (c (f"\n+5 em {attr_labels [attr ]}!",Color .BRIGHT_GREEN +Color .BOLD ))
    ui_module .pause ()

def apply_auto_allocate_now (player ,ui_module ):
    if not player .auto_allocate_build :
        ui_module .tprint (c ("\nVoce nao tem um esquema Auto-Alocate configurado.",Color .YELLOW ))
        ui_module .tprint (c ("Configure um em 'Configurar Auto-Alocate'.",Color .DIM ))
        ui_module .pause ()
        return 
    if player .level_system .attribute_points <=0 :
        ui_module .tprint (c ("\nVoce nao tem pontos para distribuir.",Color .YELLOW ))
        ui_module .pause ()
        return 
    player .apply_auto_allocate (points =player .level_system .attribute_points ,ui_module =ui_module )
    ui_module .pause ()

def configure_auto_allocate (player ,ui_module ):
    attrs =list (player .attributes .keys ())
    attr_labels ={
    "forca":"Forca Fisica",
    "ce":"Energia Amaldicoada (CE)",
    "controle":"Controle de CE",
    "velocidade":"Velocidade",
    "vigor":"Vigor (HP)",
    "sorte":"Sorte",
    }

    while True :
        ui_module .clear_screen ()
        ui_module .title_box ("  CONFIGURAR AUTO-ALLOCATE  ")
        print (c ("\n  Crie seu proprio esquema de distribuicao automatica.",Color .DIM ))
        print (c ("  Defina o PESO de cada atributo. Ao upar de level, os 5 pontos",Color .DIM ))
        print (c ("  serao distribuidos proporcionalmente aos pesos.",Color .DIM ))
        print (c ("  Ex: Forca=3, Vigor=1, Velocidade=1 -> a cada 5 pontos, ~3 Forca, ~1 Vigor, ~1 Velocidade",Color .DIM ))
        print ()
        if player .auto_allocate_build :
            print (c ("  Esquema atual:",Color .BRIGHT_CYAN ))
            for attr in attrs :
                w =player .auto_allocate_build .get (attr ,0 )
                label =attr_labels .get (attr ,attr )
                print (c (f"    {label }: {w }",Color .BRIGHT_WHITE ))
            total =sum (player .auto_allocate_build .values ())
            print (c (f"    Total de pesos: {total } (5 pontos / level)",Color .DIM ))
        else :
            print (c ("  Auto-Alocate DESATIVADO (nenhum esquema configurado).",Color .DIM ))
        print ()

        options =[]
        for attr in attrs :
            w =player .auto_allocate_build .get (attr ,0 )if player .auto_allocate_build else 0
            options .append (f"Editar peso de {attr_labels [attr ]} (atual: {w })")
        if player .auto_allocate_build :
            options .append ("Aplicar esquema agora (usa todos os pontos disponiveis)")
            options .append ("Desativar Auto-Alocate (limpa o esquema)")
        else :
            options .append ("Criar novo esquema (inicia vazio)")
        options .append ("Voltar")

        idx =ui_module .arrow_menu (options ,title ="Acao:")
        if idx <0 or idx ==len (options )-1 :
            return 

        if idx <len (attrs ):
            edit_scheme_weight (player ,attrs [idx ],attr_labels ,ui_module )
        elif idx ==len (attrs ):
            if player .auto_allocate_build :
                apply_auto_allocate_now (player ,ui_module )
            else :
                player .auto_allocate_build ={}
                ui_module .tprint (c ("\nEsquema vazio criado. Edite os pesos de cada atributo.",Color .BRIGHT_GREEN ))
                ui_module .pause ()
        elif idx ==len (attrs )+1 and player .auto_allocate_build :
            player .auto_allocate_build =None 
            ui_module .tprint (c ("\nAuto-Alocate desativado.",Color .DIM ))
            ui_module .pause ()

def edit_scheme_weight (player ,attr ,attr_labels ,ui_module ):
    if not player .auto_allocate_build :
        player .auto_allocate_build ={}
    current =player .auto_allocate_build .get (attr ,0 )
    label =attr_labels .get (attr ,attr )
    ui_module .clear_screen ()
    ui_module .title_box (f"  PESO DE {label .upper ()}  ")
    print (c (f"\n  Peso atual: {current }",Color .BRIGHT_WHITE ))
    print (c ("  Digite o novo peso (0 a 10). 0 = nao recebe pontos.",Color .DIM ))
    print (c ("  Pesos maiores = mais pontos vao para este atributo.",Color .DIM ))
    print ()
    try :
        choice =input (c ("  Novo peso > ",Color .BRIGHT_YELLOW )).strip ()
        if not choice .isdigit ():
            ui_module .tprint (c ("  Valor invalido. Use um numero inteiro.",Color .RED ))
            ui_module .pause ()
            return 
        w =int (choice )
        if w <0 or w >10 :
            ui_module .tprint (c ("  Peso deve ser entre 0 e 10.",Color .RED ))
            ui_module .pause ()
            return 
    except (EOFError ,KeyboardInterrupt ):
        return 
    if w ==0 :
        if attr in player .auto_allocate_build :
            del player .auto_allocate_build [attr ]
    else :
        player .auto_allocate_build [attr ]=w 
    if not player .auto_allocate_build :
        player .auto_allocate_build =None 
        ui_module .tprint (c (f"\nPeso de {label } removido. Esquema ficou vazio - Auto-Alocate desativado.",Color .DIM ))
    else :
        ui_module .tprint (c (f"\nPeso de {label } definido para {w }.",Color .BRIGHT_GREEN ))
    ui_module .pause ()

if __name__ =="__main__":
    setup_terminal ()
    if updater .check_and_update ():
        sys .exit (0 )
    try :
        main_menu ()
    except KeyboardInterrupt :
        ui .clear_screen ()
        print (c ("\nJogo interrompido. Ate logo!",Color .BRIGHT_CYAN ))
        sys .exit (0 )
    except Exception as e :
        ui .clear_screen ()
        print (c (f"\nErro: {e }",Color .BRIGHT_RED ))
        import traceback 
        traceback .print_exc ()
        print (c ("\nPressione qualquer tecla para sair.",Color .DIM ))
        try :
            keyboard_input .get_key ()
        except (KeyboardInterrupt ,EOFError ,Exception ):
            pass 
        sys .exit (1 )
