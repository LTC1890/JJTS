
import sys 
import os 
import time 

try :
    import keyboard_input 
    from config import CONFIG 
except ImportError :

    sys .path .insert (0 ,os .path .dirname (os .path .abspath (__file__ )))
    import keyboard_input 
    from config import CONFIG 

class Color :
    RESET ="\033[0m"
    BOLD ="\033[1m"
    DIM ="\033[2m"
    ITALIC ="\033[3m"
    UNDERLINE ="\033[4m"
    BLINK ="\033[5m"
    REVERSE ="\033[7m"

    BLACK ="\033[30m"
    RED ="\033[31m"
    GREEN ="\033[32m"
    YELLOW ="\033[33m"
    BLUE ="\033[34m"
    MAGENTA ="\033[35m"
    CYAN ="\033[36m"
    WHITE ="\033[37m"

    BRIGHT_BLACK ="\033[90m"
    BRIGHT_RED ="\033[91m"
    BRIGHT_GREEN ="\033[92m"
    BRIGHT_YELLOW ="\033[93m"
    BRIGHT_BLUE ="\033[94m"
    BRIGHT_MAGENTA ="\033[95m"
    BRIGHT_CYAN ="\033[96m"
    BRIGHT_WHITE ="\033[97m"

    BG_RED ="\033[41m"
    BG_GREEN ="\033[42m"
    BG_YELLOW ="\033[43m"
    BG_BLUE ="\033[44m"
    BG_MAGENTA ="\033[45m"
    BG_CYAN ="\033[46m"
    BG_WHITE ="\033[47m"

def _supports_color ():
    if not CONFIG .color_enabled :
        return False 
    plat =sys .platform 
    supported =plat !="Pocket PC"and (plat !="win32"or 
    "ANSICON"in os .environ or 
    "WT_SESSION"in os .environ or 
    os .environ .get ("TERM_PROGRAM")=="vscode")
    if not supported :
        return False 
    return hasattr (sys .stdout ,"isatty")and sys .stdout .isatty ()

_COLOR_OK =None 

def c (text ,color ):

    global _COLOR_OK 
    if _COLOR_OK is None :
        _COLOR_OK =_supports_color ()
    if _COLOR_OK :
        return f"{color }{text }{Color .RESET }"
    return text 

def clear_screen ():

    os .system ("cls"if os .name =="nt"else "clear")

def type_text (text ,delay =None ,end ="\n",flush_end =True ):

    if delay is None :
        delay =CONFIG .get_text_delay ()

    if delay <=0 :

        sys .stdout .write (text +end )
        sys .stdout .flush ()
        return 

    i =0 
    n =len (text )
    while i <n :
        ch =text [i ]

        if ch =="\033":
            j =i 
            while j <n and text [j ]!="m":
                j +=1 
            if j <n :
                j +=1 
            sys .stdout .write (text [i :j ])
            sys .stdout .flush ()
            i =j 
            continue 

        sys .stdout .write (ch )
        sys .stdout .flush ()

        if ch in ("\n","\r"):
            time .sleep (delay *0.5 )
        elif ch in (" ","\t"):
            time .sleep (delay *0.3 )
        else :
            time .sleep (delay )
        i +=1 

    sys .stdout .write (end )
    if flush_end :
        sys .stdout .flush ()

def tprint (text ,delay =None ,end ="\n"):

    type_text (text ,delay =delay ,end =end )

def line (char ="=",length =70 ,color =None ):

    if color :
        print (c (char *length ,color ))
    else :
        print (char *length )

def title_box (text ,color =Color .BRIGHT_CYAN ):

    border ="+"+"-"*(len (text )+2 )+"+"
    print (c (border ,color ))
    print (c (f"| {text } |",color ))
    print (c (border ,color ))

def arrow_menu (options ,title =None ,color =Color .BRIGHT_CYAN ,prompt_color =Color .BRIGHT_YELLOW ):

    if not options :
        return -1 

    if CONFIG .is_mobile ():
        return _arrow_menu_mobile (options ,title ,color ,prompt_color )

    selected =0 

    while True :

        if title :
            print (c (f" {title }",color ))
            print (c ("-"*60 ,Color .DIM ))

        for i ,opt in enumerate (options ):
            if isinstance (opt ,dict ):
                label =opt .get ("label","")
                desc =opt .get ("desc","")
            else :
                label =opt 
                desc =""

            prefix =c (">",prompt_color )+" "if i ==selected else "  "
            if i ==selected :
                line_str =f"{prefix }{c (label ,Color .BOLD +Color .BRIGHT_WHITE )}"
                if desc :
                    line_str +=c (f"  - {desc }",Color .DIM )
            else :
                line_str =f"{prefix }{label }"
                if desc :
                    line_str +=c (f"  - {desc }",Color .DIM )
            print (line_str )

        print (c ("\n[Setas: navegar | ENTER: confirmar | ESC: voltar]",Color .DIM ))

        key =keyboard_input .get_key ()
        if key =="UP":
            selected =(selected -1 )%len (options )
        elif key =="DOWN":
            selected =(selected +1 )%len (options )
        elif key =="ENTER":
            clear_screen ()
            return selected 
        elif key =="ESC":
            clear_screen ()
            return -1 
        elif key in ("Q","q"):
            clear_screen ()
            return -1 
        else :

            if key .isdigit ():
                idx =int (key )-1 
                if 0 <=idx <len (options ):
                    clear_screen ()
                    return idx 

        clear_screen ()

def _arrow_menu_mobile (options ,title =None ,color =Color .BRIGHT_CYAN ,
prompt_color =Color .BRIGHT_YELLOW ):

    while True :
        if title :
            print (c (f" {title }",color ))
            print (c ("-"*60 ,Color .DIM ))

        for i ,opt in enumerate (options ,1 ):
            if isinstance (opt ,dict ):
                label =opt .get ("label","")
                desc =opt .get ("desc","")
            else :
                label =opt 
                desc =""

            num_str =c (f"  [{i }]",prompt_color )
            line_str =f"{num_str } {c (label ,Color .BRIGHT_WHITE )}"
            if desc :
                line_str +=c (f"  - {desc }",Color .DIM )
            print (line_str )

        print (c ("\n  [0] Voltar",Color .DIM ))
        print ()
        try :
            choice =input (c ("  Digite o numero: ",prompt_color )).strip ()
        except (EOFError ,KeyboardInterrupt ):
            clear_screen ()
            return -1 

        if choice =="":

            clear_screen ()
            return 0 

        if not choice .isdigit ():
            print (c ("  Por favor, digite apenas numeros.",Color .RED ))
            try :
                input (c ("  [ENTER para tentar de novo]",Color .DIM ))
            except (EOFError ,KeyboardInterrupt ):
                pass 
            clear_screen ()
            continue 

        n =int (choice )
        if n ==0 :
            clear_screen ()
            return -1 
        if 1 <=n <=len (options ):
            clear_screen ()
            return n -1 

        print (c (f"  Numero invalido. Digite entre 1 e {len (options )} ou 0 para voltar.",Color .RED ))
        try :
            input (c ("  [ENTER para tentar de novo]",Color .DIM ))
        except (EOFError ,KeyboardInterrupt ):
            pass 
        clear_screen ()

def arrow_menu_with_cancel (options ,title =None ,cancel_label ="Voltar",color =Color .BRIGHT_CYAN ):

    full =list (options )+[cancel_label ]
    idx =arrow_menu (full ,title =title ,color =color )
    if idx ==len (options ):
        return -1 
    return idx 

def confirm (prompt ="Confirmar?",default_yes =True ):

    opts =["Sim","Nao"]

    if default_yes :
        opts =["Sim (padrao)","Nao"]
    else :
        opts =["Sim","Nao (padrao)"]
    idx =arrow_menu (opts ,title =prompt )
    return idx ==0

def pause (prompt ="\n[Pressione qualquer tecla para continuar]"):

    if CONFIG .is_mobile ():
        try :
            input (c (prompt +" (ENTER) ",Color .DIM ))
        except (EOFError ,KeyboardInterrupt ):
            pass 
    else :
        print (c (prompt ,Color .DIM ),end ="",flush =True )
        keyboard_input .get_key ()
        print ()

def bar (current ,maximum ,length =20 ,fill_char ="#",empty_char ="-",
fill_color =Color .GREEN ,empty_color =Color .DIM ):

    if maximum <=0 :
        pct =0 
    else :
        pct =max (0.0 ,min (1.0 ,current /maximum ))
    filled =int (length *pct )
    empty =length -filled 
    fill =c (fill_char *filled ,fill_color )
    empt =c (empty_char *empty ,empty_color )
    return f"[{fill }{empt }] {current }/{maximum }"

def hp_bar (hp ,max_hp ,length =20 ):

    if max_hp <=0 :
        pct =0 
    else :
        pct =hp /max_hp 
    if pct >0.6 :
        col =Color .GREEN 
    elif pct >0.3 :
        col =Color .YELLOW 
    else :
        col =Color .RED 
    return bar (hp ,max_hp ,length =length ,fill_color =col )

def ce_bar (ce ,max_ce ,length =20 ):

    return bar (ce ,max_ce ,length =length ,fill_color =Color .BRIGHT_BLUE ,
    empty_char ="-")

def xp_bar (current_xp ,xp_to_next ,length =20 ):

    if xp_to_next <=0 :
        return c ("[MAX LEVEL]",Color .BRIGHT_YELLOW +Color .BOLD )
    pct =min (1.0 ,current_xp /xp_to_next )
    filled =int (length *pct )
    empty =length -filled 
    fill =c ("#"*filled ,Color .BRIGHT_YELLOW )
    empt =c ("-"*empty ,Color .DIM )
    return f"[{fill }{empt }] {current_xp }/{xp_to_next } XP"

ASCII_LOGO =r"""
   ___  ___  ___  ___  ___  ___  ___  ___  ___  ___
  |_ _||_ _||_ _||_ _||_ _||_ _||_ _||_ _||_ _||_ _|
   ___  ___  ___  ___  ___  ___  ___  ___  ___  ___
  | J || J || T || S || - || J || U || J || U || T || S || U
   """+"""
   =====================================================
        JUJUTSU TEXTSEN - A Maldicao do Terminal
   =====================================================
"""

ASCII_SKULL =r'''
        .-""""-.
       /        \
      |  _    _  |
      | (_)  (_) |
      |   /\     |
      \  `--`   /
       `------`
       M A L D I C A O
'''

ASCII_DOMAIN =r"""
   +-----------------------------------------+
   |       E X P A N S A O   D E   D O M I N I O       |
   |                  ~  ~  ~  ~  ~                  |
   |              ~    EXPANSAO    ~                |
   |                  ~  ~  ~  ~  ~                  |
   +-----------------------------------------+
"""

ASCII_BLACK_FLASH =r"""
   !  *  !  *  !  *  !  *  !  *  !  *  !
   *  P I S C A R   N E G R O  *
   !  *  !  *  !  *  !  *  !  *  !  *  !
   >>>>>>>>>>>> K A B O O M <<<<<<<<<<<<
"""

ASCII_GOJO =r"""
      ___
     /o o\
    |  ^  |
     \ - /
    /|   |\
   / |   | \
  /  |___|  \
 /___|   |___\
   |  ___  |
   |_______|
   GOJO SATORU
   Os Seis Olhos
"""

ASCII_SUKUNA =r"""
   .-"-.
  /  o  \
 | .---. |
  \  v  /
   '-.-'
   / | \
  /  |  \
   SUKUNA
   Rei das Maldicoes
"""

ASCII_MAHITO =r"""
   .---.
  /     \
 | o   o |
 |  <->  |
  \  w  /
   '---'
   MAHITO
   Maldicao das Almas
"""

ASCII_TOJI =r"""
    [---]
     | |
    /   \
   |     |
   |  T  |
   |____ |
   TOJI FUSHIGURO
   O Sacrificio
"""

ASCII_SCHOOL =r"""
        ______________
       /  TOKYO JJHS  \
      /__________ _____\
         ||    ||
    _____||____||_____
   |   ESCOLA DE       |
   |   FEITICEIROS     |
   |___________________|
        ||        ||
   TOKYO JUJUTSU HIGH
"""

ASCII_SHOP =r"""
      _____________
     /  \ LOJA /  \
    /____\____/____\
   |  $   CE   $   |
   |  amuletos armas |
   |  pergaminhos     |
   |__________________|
   LOJA DA ESCOLA
"""

ASCII_INVENTORY =r"""
    .-==========-.
   /  MOCHILA     \
  |  [] [] []      |
  |  [] [] []      |
   \_______________/
      |   |   |
   INVENTARIO
"""

ASCII_CHARACTER =r"""
       .-----.
      /  o o  \
     |    ^    |
      \  ___  /
    ---'     '---
   FICHA DO FEITICEIRO
"""

ASCII_DUNGEON =r"""
    _____________
   /             \
  /   ___________ \
 |   /  ENTRADA  \ |
 |  |   AMALDI-   ||
 |  |   COADA     ||
 |   \___________/ |
  \_________________/
   REGIAO AMALDICOADA
"""

ASCII_AWAKENING =r"""
        *  .  *    .   *
      .   \  |  /   .
    *   `--(o)--'   *   .
      .   /  |  \    .
        *  .  *    .   *
   O DESPERTAR AMALDICOADO
"""

ASCII_MISSION =r"""
     ____________
    /  QUADRO DE  \
   |   MISSOES     |
   |  [x][ ][x]    |
   |  [ ][x][ ]    |
   |_______________|
   DETALHES DA MISSAO
"""

ASCII_SAVE =r"""
     ___________
    /  SELO DE  \
   |  GRAVACAO   |
   |   #  #  #   |
   |_____________|
      \  |  /
   SALVAR / CARREGAR
"""

def show_ascii (art ,color =Color .BRIGHT_MAGENTA ,clear =True ):

    if clear :
        clear_screen ()
    if CONFIG .ascii_art :
        for line in art .split ("\n"):
            print (c (line ,color ))
            time .sleep (0.05 )
    else :

        name =art .split ("\n")[-2 ].strip ()if "\n"in art else ""
        if name :
            print (c (f"[ {name } ]",color ))

def screen_header (art ,title ,subtitle =None ,color =Color .BRIGHT_MAGENTA ,title_color =Color .BRIGHT_CYAN ):

    show_ascii (art ,color =color ,clear =True )
    title_box (title ,color =title_color )
    if subtitle :
        print (c (subtitle ,Color .DIM ))

def stat_line (label ,value ,label_width =18 ,color =Color .BRIGHT_CYAN ):
    print (c (f"  {label :<{label_width}}: " ,color )+str (value ))

def roulette_reveal (candidates ,final_result ,label ="Sorteando",color =Color .BRIGHT_MAGENTA ,spins =14 ):
    import random 
    for i in range (spins ):
        pick =final_result if i ==spins -1 else random .choice (candidates )
        delay =0.03 +(i /spins )*0.10 
        print (c (f"\r  {label }... > {pick }" +" "*10 ,color ),end ="",flush =True )
        time .sleep (delay )
    print ()

def section (title ,lines ,color =Color .BRIGHT_CYAN ):
    if not lines :
        return 
    max_len =max ([len (title )]+[len (l )for l in lines ])
    border ="+"+"-"*(max_len +4 )+"+" 
    print (c (border ,color ))
    print (c (f"|  {title}{' '*(max_len-len(title))}  |" ,color ))
    print (c ("+"+"-"*(max_len +4 )+"+",color ))
    for l in lines :
        pad =" "*(max_len -len (l ))
        print (c (f"|  {l}{pad}  |" ,color ))
    print (c (border ,color ))

def banner ():

    if CONFIG .ascii_art :
        print (c (ASCII_LOGO ,Color .BRIGHT_CYAN ))
    else :
        print (c ("=== JUJUTSU TEXTSEN ===",Color .BRIGHT_CYAN ))
        print (c ("A Maldicao do Terminal",Color .DIM ))

def flash_red (text ,times =3 ):

    for _ in range (times ):
        sys .stdout .write ("\r"+" "*80 +"\r")
        sys .stdout .write (c (text ,Color .BG_RED +Color .BOLD +Color .WHITE ))
        sys .stdout .flush ()
        time .sleep (0.15 )
        sys .stdout .write ("\r"+" "*80 +"\r")
        sys .stdout .flush ()
        time .sleep (0.1 )
    print (c (text ,Color .BRIGHT_RED +Color .BOLD ))

def separator (char ="~",length =70 ,color =Color .BRIGHT_BLACK ):
    print (c (char *length ,color ))

def combat_separator ():
    separator (char ="*",length =60 ,color =Color .BRIGHT_RED )

def info_box (text ,color =Color .BRIGHT_CYAN ):

    lines =text .split ("\n")
    max_len =max (len (l )for l in lines )if lines else 0 
    border ="+"+"-"*(max_len +4 )+"+"
    print (c (border ,color ))
    for l in lines :
        pad =" "*(max_len -len (l ))
        print (c (f"|  {l }{pad }  |",color ))
    print (c (border ,color ))
