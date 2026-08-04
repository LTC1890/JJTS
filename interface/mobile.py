
import os 
import sys 

sys .path .insert (0 ,os .path .dirname (os .path .abspath (__file__ )))

from config import CONFIG
from ui import Color ,c ,pause

def detect_mobile_platform ():

    indicators =[]

    if os .environ .get ("TERMUX_VERSION"):
        indicators .append ("Termux (Android)")
    if os .environ .get ("IS_TERMUX"):
        indicators .append ("Termux")
    if os .environ .get ("PREFIX","").startswith ("/data/data/com.termux"):
        indicators .append ("Termux (Android)")
    if os .environ .get ("ISH_VERSION"):
        indicators .append ("iSH (iOS)")

    try :
        import shutil 
        cols ,rows =shutil .get_terminal_size ((80 ,24 ))
        if cols <50 or rows <20 :
            indicators .append (f"terminal pequeno ({cols }x{rows })")
    except Exception :
        pass 

    if not sys .stdin .isatty ()and os .environ .get ("SSH_CONNECTION"):
        indicators .append ("SSH remoto")

    return bool (indicators ),indicators 

def select_input_mode (ui_module =None ):

    if ui_module is None :
        import ui as ui_module 

    detected ,indicators =detect_mobile_platform ()

    ui_module .clear_screen ()
    ui_module .banner ()
    print ()
    ui_module .title_box ("  SELECIONE O MODO DE JOGO  ")
    print ()

    if detected :
        print (c ("  Plataforma mobile detectada:",Color .BRIGHT_YELLOW ))
        for ind in indicators :
            print (c (f"    - {ind }",Color .YELLOW ))
        print (c ("  Recomendamos o Modo Mobile.",Color .BRIGHT_GREEN ))
        print ()

    print (c ("  Escolha como deseja navegar nos menus:",Color .BRIGHT_CYAN ))
    print ()
    print (c ("  [1]",Color .BRIGHT_YELLOW )+" Modo PC")
    print (c ("      Navegacao com setas direcionais (Cima/Baixo)",Color .DIM ))
    print (c ("      ENTER para confirmar, ESC para voltar",Color .DIM ))
    print (c ("      Atalhos: digite o numero da opcao + ENTER",Color .DIM ))
    print ()
    print (c ("  [2]",Color .BRIGHT_YELLOW )+" Modo Mobile")
    print (c ("      Navegacao por numeros (1, 2, 3...)",Color .BRIGHT_WHITE ))
    print (c ("      Digite o numero da opcao + ENTER",Color .DIM ))
    print (c ("      0 = Voltar / Cancelar",Color .DIM ))
    print (c ("      Ideal para Termux, iSH, SSH mobile, etc",Color .DIM ))
    print ()

    while True :
        try :
            choice =input (c ("  Digite 1 (PC) ou 2 (Mobile): ",Color .BRIGHT_YELLOW )).strip ()
        except (EOFError ,KeyboardInterrupt ):

            choice ="1"

        if choice =="1":
            CONFIG .input_mode ="pc"
            CONFIG .save ()
            ui_module .tprint (c ("\n  Modo PC selecionado. Use as setas.",Color .BRIGHT_GREEN ))
            ui_module .pause ()
            return "pc"
        elif choice =="2":
            CONFIG .input_mode ="mobile"
            CONFIG .save ()
            ui_module .tprint (c ("\n  Modo Mobile selecionado. Use numeros + ENTER.",Color .BRIGHT_GREEN ))
            ui_module .pause ()
            return "mobile"
        else :
            print (c ("  Escolha invalida. Digite 1 ou 2.",Color .RED ))

def get_current_mode ():

    return CONFIG .input_mode 

def is_mobile ():

    return CONFIG .is_mobile ()

def is_pc ():

    return not CONFIG .is_mobile ()

def mobile_get_menu_choice (num_options ,allow_zero =True ):

    prompt =c ("  Digite o numero (0=voltar): ",Color .BRIGHT_YELLOW )if allow_zero else c ("  Digite o numero: ",Color .BRIGHT_YELLOW )

    attempts =0 
    while attempts <3 :
        try :
            choice =input (prompt ).strip ()
        except (EOFError ,KeyboardInterrupt ):
            return -1 

        if choice =="":

            return 0 

        if not choice .isdigit ():
            print (c ("  Por favor digite apenas numeros.",Color .RED ))
            attempts +=1 
            continue 

        n =int (choice )
        if allow_zero and n ==0 :
            return -1 
        if 1 <=n <=num_options :
            return n -1 

        print (c (f"  Numero invalido. Digite entre 1 e {num_options }"+
        (" ou 0 para voltar."if allow_zero else "."),Color .RED ))
        attempts +=1 

    return -1 

def mobile_input (prompt =""):

    try :
        return input (c (prompt ,Color .BRIGHT_YELLOW )).strip ()
    except (EOFError ,KeyboardInterrupt ):
        return ""

def mobile_pause (prompt ="Pressione ENTER para continuar..."):

    try :
        input (c (f"\n  {prompt }",Color .DIM ))
    except (EOFError ,KeyboardInterrupt ):
        pass 

def demo_mobile_mode ():

    import ui as ui_module 
    ui_module .clear_screen ()
    ui_module .title_box ("  TESTE DO MODO MOBILE  ")
    print ()
    print (c ("  Modo atual: "+("MOBILE"if is_mobile ()else "PC"),Color .BRIGHT_CYAN ))
    print ()
    print (c ("  Exemplo de menu numerico:",Color .BRIGHT_YELLOW ))
    print ()

    options =["Atacar","Defender","Usar Tecnica","Fugir"]
    for i ,opt in enumerate (options ,1 ):
        print (c (f"  [{i }]",Color .BRIGHT_YELLOW )+f" {opt }")
    print (c ("  [0] Voltar",Color .DIM ))
    print ()

    idx =mobile_get_menu_choice (len (options ),allow_zero =True )
    if idx >=0 :
        print (c (f"\n  Voce selecionou: {options [idx ]}",Color .BRIGHT_GREEN ))
    else :
        print (c ("\n  Voce voltou.",Color .YELLOW ))
    pause ()

def show_input_mode_info ():

    if is_mobile ():
        return c ("[MODO MOBILE: numeros + ENTER | 0=voltar]",Color .BRIGHT_CYAN )
    else :
        return c ("[MODO PC: setas + ENTER | ESC=voltar]",Color .BRIGHT_CYAN )

def show_quick_help ():

    print ()
    if is_mobile ():
        print (c ("  === CONTROLES MOBILE ===",Color .BRIGHT_CYAN ))
        print (c ("  Digite o NUMERO da opcao desejada + ENTER",Color .WHITE ))
        print (c ("  0 + ENTER = Voltar / Cancelar",Color .WHITE ))
        print (c ("  ENTER puro = confirma opcao 1",Color .DIM ))
    else :
        print (c ("  === CONTROLES PC ===",Color .BRIGHT_CYAN ))
        print (c ("  Setas CIMA/BAIXO = navegar",Color .WHITE ))
        print (c ("  ENTER = confirmar",Color .WHITE ))
        print (c ("  ESC = voltar",Color .WHITE ))
        print (c ("  Digite o numero + ENTER = atalho rapido",Color .DIM ))
    print ()
