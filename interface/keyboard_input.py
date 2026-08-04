
import sys 
import os 

_CONFIG_CACHE =None 

def _get_config ():
    global _CONFIG_CACHE 
    if _CONFIG_CACHE is None :
        try :
            sys .path .insert (0 ,os .path .dirname (os .path .abspath (__file__ )))
            from config import CONFIG 
            _CONFIG_CACHE =CONFIG 
        except Exception :
            _CONFIG_CACHE =None 
    return _CONFIG_CACHE 

def _is_mobile ():
    cfg =_get_config ()
    if cfg is None :
        return False 
    return cfg .is_mobile ()

def _get_char_unix ():
    import termios 
    import tty 
    fd =sys .stdin .fileno ()
    old_settings =termios .tcgetattr (fd )
    try :
        tty .setraw (fd )
        ch =sys .stdin .read (1 )
    finally :
        termios .tcsetattr (fd ,termios .TCSADRAIN ,old_settings )
    return ch 

def _get_char_windows ():
    import msvcrt 
    return msvcrt .getch ().decode ("latin-1")

def get_char ():

    if os .name =="nt":
        return _get_char_windows ()
    return _get_char_unix ()

def get_key ():

    if _is_mobile ():
        return _mobile_get_key ()

    ch =get_char ()

    if ch =="\x03":
        raise KeyboardInterrupt 
    if ch =="\x04":
        raise EOFError 

    if ch =="\r"or ch =="\n":
        return "ENTER"

    if os .name =="nt"and ch in ("\xe0","\x00"):
        import msvcrt 
        if msvcrt .kbhit ():
            ch2 =get_char ()
            keys ={"H":"UP","P":"DOWN","M":"RIGHT","K":"LEFT",
            "G":"HOME","O":"END","I":"PAGEUP","Q":"PAGEDOWN",
            "R":"INSERT","S":"DELETE",
            ";":"F1","<":"F2","=":"F3",">":"F4","?":"F5","@":"F6",
            "A":"F7","B":"F8","C":"F9","D":"F10","\x85":"F11","\x86":"F12"}
            return keys .get (ch2 ,"ESC")
        return "ESC"

    if ch =="\x1b":

        if os .name =="nt":

            import msvcrt 
            if msvcrt .kbhit ():
                ch2 =get_char ()
                if ch2 =="[":
                    if msvcrt .kbhit ():
                        ch3 =get_char ()
                        arrows ={"A":"UP","B":"DOWN","C":"RIGHT","D":"LEFT",
                        "H":"HOME","F":"END"}
                        return arrows .get (ch3 ,"ESC")
            return "ESC"
        else :

            import select 
            if select .select ([sys .stdin ],[],[],0.05 )[0 ]:
                ch2 =get_char ()
                if ch2 =="[":
                    if select .select ([sys .stdin ],[],[],0.05 )[0 ]:
                        ch3 =get_char ()

                        if ch3 in ("1","2","3","4","5","6","7","8"):
                            try :
                                ch4 =get_char ()
                            except Exception :
                                ch4 =""
                            combo =ch3 +ch4 
                            til_map ={
                            "1~":"HOME","4~":"END",
                            "5~":"PAGEUP","6~":"PAGEDOWN",
                            "2~":"INSERT","3~":"DELETE",
                            }
                            return til_map .get (combo ,"ESC")
                        arrows ={"A":"UP","B":"DOWN","C":"RIGHT","D":"LEFT",
                        "H":"HOME","F":"END"}
                        return arrows .get (ch3 ,"ESC")
                elif ch2 =="O":
                    if select .select ([sys .stdin ],[],[],0.05 )[0 ]:
                        ch3 =get_char ()
                        arrows ={"H":"HOME","F":"END",
                        "P":"F1","Q":"F2","R":"F3","S":"F4"}
                        return arrows .get (ch3 ,"ESC")
            return "ESC"

    if ch ==" ":
        return "SPACE"

    if ch in ("\x7f","\x08"):
        return "BACKSPACE"

    return ch .upper ()if ch .isalpha ()else ch 

def _mobile_get_key ():

    try :
        line =input ().strip ()
    except (EOFError ,KeyboardInterrupt ):
        return "ESC"

    if line =="":
        return "ENTER"
    if line in ("0","q","Q","esc","ESC","sair","voltar"):
        return "ESC"

    first =line [0 ]
    return first .upper ()if first .isalpha ()else first 

def wait_for_key (prompt ="Pressione qualquer tecla..."):

    if _is_mobile ():

        try :
            input (prompt +" (ENTER) ")
        except (EOFError ,KeyboardInterrupt ):
            pass 
        return "ENTER"
    else :
        print (prompt ,end ="",flush =True )
        k =get_key ()
        print ()
        return k

def _wait_for_key_timed_unix (timeout ):
    import termios 
    import tty 
    import select 
    fd =sys .stdin .fileno ()
    old_settings =termios .tcgetattr (fd )
    try :
        tty .setraw (fd )
        rlist ,_ ,_ =select .select ([sys .stdin ],[],[],timeout )
        if rlist :
            ch =sys .stdin .read (1 )
            return ch 
        return None 
    finally :
        termios .tcsetattr (fd ,termios .TCSADRAIN ,old_settings )

def _wait_for_key_timed_windows (timeout ):
    import msvcrt 
    import time 
    start =time .time ()
    while time .time ()-start <timeout :
        if msvcrt .kbhit ():
            ch =msvcrt .getch ().decode ("latin-1")
            if ch in ("\xe0","\x00")and msvcrt .kbhit ():
                msvcrt .getch ()
            return ch 
        time .sleep (0.01 )
    return None 

def wait_for_key_timed (timeout ):
    try :
        if os .name =="nt":
            return _wait_for_key_timed_windows (timeout )
        return _wait_for_key_timed_unix (timeout )
    except Exception :
        return "UNSUPPORTED"

def _flush_stdin_buffer ():
    try :
        if os .name =="nt":
            import msvcrt 
            while msvcrt .kbhit ():
                msvcrt .getch ()
        else :
            import termios 
            termios .tcflush (sys .stdin .fileno (),termios .TCIFLUSH )
    except Exception :
        pass 

MIN_PLAUSIBLE_REACTION_SECONDS =0.15 

def _mobile_ding_minigame (ui_module ,wait_min ,wait_max ,window ,prompt_wait ,prompt_go ):
    import random 
    import time 

    ui_module .tprint (prompt_wait )
    total_wait =random .uniform (wait_min ,wait_max )
    time .sleep (min (total_wait ,2.5 ))

    _flush_stdin_buffer ()

    ui_module .tprint (prompt_go )
    start =time .time ()
    try :
        input ()
    except (EOFError ,KeyboardInterrupt ):
        return "too_late"
    elapsed =time .time ()-start 

    if elapsed <MIN_PLAUSIBLE_REACTION_SECONDS :
        return "too_early"

    mobile_window =max (window *2.0 ,0.5 )
    if elapsed <=mobile_window :
        return "success"
    return "too_late"

def reaction_minigame (ui_module ,wait_min =0.6 ,wait_max =1.6 ,window =0.5 ,
prompt_wait ="Prepare-se...",prompt_go ="AGORA!! (aperte qualquer tecla)",difficulty =0.0 ):
    import random 

    difficulty =max (0.0 ,min (1.0 ,difficulty ))
    window =max (0.10 ,window *(1.0 -0.65 *difficulty ))
    wait_min =max (0.15 ,wait_min *(1.0 -0.35 *difficulty ))
    wait_max =max (wait_min +0.15 ,wait_max *(1.0 -0.20 *difficulty ))

    if _is_mobile ():
        return _mobile_ding_minigame (ui_module ,wait_min ,wait_max ,window ,prompt_wait ,prompt_go )

    probe =wait_for_key_timed (0.001 )
    if probe =="UNSUPPORTED":
        return _mobile_ding_minigame (ui_module ,wait_min ,wait_max ,window ,prompt_wait ,prompt_go )

    ui_module .tprint (prompt_wait )
    total_wait =random .uniform (wait_min ,wait_max )
    elapsed =0.0 
    slice_size =0.05 
    while elapsed <total_wait :
        step =min (slice_size ,total_wait -elapsed )
        ch =wait_for_key_timed (step )
        if ch not in (None ,"UNSUPPORTED"):
            return "too_early"
        elapsed +=step 

    ui_module .tprint (prompt_go )
    ch =wait_for_key_timed (window )
    if ch in (None ,"UNSUPPORTED"):
        return "too_late"
    return "success"
