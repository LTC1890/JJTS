from .common import *

class PlayerActionsMixin :

    def player_action (self ):

        technique_sealed =self .player .get_debuff_value ("technique_sealed")>0 

        if technique_sealed :
            actions =["Atacar","Usar Tecnica (SELADA)","Esquivar","Contra-Golpe (Parry)","Reforco de CE",
            "Usar Item","Fugir"]
        else :
            actions =["Atacar","Usar Tecnica","Esquivar","Contra-Golpe (Parry)","Reforco de CE",
            "Usar Item","Fugir"]

        if self .player .has_domain_available ():
            can_dom ,_ =self .player .can_use_domain ()
            if can_dom :
                actions .append ("Expansao de Dominio")
            else :
                actions .append ("Expansao de Dominio (indisponivel)")

        if self .player .can_use_rct ():
            actions .append ("Tecnica Reversa (RCT)")

        if mahoraga_mod .can_use_stolen_adaptation (self .player ):
            if getattr (self .player ,"_stolen_adaptation_active",False ):
                actions .append ("Adaptacao Roubada (ATIVA)")
            else :
                actions .append ("Adaptacao Roubada (ativar)")

        if getattr (self .player ,"copied_technique",None ):
            copied =self .player .copied_technique 
            actions .append (f"Usar Copia: {copied ['name']} ({copied ['ce_cost']} CE)")

        idx =self .ui .arrow_menu (actions ,title ="Sua acao:")
        if idx <0 :
            return None 

        action =actions [idx ]
        if action =="Atacar":
            return self .player_attack ()
        elif action =="Usar Tecnica":
            return self .player_technique ()
        elif action =="Usar Tecnica (SELADA)":
            self .ui .tprint (c (
            "\nSua tecnica amaldicoada esta selada pelo Inversor de Espiritos! "
            "Ataque fisicamente ou use itens.",Color .RED ))
            self .ui .pause ()
            return None 
        elif action =="Esquivar":
            return self .player_dodge ()
        elif action =="Contra-Golpe (Parry)":
            return self .player_parry ()
        elif action =="Reforco de CE":
            return self .player_ce_reinforce ()
        elif action =="Usar Item":
            return self .player_use_item ()
        elif action =="Fugir":
            return self .player_flee ()
        elif action .startswith ("Expansao de Dominio"):
            if "indisponivel"in action :
                self .ui .tprint (c ("Dominio indisponivel agora.",Color .YELLOW ))
                can ,reason =self .player .can_use_domain ()
                self .ui .tprint (f"Motivo: {reason }")
                self .ui .pause ()
                return None 
            return self .player_domain_expansion ()
        elif action =="Tecnica Reversa (RCT)":
            return self .player_rct ()
        elif action =="Adaptacao Roubada (ativar)":
            mahoraga_mod .activate_stolen_adaptation (self .player ,ui_module =self .ui )
            return None 
        elif action =="Adaptacao Roubada (ATIVA)":
            self .ui .tprint (c (
            f"\nA Adaptacao Roubada ja esta ativa. "
            f"Proxima cobranca em {getattr (self .player ,'_stolen_adaptation_turns_left',0 )} turno(s).",
            Color .DIM ))
            self .ui .pause ()
            return None 
        elif action .startswith ("Usar Copia:"):
            return self .player_use_copied_technique ()
        return None 

    def player_attack (self ):

        alive_enemies =[e for e in self .enemies if e ["hp"]>0 ]
        if not alive_enemies :
            return None 
        if len (alive_enemies )==1 :
            target =alive_enemies [0 ]
        else :
            opts =[e ["name"]for e in alive_enemies ]
            idx =self .ui .arrow_menu (opts ,title ="Escolha o alvo:")
            if idx <0 :
                return None 
            target =alive_enemies [idx ]

        dodge_info =""
        if target .get ("can_dodge")and target .get ("dodge_chance",0 )>0 :
            effective =max (0 ,target .get ("dodge_chance",0 )-target .get ("dodge_penalty",0 ))
            dodge_info =c (f" [Esquiva: {int (effective *100 )}%]",Color .DIM )
        def_info =c (f" [DEF: {target .get ('def',0 )}]",Color .DIM )if target .get ("def",0 )>0 else ""
        self .ui .tprint (f"Alvo: {target ['name']}{dodge_info }{def_info }")

        base_dmg =self .player .get_total_str ()+random .randint (-3 ,5 )
        if self .player .equipped .get ("arma")and self .player .equipped ["arma"]in ITEMS_DB :
            base_dmg +=ITEMS_DB [self .player .equipped ["arma"]].get ("effect",{}).get ("dmg_bonus",0 )

        if target .get ("immune_physical"):
            self .ui .tprint (c (f"\n{target ['name']} eh imune a dano fisico!",Color .YELLOW ))
            self .ui .tprint (c ("Seu golpe atravessa o corpo sem causar dano.",Color .DIM ))
            self .ui .pause ()
            self .player_hit_streak =0 
            return None 

        effective_dodge =max (0 ,target .get ("dodge_chance",0 )-target .get ("dodge_penalty",0 ))
        if target .get ("can_dodge")and random .random ()<effective_dodge :
            self .ui .tprint (c (f"\nVoce ataca {target ['name']}, mas ele ESCAPA!",
            Color .YELLOW ))
            self .ui .pause ()
            self .player_hit_streak =0 
            return None 

        if target .get ("can_defend")and random .random ()<target .get ("defense_chance",0 ):
            defended =True 
            self .ui .tprint (c (f"\n{target ['name']} se DEFENDE com CE!",Color .BRIGHT_CYAN ))
        else :
            defended =False 

        self .player_hit_streak +=1 
        if self .player_hit_streak >=2 :
            self .ui .tprint (c (f"[Pressao x{self .player_hit_streak }]",Color .BRIGHT_YELLOW ))

        bleed_chance =0 
        if self .player .equipped .get ("arma")and self .player .equipped ["arma"]in ITEMS_DB :
            bleed_chance =ITEMS_DB [self .player .equipped ["arma"]].get ("effect",{}).get ("bleed_chance",0 )

        focus_bonus =self .player .get_buff_value ("black_flash_focus")*0.01 
        bf_chance =self .player .get_black_flash_chance ()+focus_bonus 
        if self .player_hit_streak >=3 :
            bf_chance +=0.10 
        black_flash =random .random ()<bf_chance 

        if black_flash :
            dmg =int (base_dmg *BLACK_FLASH_DMG_MULT *random .uniform (1.5 ,2.5 ))
            self .ui .flash_red (f"!! BLACK FLASH !! Dano: {dmg }")
            self .ui .show_ascii (ui .ASCII_BLACK_FLASH ,color =Color .BRIGHT_RED ,clear =False )
            self .ui .pause ()

            ce_gain =int (self .player .max_ce *BLACK_FLASH_CE_GAIN_PCT )
            if not self .player .sukuna_takeover_active :
                self .player .restore_ce (ce_gain )
                self .ui .tprint (c (f"+{ce_gain } CE da adrenaline!",Color .BRIGHT_CYAN ))
        else :
            dmg =base_dmg 
            self .ui .tprint (c (f"\nVoce ataca {target ['name']}!",Color .BRIGHT_WHITE ))

        armor_pierce =False 
        armor_pierce_pct =0.0 
        infinity_bypass =False 
        if self .player .equipped .get ("arma")and self .player .equipped ["arma"]in ITEMS_DB :
            eff =ITEMS_DB [self .player .equipped ["arma"]].get ("effect",{})
            armor_pierce =eff .get ("armor_pierce",False )
            armor_pierce_pct =eff .get ("armor_pierce_pct",0.0 )
            infinity_bypass =eff .get ("infinity_bypass",False )

        if target .get ("dmg_taken_mult",1.0 )<=0.0 and not infinity_bypass :
            self .ui .tprint (c (f"\nO Infinito de {target ['name']} bloqueia totalmente seu ataque!",Color .BRIGHT_CYAN ))
            self .ui .tprint (c ("(Use Inverted Spear of Heaven ou World Cutting Slash para atravessar.)",Color .DIM ))
            self .ui .pause ()
            self .player_hit_streak =0 
            return None 

        if armor_pierce :
            actual_dmg =dmg 
        elif armor_pierce_pct >0 :
            effective_def =int (target .get ("def",0 )*(1.0 -armor_pierce_pct ))
            actual_dmg =calculate_damage (dmg ,effective_def )
        else :
            actual_dmg =calculate_damage (dmg ,target .get ("def",0 ))

        if target .get ("adaptive"):
            mahoraga_resist =mahoraga_mod .get_damage_reduction (target ,"Ataque Fisico")
            if mahoraga_resist >0 :
                actual_dmg =max (1 ,int (actual_dmg *(1.0 -mahoraga_resist )))

        if infinity_bypass and target .get ("dmg_taken_mult",1.0 )<=0.0 :
            self .ui .tprint (c (f"!! {self .player .equipped ['arma']} ATRAVESSA O INFINITO !!",
            Color .BRIGHT_YELLOW +Color .BOLD ))

        if defended :
            actual_dmg =int (actual_dmg *DEFENDED_DMG_REDUCTION )
            self .ui .tprint (c (f"(Dano reduzido pela defesa: {actual_dmg })",Color .DIM ))

        if self .player_hit_streak >=3 :
            actual_dmg =int (actual_dmg *1.25 )
        elif self .player_hit_streak >=2 :
            actual_dmg =int (actual_dmg *1.15 )

        target ["hp"]-=actual_dmg 
        self .ui .tprint (c (f"Dano causado: {actual_dmg }",Color .BRIGHT_RED ))
        if target .get ("adaptive"):
            mahoraga_mod .register_hit (target ,"Ataque Fisico",ui_module =self .ui )
        else :
            self ._register_adaptation_hit (target ,"physical")

        if random .random ()<bleed_chance :
            b_resist =target .get ("bleed_resist",0.0 )
            if random .random ()>b_resist :
                target ["bleed_stacks"]=target .get ("bleed_stacks",0 )+2 
                self .ui .tprint (c (f"{target ['name']} esta sangrando!",Color .RED ))
                self ._register_adaptation_hit (target ,"bleed")
            else :
                self .ui .tprint (c (f"{target ['name']} resiste ao sangramento!",Color .DIM ))

        if self .player .equipped .get ("arma")and self .player .equipped ["arma"]in ITEMS_DB :
            weff =ITEMS_DB [self .player .equipped ["arma"]].get ("effect",{})
            stun_ch =weff .get ("stun_chance",0 )
            if stun_ch >0 and random .random ()<stun_ch :
                stun_turns =weff .get ("stun_turns",1 )
                resist =target .get ("stun_resist",0.0 )
                if random .random ()>resist :
                    target ["stunned_turns"]=max (1 ,target .get ("stunned_turns",0 )+stun_turns )
                    self .ui .tprint (c (f"{target ['name']} atordoado por {stun_turns }t! ({self .player .equipped ['arma']})",
                    Color .YELLOW ))
                else :
                    self .ui .tprint (c (f"{target ['name']} resiste ao atordoamento!",Color .DIM ))
            if weff .get ("damage_accumulator"):
                if not hasattr (self ,"_dragon_bone_stacks"):
                    self ._dragon_bone_stacks =0 
                    self ._dragon_bone_accumulated =0 
                    self ._dragon_bone_turns_left =weff .get ("accumulator_turns",4 )
                self ._dragon_bone_accumulated +=actual_dmg 
                self ._dragon_bone_turns_left -=1 
                self .ui .tprint (c (f"[Dragon Bone acumula dano: {self ._dragon_bone_accumulated } ({self ._dragon_bone_turns_left }t restante)]",
                Color .DIM ))
                if self ._dragon_bone_turns_left <=0 :
                    release_mult =weff .get ("accumulator_mult",2.5 )
                    release_dmg =int (self ._dragon_bone_accumulated *release_mult )
                    self .ui .tprint (c (f"\n!! DRAGON BONE LIBERA {release_dmg } de dano acumulado ({release_mult }x) !!",
                    Color .BRIGHT_YELLOW +Color .BOLD ))
                    for e in self .enemies :
                        if e .get ("hp",0 )>0 :
                            e ["hp"]-=release_dmg 
                            self .ui .tprint (c (f"  {e ['name']}: {release_dmg } dano",Color .BRIGHT_RED ))
                    self ._dragon_bone_stacks =0 
                    self ._dragon_bone_accumulated =0 
                    self ._dragon_bone_turns_left =weff .get ("accumulator_turns",4 )
            if weff .get ("dynamic_str_pct_per_5"):
                total_str =self .player .get_total_str ()
                bonus_pct =(total_str //5 )*weff ["dynamic_str_pct_per_5"]
                if bonus_pct >0 :
                    extra =int (actual_dmg *bonus_pct )
                    target ["hp"]-=extra 
                    self .ui .tprint (c (f"[Playful Cloud: +{extra } dano (forca {total_str })]",Color .DIM ))
            if weff .get ("technique_nullify"):
                target ["technique_nullified"]=True 
                self .ui .tprint (c (f"{target ['name']} teve sua tecnica anulada!",Color .BRIGHT_CYAN ))

        trait =BIRTH_TRAITS .get (self .player .birth_trait ,{})
        lifesteal_pct =trait .get ("effects",{}).get ("lifesteal_pct",0 )
        if lifesteal_pct >0 :
            heal =int (actual_dmg *lifesteal_pct )
            if not self .player .sukuna_takeover_active :
                self .player .hp =min (self .player .max_hp ,self .player .hp +heal )
                self .ui .tprint (c (f"Sugador de vida: +{heal } HP",Color .GREEN ))

        if self .player .equipped .get ("arma")and self .player .equipped ["arma"]in ITEMS_DB :
            ls =ITEMS_DB [self .player .equipped ["arma"]].get ("effect",{}).get ("lifesteal_pct",0 )
            if ls >0 :
                heal =int (actual_dmg *ls )
                if not self .player .sukuna_takeover_active :
                    self .player .hp =min (self .player .max_hp ,self .player .hp +heal )
                    self .ui .tprint (c (f"+{heal } HP (arma)",Color .GREEN ))

        self .ui .pause ()
        return None 

    def player_technique (self ):

        available_exts =get_available_extensions (self .player )
        if not available_exts :
            self .ui .tprint (c ("Voce nao tem tecnica disponivel.",Color .YELLOW ))
            self .ui .pause ()
            return None 

        tech_groups ={}
        for tech_name ,ext in available_exts :
            tech_groups .setdefault (tech_name ,[]).append (ext )

        if len (tech_groups )>1 :
            tech_labels =list (tech_groups .keys ())+["Voltar"]
            tidx =self .ui .arrow_menu (tech_labels ,title ="Qual tecnica usar?")
            if tidx <0 or tidx ==len (tech_labels )-1 :
                return None 
            selected_tech =list (tech_groups .keys ())[tidx ]
            extensions =tech_groups [selected_tech ]
        else :
            selected_tech =list (tech_groups .keys ())[0 ]
            extensions =tech_groups [selected_tech ]

        opts =[]
        for ext in extensions :
            ce_eff =self .player .get_ce_efficiency ()
            actual_ce =int (ext ["ce_cost"]/ce_eff )if ce_eff >0 else ext ["ce_cost"]
            hp_cost =ext .get ("hp_cost",0 )
            cost_str =f"CE: {actual_ce }"
            if hp_cost >0 :
                cost_str +=f" | HP: {hp_cost }"
            opts .append (f"{ext ['name']} ({cost_str })")
        opts .append ("Voltar")

        idx =self .ui .arrow_menu (opts ,title =f"Tecnica: {selected_tech }")
        if idx <0 or idx ==len (extensions ):
            return None 

        ext =extensions [idx ]

        actual_cost =int (ext ["ce_cost"]/self .player .get_ce_efficiency ())
        if ext .get ("sukuna_skill")and self .player .sukuna_fingers_eaten >0 :
            ce_reduction =self .player .sukuna_fingers_eaten *8
            actual_cost =max (0 ,actual_cost -ce_reduction )
        if self .player .ce_current <actual_cost :
            self .ui .tprint (c (f"CE insuficiente! Precisa de {actual_cost }.",Color .RED ))
            self .ui .pause ()
            return None 

        hp_cost =ext .get ("hp_cost",0 )
        if hp_cost >0 and self .player .hp <=hp_cost :
            self .ui .tprint (c (f"HP insuficiente! Precisa de {hp_cost } HP (nao pode se matar).",Color .RED ))
            self .ui .pause ()
            return None 

        if ext .get ("requires_hp_below_pct"):
            hp_pct =self .player .hp /max (1 ,self .player .max_hp )
            if hp_pct >ext ["requires_hp_below_pct"]:
                self .ui .tprint (c (f"Requer HP abaixo de {int (ext ['requires_hp_below_pct']*100 )}% (atual: {int (hp_pct *100 )}%).",Color .YELLOW ))
                self .ui .pause ()
                return None 

        if ext .get ("requires_ce_full"):
            if self .player .ce_current <self .player .max_ce :
                self .ui .tprint (c ("Requer CE 100%.",Color .YELLOW ))
                self .ui .pause ()
                return None 

        if ext .get ("one_use_per_battle"):
            if ext ["name"]in self .techniques_used_this_combat :
                self .ui .tprint (c (f"{ext ['name']} ja foi usado nesta batalha.",Color .YELLOW ))
                self .ui .pause ()
                return None 

        if ext .get ("type")=="domain_active":
            can ,reason =self .player .can_use_domain ()
            if not can :
                self .ui .tprint (c (f"Dominio indisponivel: {reason }",Color .RED ))
                self .ui .pause ()
                return None 

        if ext .get ("charge_turns"):
            if not ui .confirm (f"{ext ['name']} requer {ext ['charge_turns']} turno(s) de carga. Continuar?",default_yes =False ):
                return None
            if not hasattr (self ,"pending_charged_techniques"):
                self .pending_charged_techniques =[]
            target =None
            if ext ["type"]in ("attack","attack_aoe","stun","stun_chance",
            "debuff_dot","sleep","lifesteal","swap","swap_protect",
            "ce_drain_on_hit"):
                alive_enemies =[e for e in self .enemies if e ["hp"]>0 ]
                if not alive_enemies :
                    return None
                if ext ["type"]in ("attack_aoe","attack_chain"):
                    target ="all"
                elif len (alive_enemies )==1 :
                    target =alive_enemies [0 ]
                else :
                    opts =[e ["name"]for e in alive_enemies ]
                    idx =self .ui .arrow_menu (opts ,title ="Escolha o alvo da tecnica carregada:")
                    if idx <0 :
                        return None
                    target =alive_enemies [idx ]
            self .pending_charged_techniques .append ({
            "ext":ext ,"target":target ,"ce_cost":actual_cost ,"hp_cost":hp_cost ,
            "charge_turns":ext ["charge_turns"],
            })
            self .player .add_debuff ("charging",1 ,ext ["charge_turns"],f"Carga: {ext ['name']}")
            self .ui .tprint (c (f"\n{ext ['name']} sera carregada por {ext ['charge_turns']} turno(s).",Color .BRIGHT_YELLOW ))
            self .ui .tprint (c ("O CE sera consumido quando a tecnica disparar.",Color .DIM ))
            self .ui .pause ()
            return None

        self .player .ce_current -=actual_cost 

        if hp_cost >0 :
            self .player .hp =max (1 ,self .player .hp -hp_cost )
            self .ui .tprint (c (f"Custo de sangue: -{hp_cost } HP",Color .RED ))

        target =None 
        if ext ["type"]in ("attack","attack_aoe","stun","stun_chance",
        "debuff_dot","sleep","lifesteal","swap","swap_protect",
        "ce_drain_on_hit"):
            alive_enemies =[e for e in self .enemies if e ["hp"]>0 ]
            if not alive_enemies :
                return None 
            if ext ["type"]in ("attack_aoe","attack_chain"):
                target ="all"
            elif len (alive_enemies )==1 :
                target =alive_enemies [0 ]
            else :
                opts2 =[e ["name"]for e in alive_enemies ]
                idx2 =self .ui .arrow_menu (opts2 ,title ="Alvo:")
                if idx2 <0 :
                    self .player .ce_current +=actual_cost 
                    return None 
                target =alive_enemies [idx2 ]
        elif ext ["type"]=="domain_active":
            if ext .get ("name")and ext ["name"]not in self .techniques_used_this_combat :
                self .techniques_used_this_combat .append (ext ["name"])
            self .player .domain_used_count +=1 
            return self ._activate_domain (ext ,already_paid =True )

        if ext .get ("name")and ext ["name"]not in self .techniques_used_this_combat :
            self .techniques_used_this_combat .append (ext ["name"])
        return self .execute_technique (ext ,target )

    def _activate_domain (self ,ext ,already_paid =False ):

        if self .player .active_domain is not None :
            self .ui .tprint (c ("Voce ja tem uma expansao ativa!",Color .YELLOW ))
            self .ui .pause ()
            return None 

        if not already_paid :
            actual_cost =int (ext ["ce_cost"]/self .player .get_ce_efficiency ())
            if self .player .ce_current <actual_cost :
                self .ui .tprint (c (f"CE insuficiente! Precisa de {actual_cost }.",Color .RED ))
                self .ui .pause ()
                return None 
            self .player .ce_current -=actual_cost 

        clashing_enemy =next ((e for e in self .enemies if e .get ("hp",0 )>0 and e .get ("active_domain")),None )
        if clashing_enemy :
            enemy_dmg_mult =clashing_enemy .get ("active_domain",{}).get ("dmg_mult",3.0 )/3.0 
            player_dmg_mult =(ext .get ("dmg_per_turn_max",300 )/150.0 )
            player_wins =self ._resolve_domain_clash (clashing_enemy ,player_dmg_mult =player_dmg_mult ,
            enemy_dmg_mult =enemy_dmg_mult )
            if not player_wins :
                self .ui .tprint (c ("Seu dominio nao consegue se formar! Voce toma dano e fica atordoado.",
                Color .BRIGHT_RED +Color .BOLD ))
                punish =int (self .player .max_hp *0.15 )
                actual =self .player .take_damage (punish ,damage_type ="cursed",ignore_def =True )
                self .player .stunned_turns =max (1 ,self .player .stunned_turns +1 )
                self .ui .tprint (c (f"Voce toma {actual } dano do colapso do dominio.",Color .RED ))
                self .ui .pause ()
                return None 
            else :
                clashing_enemy ["active_domain"]=None 
                punish =int (clashing_enemy .get ("max_hp",1000 )*0.10 )
                clashing_enemy ["hp"]-=punish 
                self .ui .tprint (c (f"O dominio de {clashing_enemy ['name']} se despedaca! ({punish } dano)",
                Color .BRIGHT_GREEN ))
                self .ui .pause ()

        domain_id =ext .get ("domain_id")
        ce_per_turn =ext .get ("ce_per_turn",30 )
        self .player .active_domain ={
        "name":ext ["name"],
        "domain_id":domain_id ,
        "ce_per_turn":ce_per_turn ,
        "effect":ext ,
        "turns_active":0 ,
        }
        self .player .active_domain_used_count +=1 

        self .ui .clear_screen ()
        self .ui .show_ascii (ui .ASCII_DOMAIN ,color =Color .BRIGHT_MAGENTA ,clear =False )
        self .ui .tprint (c (f"!! EXPANSAO DE DOMINIO ATIVADA: {ext ['name']} !!",
        Color .BRIGHT_MAGENTA +Color .BOLD +Color .BLINK ))
        self .ui .tprint (c (f"   Custo: {ce_per_turn } CE por turno. Dura ate o CE acabar.",Color .DIM ))
        if "dmg_per_turn_min"in ext :
            self .ui .tprint (c (f"   Dano/turno: {ext ['dmg_per_turn_min']}-{ext ['dmg_per_turn_max']}",Color .DIM ))
        if ext .get ("bleed_per_turn"):
            self .ui .tprint (c (f"   Sangramento/turno: +{ext ['bleed_per_turn']} stacks em todos inimigos",Color .DIM ))
        if ext .get ("heal_per_turn_pct"):
            self .ui .tprint (c (f"   Cura/turno: +{int (ext ['heal_per_turn_pct']*100 )}% HP maximo",Color .DIM ))
        if ext .get ("stun_all_per_turn"):
            self .ui .tprint (c ("   STUN em todos inimigos enquanto ativo!",Color .DIM ))
        if ext .get ("post_duration_stun"):
            self .ui .tprint (c (f"   Apos acabar: alvo fica parado {ext ['post_duration_stun']}t e toma {int (ext .get ('post_duration_dmg_pct',0 )*100 )}% HP de dano",
            Color .DIM ))
        self .ui .pause ()

        self ._tick_active_domain (first_activation =True )

        if self .player .active_domain :
            self .player .active_domain ["ticked_this_turn"]=True 
        return None 

    def _tick_active_domain (self ,first_activation =False ):

        _ =first_activation
        if not self .player .active_domain :
            return 

        domain =self .player .active_domain 
        effect =domain ["effect"]
        ce_cost =domain ["ce_per_turn"]

        if self .player .ce_current <ce_cost :

            self .ui .tprint (c (f"\nCE insuficiente! {domain ['name']} se dissipa.",Color .YELLOW ))
            self ._apply_post_duration_effects (domain )
            self .player .active_domain =None 
            return 

        self .player .ce_current -=ce_cost 
        domain ["turns_active"]+=1 

        msgs =[]

        if "dmg_per_turn_min"in effect and "dmg_per_turn_max"in effect :
            sure_hit =effect .get ("sure_hit",True )
            for e in self .enemies :
                if e ["hp"]>0 :
                    dmg =random .randint (effect ["dmg_per_turn_min"],effect ["dmg_per_turn_max"])
                    if sure_hit :
                        actual =calculate_damage (dmg ,int (e .get ("def",0 )*0.5 ))
                    else :
                        actual =calculate_damage (dmg ,e .get ("def",0 ))
                    e ["hp"]-=actual
                    msgs .append (f"  {e ['name']} sofre {actual } de dano do dominio! (CERTeiro)" )

        if effect .get ("bleed_per_turn"):
            for e in self .enemies :
                if e ["hp"]>0 :
                    e ["bleed_stacks"]=e .get ("bleed_stacks",0 )+effect ["bleed_per_turn"]
            msgs .append (f"  Todos os inimigos ganham +{effect ['bleed_per_turn']} stacks de sangramento.")

        if effect .get ("stun_all_per_turn"):
            for e in self .enemies :
                if e ["hp"]>0 :
                    e ["stunned_turns"]=max (e .get ("stunned_turns",0 ),1 )
            msgs .append ("  Todos os inimigos estao atordoados pelo dominio!")

        if effect .get ("frame_lock_per_turn"):
            for e in self .enemies :
                if e ["hp"]>0 :
                    e ["frame_locks"]=e .get ("frame_locks",0 )+effect ["frame_lock_per_turn"]
                    if e .get ("frame_locks",0 )>=effect .get ("freeze_at_locks",3 ):
                        e ["stunned_turns"]=e .get ("stunned_turns",0 )+1 
                        msgs .append (f"  {e ['name']} foi CONGELADO pelo Time Cell Moon Palace!")

            self .player .frame_stacks =min (5 ,self .player .frame_stacks +1 )
            msgs .append (f"  Voce ganha +1 Frame Stack (total: {self .player .frame_stacks }).")

        if effect .get ("heal_per_turn_pct"):
            heal =int (self .player .max_hp *effect ["heal_per_turn_pct"])
            if not self .player .sukuna_takeover_active :
                self .player .hp =min (self .player .max_hp ,self .player .hp +heal )
                msgs .append (f"  +{heal } HP do dominio de sangue.")

        if msgs :
            for m in msgs :
                self .ui .tprint (c (m ,Color .BRIGHT_MAGENTA ))
            self .ui .pause ()

        if effect .get ("slot_machine"):
            domain ["spins_done"]=domain .get ("spins_done",0 )+1 
            max_spins =effect .get ("max_spins",3 )
            is_jackpot =random .random ()<effect .get ("jackpot_chance_per_spin",0.08 )
            symbols_pool =["BAR","CHERRY","BELL","STAR","TREM"]
            if is_jackpot :
                roll =["7","7","7"]
            else :
                roll =[random .choice (symbols_pool )for _ in range (3 )]
                if roll [0 ]==roll [1 ]==roll [2 ]:
                    roll [2 ]=random .choice ([s for s in symbols_pool if s !=roll [2 ]])
            self .ui .tprint (c (f"\n  [CACA-NIQUEIS] {' - '.join (roll )}",Color .BRIGHT_YELLOW +Color .BOLD ))
            if is_jackpot :
                self .ui .tprint (c ("  !!!!! JACKPOT 7-7-7 !!!!! Hakari se torna IMBATIVEL nesta batalha!",
                Color .BRIGHT_RED +Color .BOLD +Color .BLINK ))
                self .player .infinite_resources_active =True 
                self .player .hp =self .player .max_hp 
                self .player .ce_current =self .player .max_ce 
            self .ui .pause ()

            if domain .get ("spins_done",0 )>=max_spins and self .player .active_domain :
                self .ui .tprint (c (f"\n  A maquina de {domain ['name']} trava e quebra apos {max_spins } giros!",
                Color .DIM ))
                self ._apply_post_duration_effects (domain )
                self .player .active_domain =None 

    def _apply_post_duration_effects (self ,domain ):

        effect =domain .get ("effect",{})
        domain_name =domain .get ("name","Dominio")

        if effect .get ("post_duration_stun")or effect .get ("post_duration_dmg_pct"):
            self .ui .tprint (c (f"\n!! {domain_name } acabou - efeitos residuais! !!",
            Color .BRIGHT_MAGENTA +Color .BOLD ))
            for e in self .enemies :
                if e ["hp"]>0 :
                    if effect .get ("post_duration_stun"):
                        e ["stunned_turns"]=e .get ("stunned_turns",0 )+effect ["post_duration_stun"]
                        self .ui .tprint (c (f"  {e ['name']} fica parado por {effect ['post_duration_stun']} turnos!",
                        Color .YELLOW ))
                    if effect .get ("post_duration_dmg_pct"):
                        dmg =int (e ["max_hp"]*effect ["post_duration_dmg_pct"])
                        e ["hp"]-=dmg 
                        self .ui .tprint (c (f"  {e ['name']} sofre {dmg } de dano residual! ({int (effect ['post_duration_dmg_pct']*100 )}% HP max)",
                        Color .BRIGHT_RED ))
            self .ui .pause ()

    def execute_technique (self ,ext ,target ):

        self .ui .tprint (c (f"\n>> {self .player .name } usa {ext ['name']}!",Color .BRIGHT_MAGENTA +Color .BOLD ))
        self .ui .tprint (c (f"   {ext ['desc']}",Color .DIM ))
        time .sleep (0.5 )

        ttype =ext ["type"]

        if ext .get ("sukuna_skill"):
            skill_bonus =self .player .get_sukuna_skill_bonus ()
            if skill_bonus >0 :
                ext =dict (ext )
                ext ["dmg_mult"]=ext .get ("dmg_mult",1.0 )*(1.0 +skill_bonus )
                self .ui .tprint (c (f"  [Poder de Sukuna: {self .player .sukuna_fingers_eaten } dedos - "
                f"bonus x{1.0 +skill_bonus :.2f}]",Color .BRIGHT_RED +Color .BOLD ))

            if ext .get ("armor_pierce_pct_dynamic"):
                ext ["armor_pierce_pct"]=self .player .get_sukuna_def_ignore ()

                ce_reduction =self .player .sukuna_fingers_eaten *8 

                self .ui .tprint (c (f"  [Passiva Rei das Maldicoes: -{ce_reduction } CE custo, ignora {int (ext ['armor_pierce_pct']*100 )}% def]",
                Color .DIM ))

        if ttype =="attack":
            if ext .get ("requires_part")and not target .get ("nobara_bound"):
                has_part =any ("parte_do_alvo"in n or "Parte do Alvo"in n for n in self .player .inventory .keys ())
                if not has_part :
                    self .ui .tprint (c ("Voce precisa de uma Parte do Alvo para usar esta tecnica!",Color .RED ))
                    self .ui .pause ()
                    return None
                self .player .remove_item ("Parte do Alvo")
                self .ui .tprint (c ("Parte do Alvo consumida!",Color .DIM ))
            elif ext .get ("requires_part")and target .get ("nobara_bound"):
                self .ui .tprint (c ("O vinculo com o boneco ja esta ativo - nao precisa de outra Parte do Alvo!",
                Color .DIM ))
            if ext .get ("variable_dmg"):
                dmg_min ,dmg_max =ext ["variable_dmg"]
                base_dmg =random .randint (dmg_min ,dmg_max )
            else :
                dmg_mult =ext .get ("dmg_mult",1.5 )
                base_dmg =int (self .player .get_total_str ()*dmg_mult )

            if ext .get ("resonance_skill"):
                res_mult =self .player .get_buff_value ("resonance_mult")
                if res_mult >0 :
                    bonus_pct =res_mult /100.0
                    base_dmg =int (base_dmg *(1.0 +bonus_pct ))
                    self .ui .tprint (c (f"  (Hairbag amplifica Resonance: +{res_mult }% dano)",Color .BRIGHT_MAGENTA ))

            if ext .get ("bonus_vs_high_hp")and target .get ("hp",0 )>target .get ("max_hp",0 )*0.5 :
                base_dmg =int (base_dmg *1.5 )
                self .ui .tprint (c ("  (Bonus vs HP alto: +50% dano)",Color .DIM ))

            if ext .get ("bonus_vs_bleeding")and target .get ("bleed_stacks",0 )>0 :
                base_dmg =int (base_dmg *ext .get ("bonus_vs_bleeding",1.5 ))
                self .ui .tprint (c (f"  (Bonus vs sangrando: +{int ((ext .get ('bonus_vs_bleeding',1.5 )-1 )*100 )}% dano)",
                Color .DIM ))

            if ext .get ("bonus_vs_burning")and target .get ("burn_stacks",0 )>0 :
                base_dmg =int (base_dmg *1.5 )
                self .ui .tprint (c ("  (Bonus vs queimando: +50% dano)",Color .DIM ))

            if ext .get ("scales_with_missing_hp"):
                missing_pct =1.0 -(self .player .hp /max (1 ,self .player .max_hp ))
                rage_bonus =missing_pct *ext .get ("rage_mult",1.5 )
                base_dmg =int (base_dmg *(1.0 +rage_bonus ))
                if rage_bonus >0.05 :
                    self .ui .tprint (c (f"  (Rika sente seu desespero: +{int (rage_bonus *100 )}% dano)",
                    Color .BRIGHT_MAGENTA ))

            if ext .get ("gamble"):
                if random .random ()<ext .get ("gamble_win_chance",0.5 ):
                    base_dmg =int (base_dmg *ext .get ("gamble_high_mult",2.5 ))
                    self .ui .tprint (c ("  !! APOSTA GANHA !! Sorte maxima.",Color .BRIGHT_GREEN +Color .BOLD ))
                else :
                    base_dmg =int (base_dmg *ext .get ("gamble_low_mult",0.5 ))
                    self .ui .tprint (c ("  Aposta perdida... dano reduzido.",Color .DIM ))

            if target .get ("immune_physical")and not (ext .get ("armor_pierce")or ext .get ("soul_attack")):
                self .ui .tprint (c (f"{target ['name']} eh imune a dano fisico!",Color .YELLOW ))
                self .ui .pause ()
                return None 

            if target .get ("dmg_taken_mult",1.0 )<=0.0 and not ext .get ("infinity_bypass"):
                self .ui .tprint (c (f"O Infinito de {target ['name']} bloqueia totalmente a tecnica!",Color .BRIGHT_CYAN ))
                self .ui .tprint (c ("(Use World Cutting Slash para atravessar.)",Color .DIM ))
                self .ui .pause ()
                return None 

            if ext .get ("infinity_bypass")and target .get ("dmg_taken_mult",1.0 )<=0.0 :
                self .ui .tprint (c (f"!! {ext ['name']} ATRAVESSA O INFINITO !!",Color .BRIGHT_YELLOW +Color .BOLD ))

            effective_dodge =max (0 ,target .get ("dodge_chance",0 )-target .get ("dodge_penalty",0 ))
            if target .get ("can_dodge")and not ext .get ("guaranteed_hit")and random .random ()<effective_dodge :
                self .ui .tprint (c (f"\n{target ['name']} ESQUIVA da tecnica!",Color .BRIGHT_GREEN +Color .BOLD ))
                self .ui .pause ()
                return None 

            defended =False 
            if target .get ("can_defend")and not ext .get ("soul_attack")and random .random ()<target .get ("defense_chance",0 ):
                defended =True 
                self .ui .tprint (c (f"\n{target ['name']} se DEFENDE com CE!",Color .BRIGHT_CYAN ))

            if ext .get ("soul_attack")or ext .get ("armor_pierce"):

                actual =base_dmg 
                if ext .get ("soul_attack"):
                    self .ui .tprint (c ("(Dano espiritual ignora defesa!)",Color .MAGENTA ))

                    soul_heal =int (self .player .max_hp *0.05 )
                    if not self .player .sukuna_takeover_active :
                        self .player .hp =min (self .player .max_hp ,self .player .hp +soul_heal )
                        self .ui .tprint (c (f"+{soul_heal } HP (Forma da Alma)",Color .GREEN ))
            elif ext .get ("armor_pierce_pct"):
                def_ignore =ext ["armor_pierce_pct"]
                effective_def =int (target .get ("def",0 )*(1.0 -def_ignore ))
                actual =calculate_damage (base_dmg ,effective_def )
                self .ui .tprint (c (f"(Ignora {int (def_ignore *100 )}% defesa)",Color .DIM ))
            else :
                actual =calculate_damage (base_dmg ,target .get ("def",0 ))

            if defended :
                actual =int (actual *DEFENDED_DMG_REDUCTION )
                self .ui .tprint (c (f"(Dano reduzido pela defesa: {actual })",Color .DIM ))
                actual =max (1 ,actual )

            if target .get ("adaptive"):
                mahoraga_resist =mahoraga_mod .get_damage_reduction (target ,ext ["name"])
                if mahoraga_resist >0 :
                    actual =max (1 ,int (actual *(1.0 -mahoraga_resist )))

            if target .get ("ce_dmg_resist",0 )>0 and not ext .get ("soul_attack")and not ext .get ("armor_pierce"):
                actual =max (1 ,int (actual *(1.0 -target ["ce_dmg_resist"])))
                self .ui .tprint (c (
                f"(Restricao Celestial de {target ['name']} reduz dano de tecnicas amaldicoadas!)",
                Color .DIM ))

            target ["hp"]-=actual 
            if target .get ("adaptive"):
                mahoraga_mod .register_hit (target ,ext ["name"],ui_module =self .ui )
            else :
                self ._register_adaptation_hit (target ,"ce")
            hits =ext .get ("hits",1 )
            if hits >1 :
                for h in range (hits -1 ):
                    extra =calculate_damage (int (self .player .get_total_str ()*ext .get ("dmg_mult",1.5 )),target .get ("def",0 ))
                    if defended :
                        extra =max (1 ,int (extra *DEFENDED_DMG_REDUCTION ))
                    target ["hp"]-=extra 
                    actual +=extra 
                self .ui .tprint (c (f"({hits } hits! Dano total: {actual })",Color .BRIGHT_RED ))
            else :
                self .ui .tprint (c (f"Dano: {actual }",Color .BRIGHT_RED ))

            if ext .get ("bleed"):
                bleed_turns =ext .get ("bleed_turns",3 )
                b_resist =target .get ("bleed_resist",0.0 )
                if random .random ()>b_resist :
                    target ["bleed_stacks"]=target .get ("bleed_stacks",0 )+bleed_turns 
                    self .ui .tprint (c (f"{target ['name']} esta sangrando! (+{bleed_turns } stacks)",Color .RED ))
                    self ._register_adaptation_hit (target ,"bleed")
                else :
                    self .ui .tprint (c (f"{target ['name']} resiste ao sangramento!",Color .DIM ))

            if ext .get ("burn"):
                burn_turns =ext .get ("burn_turns",3 )
                bn_resist =target .get ("burn_resist",0.0 )
                if random .random ()>bn_resist :
                    target ["burn_stacks"]=target .get ("burn_stacks",0 )+burn_turns 
                    self .ui .tprint (c (f"{target ['name']} esta queimando! (+{burn_turns } stacks)",Color .BRIGHT_RED ))
                    self ._register_adaptation_hit (target ,"burn")
                else :
                    self .ui .tprint (c (f"{target ['name']} resiste a queimadura!",Color .DIM ))
            if ext .get ("poison"):
                poison_turns =ext .get ("poison_turns",3 )
                p_resist =target .get ("poison_resist",0.0 )
                if random .random ()>p_resist :
                    target ["poison_stacks"]=target .get ("poison_stacks",0 )+poison_turns 
                    self .ui .tprint (c (f"{target ['name']} foi envenenado! (+{poison_turns } stacks)",Color .GREEN ))
                else :
                    self .ui .tprint (c (f"{target ['name']} resiste ao veneno!",Color .DIM ))

            if ext .get ("stun_turns")and not ext .get ("stun_chance"):
                stun_resist =target .get ("stun_resist",0.0 )
                if random .random ()>stun_resist :
                    target ["stunned_turns"]=target .get ("stunned_turns",0 )+ext ["stun_turns"]
                    self .ui .tprint (c (f"{target ['name']} atordoado por {ext ['stun_turns']} turno(s)!",Color .YELLOW ))
                    self ._register_adaptation_hit (target ,"stun")
                else :
                    self .ui .tprint (c (f"{target ['name']} resiste ao atordoamento!",Color .DIM ))

            if ext .get ("stun_chance"):
                if random .random ()<ext ["stun_chance"]:
                    stun_resist =target .get ("stun_resist",0.0 )
                    if random .random ()>stun_resist :
                        target ["stunned_turns"]=target .get ("stunned_turns",0 )+ext .get ("stun_turns",1 )
                        self .ui .tprint (c (f"{target ['name']} atordoado!",Color .YELLOW ))
                        self ._register_adaptation_hit (target ,"stun")
                    else :
                        self .ui .tprint (c (f"{target ['name']} resiste ao atordoamento!",Color .DIM ))

            if ext .get ("applies_soul_mark"):
                target ["soul_marks"]=target .get ("soul_marks",0 )+ext ["applies_soul_mark"]
                self .ui .tprint (c (f"{target ['name']} recebe marca de Alma Distorcida! ({target ['soul_marks']} stacks)",
                Color .MAGENTA ))

            if ext .get ("consumes_soul_marks")and target .get ("soul_marks",0 )>0 :
                marks =target ["soul_marks"]
                bonus_per_mark =ext .get ("bonus_per_mark",0.30 )
                extra_dmg =int (actual *marks *bonus_per_mark )
                target ["hp"]-=extra_dmg
                self .ui .tprint (c (f"  +{extra_dmg } dano (consumiu {marks } marcas de alma, +{int (bonus_per_mark *100 )}%/marca)",Color .BRIGHT_MAGENTA ))
                if marks >=3 and ext .get ("stun_if_3_marks_turns"):
                    target ["stunned_turns"]=target .get ("stunned_turns",0 )+ext ["stun_if_3_marks_turns"]
                    self .ui .tprint (c (f"  {target ['name']} atordoado por consumir 3+ marcas!",Color .YELLOW ))
                target ["soul_marks"]=0 

            if ext .get ("applies_nail_mark"):
                mark_gain =ext ["applies_nail_mark"]
                if target .get ("nobara_bound"):
                    mark_gain +=1 
                target ["nail_marks"]=target .get ("nail_marks",0 )+mark_gain 
                self .ui .tprint (c (f"{target ['name']} recebe um prego amaldicoado no boneco de palha! ({target ['nail_marks']} pregos)",
                Color .BRIGHT_RED ))
                if target .get ("nobara_bound"):
                    self .ui .tprint (c ("  (Vinculo ativo: +1 prego bonus)",Color .DIM ))

            if ext .get ("applies_bond"):
                target ["nobara_bound"]=True 
                self .ui .tprint (c (f"O boneco de palha esta permanentemente vinculado a {target ['name']} - "
                "toda dor sentida por ele agora reflete direto no alvo, sem precisar de mais nenhuma Parte do Alvo!",
                Color .BRIGHT_RED +Color .BOLD ))

            if ext .get ("consumes_nail_marks")and target .get ("nail_marks",0 )>0 :
                marks =target ["nail_marks"]
                bonus_per_mark =ext .get ("bonus_per_nail_mark",0.40 )
                extra_dmg =int (actual *marks *bonus_per_mark )
                target ["hp"]-=extra_dmg
                self .ui .tprint (c (f"  RESSONANCIA! +{extra_dmg } dano (consumiu {marks } pregos, +{int (bonus_per_mark *100 )}%/prego)",
                Color .BRIGHT_RED +Color .BOLD ))
                if marks >=3 and ext .get ("stun_if_3_nails_turns"):
                    target ["stunned_turns"]=target .get ("stunned_turns",0 )+ext ["stun_if_3_nails_turns"]
                    self .ui .tprint (c (f"  {target ['name']} atordoado pela ressonancia!",Color .YELLOW ))
                target ["nail_marks"]=0 

                if target .get ("nobara_bound")and target ["hp"]<=0 :
                    ce_refund =int (self .player .max_ce *0.25 )
                    self .player .ce_current =min (self .player .max_ce ,self .player .ce_current +ce_refund )
                    self .ui .tprint (c (f"  O ritual se completa - o vinculo se rompe e devolve {ce_refund } CE!",
                    Color .BRIGHT_MAGENTA ))

            if ext .get ("applies_frame_lock"):
                target ["frame_locks"]=target .get ("frame_locks",0 )+ext ["applies_frame_lock"]
                self .ui .tprint (c (f"{target ['name']} recebe +{ext ['applies_frame_lock']} Frame Lock(s) (total: {target ['frame_locks']})",
                Color .YELLOW ))

                if target .get ("frame_locks",0 )>=3 and ext .get ("stun_if_3_locks_turns"):
                    target ["stunned_turns"]=target .get ("stunned_turns",0 )+ext ["stun_if_3_locks_turns"]
                    self .ui .tprint (c (f"  {target ['name']} congelado por 3 Frame Locks!",Color .BRIGHT_YELLOW ))

            if ext .get ("consumes_frame_stacks")and self .player .frame_stacks >0 :
                bonus_per_stack =ext .get ("bonus_per_stack",0.5 )
                extra_dmg =int (actual *self .player .frame_stacks *bonus_per_stack )
                target ["hp"]-=extra_dmg 
                self .ui .tprint (c (f"  +{extra_dmg } dano (consumiu {self .player .frame_stacks } Frame Stacks)",
                Color .BRIGHT_YELLOW ))
                self .player .frame_stacks =0 

            if ext .get ("debuff_def_pct"):
                debuff_val =int (target .get ("def",0 )*ext ["debuff_def_pct"])
                if "_original_def" not in target :
                    target ["_original_def"]=target .get ("def",0 )
                target ["def"]=max (0 ,target .get ("def",0 )-debuff_val )
                target .setdefault ("debuffs",[]).append ({
                "type":"def_debuff","value":debuff_val ,"duration":ext .get ("debuff_duration",3 ),
                "name":f"-{int (ext ['debuff_def_pct']*100 )}% DEF",
                })
                self .ui .tprint (c (f"  {target ['name']} perde {int (ext ['debuff_def_pct']*100 )}% defesa por {ext .get ('debuff_duration',3 )}t",
                Color .DIM ))
            if ext .get ("debuff_speed_pct"):
                debuff_val =int (target .get ("speed",0 )*ext ["debuff_speed_pct"])
                if "_original_speed" not in target :
                    target ["_original_speed"]=target .get ("speed",0 )
                target ["speed"]=max (1 ,target .get ("speed",0 )-debuff_val )
                target .setdefault ("debuffs",[]).append ({
                "type":"speed_debuff","value":debuff_val ,"duration":ext .get ("debuff_duration",3 ),
                "name":f"-{int (ext ['debuff_speed_pct']*100 )}% SPD",
                })
                self .ui .tprint (c (f"  {target ['name']} perde {int (ext ['debuff_speed_pct']*100 )}% velocidade",
                Color .DIM ))
            if ext .get ("debuff_dodge_pct"):
                target ["dodge_penalty"]=target .get ("dodge_penalty",0 )+ext ["debuff_dodge_pct"]
                self .ui .tprint (c (f"  {target ['name']} perde {int (ext ['debuff_dodge_pct']*100 )}% esquiva",
                Color .DIM ))

            if ext .get ("self_buff_dodge"):
                self .player .add_buff ("boogie_dodge",1 ,ext .get ("self_buff_duration",2 ),"Boogie Woogie")
                self .player .add_buff ("dodge_flat",int (ext ["self_buff_dodge"]*100 ),
                ext .get ("self_buff_duration",2 ),"Boogie Woogie")
            if ext .get ("self_buff_crit"):
                self .player .add_buff ("boogie_crit",1 ,ext .get ("self_buff_duration",2 ),"Boogie Woogie")

            if ext .get ("black_flash_chance"):
                if random .random ()<ext ["black_flash_chance"]:
                    bf_dmg =int (actual *BLACK_FLASH_DMG_MULT )
                    target ["hp"]-=bf_dmg 
                    self .ui .tprint (c (f"!! BLACK FLASH! +{bf_dmg } dano!",Color .BRIGHT_RED +Color .BOLD ))
                    self .ui .show_ascii (ui .ASCII_BLACK_FLASH ,color =Color .BRIGHT_RED ,clear =False )
                    self .ui .pause ()

            if ext .get ("instakill_below_pct"):
                if target ["hp"]/max (1 ,target ["max_hp"])<ext ["instakill_below_pct"]:
                    if random .random ()<0.5 :
                        target ["hp"]=0 
                        self .ui .tprint (c (f"!! {target ['name']} foi ANIQUILADO instanteamente!",
                        Color .BRIGHT_RED +Color .BOLD ))

            if ext .get ("instakill_below_rank"):
                if target .get ("rank")in ext ["instakill_below_rank"]:
                    target ["hp"]=0 
                    self .ui .tprint (c (f"!! {target ['name']} ({target .get ('rank')}) foi ANIQUILADO pelo 299 Seconds Run!",
                    Color .BRIGHT_RED +Color .BOLD ))

        elif ttype =="attack_aoe":
            dmg_mult =ext .get ("dmg_mult",1.5 )
            base_dmg =int (self .player .get_total_str ()*dmg_mult )

            if ext .get ("variable_dmg"):
                dmg_min ,dmg_max =ext ["variable_dmg"]
                base_dmg =random .randint (dmg_min ,dmg_max )

            for e in self .enemies :
                if e ["hp"]>0 :
                    if e .get ("immune_physical")and not (ext .get ("armor_pierce")or ext .get ("soul_attack")):
                        continue 
                    if ext .get ("soul_attack")or ext .get ("armor_pierce"):
                        actual =base_dmg 
                    elif ext .get ("armor_pierce_pct"):
                        effective_def =int (e .get ("def",0 )*(1.0 -ext ["armor_pierce_pct"]))
                        actual =calculate_damage (base_dmg ,effective_def )
                    else :
                        actual =calculate_damage (base_dmg ,e .get ("def",0 ))

                    if ext .get ("bonus_vs_bleeding")and e .get ("bleed_stacks",0 )>0 :
                        actual =int (actual *ext .get ("bonus_vs_bleeding",1.5 ))
                    if ext .get ("bonus_vs_burning")and e .get ("burn_stacks",0 )>0 :
                        actual =int (actual *1.5 )

                    e ["hp"]-=actual 
                    self .ui .tprint (c (f"  {e ['name']}: {actual } dano",Color .BRIGHT_RED ))

                    if ext .get ("bleed"):
                        e ["bleed_stacks"]=e .get ("bleed_stacks",0 )+ext .get ("bleed_turns",3 )
                    if ext .get ("burn"):
                        e ["burn_stacks"]=e .get ("burn_stacks",0 )+ext .get ("burn_turns",3 )
                    if ext .get ("stun_turns"):
                        if random .random ()<ext .get ("stun_chance",1.0 ):
                            stun_resist =e .get ("stun_resist",0.0 )
                            if random .random ()>stun_resist :
                                e ["stunned_turns"]=e .get ("stunned_turns",0 )+ext ["stun_turns"]
                                self .ui .tprint (c (f"    {e ['name']} atordoado!",Color .YELLOW ))
                            else :
                                self .ui .tprint (c (f"    {e ['name']} resiste ao atordoamento!",Color .DIM ))

                    if ext .get ("applies_soul_mark"):
                        e ["soul_marks"]=e .get ("soul_marks",0 )+ext ["applies_soul_mark"]

                    if ext .get ("applies_frame_lock"):
                        e ["frame_locks"]=e .get ("frame_locks",0 )+ext ["applies_frame_lock"]
                        if e .get ("frame_locks",0 )>=3 and ext .get ("stun_if_3_locks_turns"):
                            e ["stunned_turns"]=e .get ("stunned_turns",0 )+ext ["stun_if_3_locks_turns"]

                    if ext .get ("debuff_dodge_pct"):
                        e ["dodge_penalty"]=e .get ("dodge_penalty",0 )+ext ["debuff_dodge_pct"]

            if ext .get ("self_buff_dodge"):
                self .player .add_buff ("boogie_dodge",1 ,ext .get ("self_buff_duration",2 ),"Boogie Woogie")
                self .player .add_buff ("dodge_flat",int (ext ["self_buff_dodge"]*100 ),
                ext .get ("self_buff_duration",2 ),"Boogie Woogie")
            if ext .get ("self_buff_crit"):
                self .player .add_buff ("boogie_crit",1 ,ext .get ("self_buff_duration",2 ),"Boogie Woogie")

        elif ttype =="attack_chain":
            hits =ext .get ("hits",3 )
            alive_enemies =[e for e in self .enemies if e ["hp"]>0 ]
            for i in range (hits ):
                if not alive_enemies :
                    break 
                t =alive_enemies [i %len (alive_enemies )]
                dmg =int (self .player .get_total_str ()*ext .get ("dmg_mult",1.2 ))
                actual =calculate_damage (dmg ,t .get ("def",0 ))
                t ["hp"]-=actual 
                self .ui .tprint (c (f"  Hit {i +1 } -> {t ['name']}: {actual } dano",Color .BRIGHT_RED ))

        elif ttype =="stun":
            duration =ext .get ("duration",1 )
            stun_resist =target .get ("stun_resist",0.0 )
            if random .random ()>stun_resist :
                target ["stunned_turns"]=target .get ("stunned_turns",0 )+duration 
                self .ui .tprint (c (f"{target ['name']} atordoado por {duration } turno(s)!",Color .YELLOW ))
            else :
                self .ui .tprint (c (f"{target ['name']} resiste ao atordoamento!",Color .DIM ))

        elif ttype =="stun_chance":
            stun_chance =ext .get ("stun_chance",0.6 )
            if random .random ()<stun_chance :
                stun_resist =target .get ("stun_resist",0.0 )
                if random .random ()>stun_resist :
                    target ["stunned_turns"]=target .get ("stunned_turns",0 )+ext .get ("stun_turns",1 )
                    self .ui .tprint (c (f"{target ['name']} atordoado!",Color .YELLOW ))
                else :
                    self .ui .tprint (c (f"{target ['name']} resiste ao atordoamento!",Color .DIM ))
            dmg_mult =ext .get ("dmg_mult",1.0 )
            base_dmg =int (self .player .get_total_str ()*dmg_mult )

            if ext .get ("bonus_if_swapped_mult")and target .get ("was_swapped"):
                base_dmg =int (base_dmg *ext ["bonus_if_swapped_mult"]/dmg_mult )
                self .ui .tprint (c (f"  (Bonus vs trocado: {ext ['bonus_if_swapped_mult']}x)",Color .DIM ))

            actual =calculate_damage (base_dmg ,target .get ("def",0 ))
            target ["hp"]-=actual
            self .ui .tprint (c (f"Dano: {actual }",Color .BRIGHT_RED ))

        elif ttype =="debuff_dot":
            dmg =int (self .player .get_total_str ()*ext .get ("dmg_mult",1.0 ))
            actual =calculate_damage (dmg ,target .get ("def",0 ))
            target ["hp"]-=actual
            self .ui .tprint (c (f"Dano: {actual }",Color .BRIGHT_RED ))
            target ["bleed_stacks"]=target .get ("bleed_stacks",0 )+ext .get ("duration",3 )
            self .ui .tprint (c (f"{target ['name']} vai sofrer dano ao longo do tempo!",Color .RED ))

        elif ttype =="sleep":
            stun_resist =target .get ("stun_resist",0.0 )
            if random .random ()<0.6 and random .random ()>stun_resist :
                target ["stunned_turns"]=target .get ("stunned_turns",0 )+ext .get ("duration",2 )
                self .ui .tprint (c (f"{target ['name']} adormeceu!",Color .YELLOW ))
            else :
                self .ui .tprint (c (f"{target ['name']} resistiu!",Color .DIM ))

        elif ttype =="lifesteal":
            dmg =int (self .player .get_total_str ()*ext .get ("dmg_mult",1.5 ))
            actual =calculate_damage (dmg ,target .get ("def",0 ))
            target ["hp"]-=actual 
            heal =int (actual *ext .get ("lifesteal_pct",0.5 ))
            self .player .hp =min (self .player .max_hp ,self .player .hp +heal )
            self .ui .tprint (c (f"Dano: {actual }, cura: +{heal } HP",Color .BRIGHT_GREEN ))

        elif ttype =="heal":
            heal_pct =ext .get ("heal_pct",0.30 )
            heal =int (self .player .max_hp *heal_pct )
            if ext .get ("extra_heal_per_bleeding_enemy"):
                bleeding_count =sum (1 for e in self .enemies if e .get ("bleed_stacks",0 )>0 )
                extra =int (self .player .max_hp *ext ["extra_heal_per_bleeding_enemy"]*bleeding_count )
                heal +=extra 
                self .ui .tprint (c (f"  +{extra } HP extra ({bleeding_count } inimigo(s) sangrando)",Color .GREEN ))
            self .player .hp =min (self .player .max_hp ,self .player .hp +heal )
            self .ui .tprint (c (f"+{heal } HP",Color .BRIGHT_GREEN ))
            if ext .get ("remove_self_bleed")and self .player .bleed_stacks >0 :
                self .player .bleed_stacks =0 
                self .ui .tprint (c ("Sangramento removido!",Color .BRIGHT_GREEN ))
            if ext .get ("self_dmg_pct"):
                sd =int (self .player .max_hp *ext ["self_dmg_pct"])
                self .player .hp -=sd 
                self .ui .tprint (c (f"-{sd } HP (custo)",Color .RED ))

        elif ttype =="heal_ally":
            alive_allies =[a for a in self .allies if a ["hp"]>0 ]
            if alive_allies :
                opts =[a ["name"]for a in alive_allies ]+["Voce"]
                idx =self .ui .arrow_menu (opts ,title ="Quem curar?")
                if idx ==len (alive_allies ):
                    heal =int (self .player .max_hp *ext .get ("heal_pct",0.25 ))
                    self .player .hp =min (self .player .max_hp ,self .player .hp +heal )
                    self .ui .tprint (c (f"+{heal } HP",Color .BRIGHT_GREEN ))
                elif idx >=0 :
                    target_a =alive_allies [idx ]
                    heal =int (target_a ["max_hp"]*ext .get ("heal_pct",0.25 ))
                    target_a ["hp"]=min (target_a ["max_hp"],target_a ["hp"]+heal )
                    self .ui .tprint (c (f"+{heal } HP para {target_a ['name']}",Color .BRIGHT_GREEN ))

        elif ttype =="buff":
            buff =ext .get ("buff","attack")
            mult =ext .get ("buff_mult",1.5 )
            buff_value =ext .get ("buff_value")
            duration =ext .get ("duration",3 )
            if buff_value is not None :
                flat_val =buff_value
            else :
                flat_val =int ((mult -1 )*100 )
            self .player .add_buff (buff ,flat_val ,duration ,ext ["name"])
            self .ui .tprint (c (f"+{flat_val } {buff } por {duration } turnos",Color .BRIGHT_CYAN ))
            if ext .get ("speed_mult"):
                self .player .add_buff ("speed",int ((ext ["speed_mult"]-1 )*100 ),duration ,ext ["name"])
            if ext .get ("dodge_bonus"):
                self .player .add_buff ("dodge_flat",int (ext ["dodge_bonus"]*100 ),duration ,ext ["name"])

        elif ttype =="buff_def":
            duration =ext .get ("duration",2 )
            buff_val =ext .get ("buff_value",30 )
            self .player .add_buff ("def",buff_val ,duration ,ext ["name"])
            ce_per_turn =ext .get ("ce_per_turn",0 )
            if ce_per_turn >0 :
                self .player .add_buff ("ce_drain",ce_per_turn ,duration ,ext ["name"])
                self .ui .tprint (c (f"+{buff_val } defesa por {duration } turnos (-{ce_per_turn } CE/turno)",Color .BRIGHT_CYAN ))
            else :
                self .ui .tprint (c (f"+{buff_val } defesa por {duration } turnos",Color .BRIGHT_CYAN ))

        elif ttype =="buff_dodge":
            duration =ext .get ("duration",1 )
            self .player .add_buff ("dodge_flat",30 ,duration ,ext ["name"])
            self .ui .tprint (c (f"+30% esquiva por {duration } turno(s)",Color .BRIGHT_CYAN ))

        elif ttype =="buff_weapon":
            duration =ext .get ("duration",3 )
            self .player .add_buff ("attack_flat",15 ,duration ,ext ["name"])
            self .ui .tprint (c (f"+15 ATK por {duration } turnos",Color .BRIGHT_CYAN ))

        elif ttype =="counter_dodge":
            self .player .add_buff ("dodge_flat",50 ,1 ,"Counter Stance")
            self .ui .tprint (c ("Postura de contra-ataque!",Color .BRIGHT_CYAN ))

        elif ttype =="swap":
            self .ui .tprint (c ("*CLAP* Boogie Woogie! Posicoes trocadas!",Color .YELLOW ))
            if target and ext .get ("stun_turns"):
                stun_resist =target .get ("stun_resist",0.0 )
                if random .random ()>stun_resist :
                    target ["stunned_turns"]=target .get ("stunned_turns",0 )+ext ["stun_turns"]
                    target ["was_swapped"]=True 
                    self .ui .tprint (c (f"{target ['name']} perde o proximo turno!",Color .YELLOW ))
                else :
                    self .ui .tprint (c (f"{target ['name']} resiste ao atordoamento do swap!",Color .DIM ))

            if ext .get ("self_buff_dodge"):
                self .player .add_buff ("boogie_dodge",1 ,ext .get ("self_buff_duration",2 ),"Boogie Woogie")
                self .player .add_buff ("dodge_flat",int (ext ["self_buff_dodge"]*100 ),
                ext .get ("self_buff_duration",2 ),"Boogie Woogie")
            if ext .get ("self_buff_crit"):
                self .player .add_buff ("boogie_crit",1 ,ext .get ("self_buff_duration",2 ),"Boogie Woogie")

        elif ttype =="swap_protect":
            alive_allies =[a for a in self .allies if a ["hp"]>0 ]
            if alive_allies and target :
                target_a =min (alive_allies ,key =lambda a :a ["hp"])
                target_a ["hp"]=min (target_a ["max_hp"],target_a ["hp"]+int (target_a ["max_hp"]*0.2 ))
                self .ui .tprint (c (f"{target_a ['name']} foi protegido!",Color .BRIGHT_GREEN ))
                if ext .get ("stun_turns"):
                    stun_resist =target .get ("stun_resist",0.0 )
                    if random .random ()>stun_resist :
                        target ["stunned_turns"]=target .get ("stunned_turns",0 )+ext ["stun_turns"]
                        self .ui .tprint (c (f"{target ['name']} atordoado pela troca!",Color .YELLOW ))
                    else :
                        self .ui .tprint (c (f"{target ['name']} resiste ao atordoamento!",Color .DIM ))
                if ext .get ("ally_dodge_bonus"):
                    target_a ["dodge_bonus"]=target_a .get ("dodge_bonus",0 )+ext ["ally_dodge_bonus"]

        elif ttype =="summon_shikigami":

            shikigami_id =ext .get ("shikigami_id")
            if not shikigami_id :
                self .ui .tprint (c ("Erro: shikigami_id ausente.",Color .RED ))
                self .ui .pause ()
                return None 

            if shikigami_id =="Merged Beast":
                if "Eight-Handled Sword Mahoraga"not in self .player .tamed_shikigami :
                    self .ui .tprint (c ("Merged Beast requer Mahoraga domado!",Color .RED ))
                    self .ui .pause ()
                    return None 

            shikigami_data =SHIKIGAMI_DB .get (shikigami_id )
            if not shikigami_data :
                self .ui .tprint (c (f"Shikigami {shikigami_id } nao encontrado.",Color .RED ))
                self .ui .pause ()
                return None 

            extra_ce_cost =0 
            if shikigami_id =="Round Deer":
                extra_ce_cost =200 
                if self .player .ce_current <extra_ce_cost :
                    self .ui .tprint (c ("CE insuficiente para Round Deer (precisa de 250 CE).",Color .RED ))
                    self .ui .pause ()
                    return None 

            if shikigami_id =="Eight-Handled Sword Mahoraga"and shikigami_id not in self .player .tamed_shikigami :
                self .ui .tprint (c ("\n!! RITUAL DE DOMINACAO DE MAHORAGA !!",Color .BRIGHT_RED +Color .BOLD +Color .BLINK ))
                self .ui .tprint (c ("Voce invoca Mahoraga pela primeira vez. Ele se volta contra voce!",Color .BRIGHT_RED ))
                self .ui .tprint (c ("Derrote-o ou morra!",Color .RED ))
                self .ui .pause ()

                mahoraga_enemy =create_active_shikigami (shikigami_id ,self .player .level_system .level )
                mahoraga_enemy ["is_ally"]=False 
                mahoraga_enemy ["is_enemy"]=True 
                mahoraga_enemy ["is_shikigami"]=False 
                mahoraga_enemy ["name"]="Mahoraga (Indomado)"
                mahoraga_enemy ["rank"]="Grau Especial"
                mahoraga_enemy ["max_hp"]=mahoraga_enemy ["hp"]
                mahoraga_enemy ["max_ce"]=mahoraga_enemy .get ("max_ce",100 )
                mahoraga_enemy ["ce"]=mahoraga_enemy .get ("ce",100 )
                mahoraga_enemy ["xp"]=2000 
                mahoraga_enemy ["is_boss"]=True 
                mahoraga_enemy ["ai_type"]="adaptive_tank"
                mahoraga_enemy ["extensions_known"]=["Espada da Roda","Punho Adaptativo"]
                mahoraga_enemy ["phases"]=[
                {"hp_pct_below":0.5 ,"buff":{"atk":1.3 ,"def":1.3 },
                "msg":"Mahoraga adapta-se aos seus ataques!","applied":False },
                ]
                mahoraga_enemy ["drops"]=["Cristal de CE","Cristal de CE"]
                mahoraga_enemy ["karma_reward"]=5 

                ritual_combat =Combat (self .player ,[mahoraga_enemy ],[],
                ui_module =self .ui ,allow_flee =False )
                result =ritual_combat .start ()
                if result =="victory":
                    self .ui .tprint (c ("\n!! VOCE DOMOU MAHORAGA !!",Color .BRIGHT_YELLOW +Color .BOLD +Color .BLINK ))
                    self .ui .tprint (c ("O shikigami mais poderoso agora responde a voce.",Color .BRIGHT_GREEN ))
                    if shikigami_id not in self .player .tamed_shikigami :
                        self .player .tamed_shikigami .append (shikigami_id )
                    self .ui .pause ()
                    return None 
                else :
                    self .ui .tprint (c ("\nVoce falhou em domar Mahoraga. Ele te destruiu.",Color .BRIGHT_RED +Color .BOLD ))
                    self .ui .pause ()
                    return result 

            instance =create_active_shikigami (shikigami_id ,self .player .level_system .level )
            if not instance :
                self .ui .tprint (c ("Falha ao invocar shikigami.",Color .RED ))
                self .ui .pause ()
                return None 

            if extra_ce_cost >0 :
                self .player .ce_current -=extra_ce_cost 

            on_invoke =shikigami_data .get ("on_invoke")
            if on_invoke =="stun_inimigo_2turnos":

                alive_enemies =[e for e in self .enemies if e ["hp"]>0 ]
                if alive_enemies :
                    t =max (alive_enemies ,key =lambda e :e ["hp"])
                    t ["stunned_turns"]=t .get ("stunned_turns",0 )+2 
                    self .ui .tprint (c (f"{instance ['name']} salta em {t ['name']} - atordoado por 2 turnos!",
                    Color .BRIGHT_YELLOW ))
            elif on_invoke =="dano_queda_31_a_60":

                alive_enemies =[e for e in self .enemies if e ["hp"]>0 ]
                if alive_enemies :
                    t =max (alive_enemies ,key =lambda e :e ["hp"])
                    fall_dmg =random .randint (31 ,60 )
                    fall_actual =calculate_damage (fall_dmg ,t .get ("def",0 ))
                    t ["hp"]-=fall_actual
                    self .ui .tprint (c (f"{instance ['name']} cai em cima de {t ['name']}! {fall_actual } dano!",
                    Color .BRIGHT_RED +Color .BOLD ))
            elif on_invoke =="cura_100_hp":

                heal =100 
                self .player .hp =min (self .player .max_hp ,self .player .hp +heal )
                self .ui .tprint (c (f"{instance ['name']} emite luz benevolente - +{heal } HP!",Color .BRIGHT_GREEN ))
                self .ui .tprint (c (f"{instance ['name']} se dissipa apos curar.",Color .DIM ))
                self .ui .pause ()
                return None 
            elif on_invoke =="fuga_garantida_2turnos":

                self .ui .tprint (c (f"\n!! {instance ['name']} cria uma horda de coelhos !!",Color .BRIGHT_CYAN ))
                self .ui .tprint (c ("AVISO: Voce podera fugir da batalha em 2 turnos.",Color .YELLOW ))
                self .ui .tprint (c ("(Use 'Fugir' nos proximos 2 turnos para escapar garantidamente.)",Color .DIM ))

                self .player .add_buff ("guaranteed_flee_pending",1 ,2 ,"Rabbit Escape")

                self .ui .pause ()
                return None 

            if hasattr (self ,"active_shikigamis")and len (self .active_shikigamis )>=1 :
                self .ui .tprint (c ("Voce ja tem um shikigami ativo! So 1 por vez.",Color .YELLOW ))
                self .ui .pause ()
                return None 

            instance ["is_ally"]=True 
            instance ["is_shikigami"]=True 
            if not hasattr (self ,"active_shikigamis"):
                self .active_shikigamis =[]
            self .active_shikigamis .append (instance )

            self .ui .tprint (c (f"\n{instance ['name']} invocado! ({instance ['hp']}/{instance ['max_hp']} HP, "
            f"{instance ['atk']} ATK)",Color .BRIGHT_BLACK +Color .BOLD ))
            self .ui .tprint (c (f"Custo de manutencao: {instance .get ('ce_cost_per_turn',0 )} CE/turno",Color .DIM ))
            self .ui .pause ()
            return None 

        elif ttype =="copy_technique":
            self .ui .tprint (c ("Yuta observa atentamente os movimentos do inimigo...",Color .BRIGHT_MAGENTA ))
            source_moves =list (target .get ("abilities",[]))
            if target .get ("adaptive"):
                source_moves .append ({"name":"Adaptacao de Mahoraga (copiada)","dmg_mult":2.5 ,"effect":None })

            dmg =int (self .player .get_total_str ()*ext .get ("dmg_mult",2.0 ))
            actual =calculate_damage (dmg ,target .get ("def",0 ))
            target ["hp"]-=actual 

            if not source_moves :
                self .ui .tprint (c (f"Nao havia nada de especial para copiar - mesmo assim, {actual } dano.",
                Color .DIM ))
            else :
                copied =random .choice (source_moves )
                copy_cost =ext .get ("copy_ce_cost",180 )
                self .player .copied_technique ={
                "name":copied ["name"],
                "dmg_mult":copied .get ("dmg_mult",2.0 ),
                "effect":copied .get ("effect"),
                "effect_value":copied .get ("effect_value",0 ),
                "ce_cost":copy_cost ,
                "source_adaptive":bool (target .get ("adaptive")),
                }
                adaptive_note =" (inclusive o rastro de adaptacao dela!)"if target .get ("adaptive")else "" 
                self .ui .tprint (c (f"Yuta copia '{copied ['name']}' de {target ['name']}{adaptive_note }!",
                Color .BRIGHT_MAGENTA +Color .BOLD ))
                self .ui .tprint (c (f"(Disponivel como 'Usar Copia' - custa {copy_cost } CE por uso)",Color .DIM ))
                self .ui .tprint (c (f"Golpe de observacao: {actual } dano.",Color .BRIGHT_RED ))

        elif ttype =="summon_rika":
            if getattr (self .player ,"rika_summoned",False ):
                self .ui .tprint (c ("Rika ja esta manifestada!",Color .YELLOW ))
            else :
                form =ext .get ("rika_form","incomplete")
                if form =="complete":
                    rika ={
                    "name":"Rika (Forma Completa)",
                    "hp":int (self .player .max_hp *1.2 ),"max_hp":int (self .player .max_hp *1.2 ),
                    "atk":int (self .player .get_total_str ()*2.2 ),
                    "def":int (self .player .get_total_def ()*0.8 ),
                    "speed":int (self .player .get_total_speed ()*1.2 ),
                    "ce":999999 ,"max_ce":999999 ,
                    "ai_type":"rika_random","black_flash_chance":0.20 ,
                    "is_rika_summon":True ,
                    }
                    ce_upkeep =45 
                else :
                    rika ={
                    "name":"Rika (Forma Incompleta)",
                    "hp":int (self .player .max_hp *0.6 ),"max_hp":int (self .player .max_hp *0.6 ),
                    "atk":int (self .player .get_total_str ()*1.3 ),
                    "def":int (self .player .get_total_def ()*0.5 ),
                    "speed":self .player .get_total_speed (),
                    "ce":999999 ,"max_ce":999999 ,
                    "ai_type":"rika_random","black_flash_chance":0.10 ,
                    "is_rika_summon":True ,
                    }
                    ce_upkeep =15 
                self .allies .append (rika )
                self .player .rika_summoned =True 
                self .player .rika_ce_upkeep =ce_upkeep 
                self .ui .tprint (c (f"!! {rika ['name']} se manifesta ao seu lado !!",Color .BRIGHT_MAGENTA +Color .BOLD ))
                self .ui .tprint (c (f"(Consome {ce_upkeep } CE por turno enquanto ativa)",Color .DIM ))

        elif ttype =="summon":
            self .ui .tprint (c ("Shikigami convocado!",Color .BRIGHT_BLACK ))
            dmg =int (self .player .get_total_str ()*ext .get ("dmg_mult",1.0 )+20 )
            alive_enemies =[e for e in self .enemies if e ["hp"]>0 ]
            if alive_enemies :
                t =random .choice (alive_enemies )
                actual =calculate_damage (dmg ,t .get ("def",0 ))
                t ["hp"]-=actual
                self .ui .tprint (c (f"Shikigami ataca {t ['name']}: {actual } dano",Color .BRIGHT_RED ))

        elif ttype =="summon_boss":

            self .ui .tprint (c ("!! INVOCACAO DE MAHORAGA !!",Color .BRIGHT_RED +Color .BOLD ))
            self .ui .tprint (c ("A roda divina gira. PRIMEIRO ADAPTACAO.",Color .BRIGHT_RED ))
            self .ui .pause ()
            alive_enemies =[e for e in self .enemies if e ["hp"]>0 ]
            if alive_enemies :
                t =max (alive_enemies ,key =lambda e :e ["hp"])
                dmg =int (self .player .get_total_str ()*ext .get ("dmg_mult",3.0 )+100 )
                actual =calculate_damage (dmg ,t .get ("def",0 ))
                t ["hp"]-=actual
                self .ui .tprint (c (f"Mahoraga devasta {t ['name']}: {actual } dano!",Color .BRIGHT_RED ))

            if random .random ()<0.30 :
                self .ui .tprint (c ("Mahoraga se volta contra voce!",Color .BRIGHT_RED +Color .BOLD ))
                dmg_to_player =int (self .player .max_hp *0.4 )
                self .player .hp -=dmg_to_player 
                self .ui .tprint (c (f"Voce toma {dmg_to_player } de dano!",Color .RED ))

        elif ttype =="trap":

            self .ui .tprint (c ("Armadilha plantada! Explode no proximo turno.",Color .YELLOW ))
            self .player .add_buff ("trap_armed",ext .get ("dmg_mult",1.5 ),1 ,"Armadilha")

        elif ttype =="ce_drain_on_hit":
            dmg =int (self .player .get_total_str ()*ext .get ("dmg_mult",1.2 ))
            actual =calculate_damage (dmg ,target .get ("def",0 ))
            target ["hp"]-=actual 
            drain_amt =ext .get ("ce_drain",5 )
            if target .get ("ce",0 )>0 :
                target ["ce"]=max (0 ,target ["ce"]-drain_amt )
                self .ui .tprint (c (f"Dano: {actual } | Drenou {drain_amt } CE de {target ['name']}",Color .BRIGHT_RED ))
            else :
                self .ui .tprint (c (f"Dano: {actual }",Color .BRIGHT_RED ))

        if ext .get ("self_dmg_pct")and ttype not in ("heal",):
            sd =int (self .player .max_hp *ext ["self_dmg_pct"])
            self .player .hp -=sd 
            if self .player .hp <0 :self .player .hp =0 
            self .ui .tprint (c (f"-{sd } HP (dano auto-infligido)",Color .RED ))

        if ext .get ("throat_dmg"):
            self .player .hp -=ext ["throat_dmg"]
            self .ui .tprint (c (f"-{ext ['throat_dmg']} HP (dano a garganta)",Color .RED ))

        self .ui .pause ()
        return None 

    def player_use_copied_technique (self ):

        copied =getattr (self .player ,"copied_technique",None )
        if not copied :
            self .ui .tprint (c ("Nenhuma tecnica copiada disponivel.",Color .RED ))
            self .ui .pause ()
            return None 

        if self .player .ce_current <copied ["ce_cost"]:
            self .ui .tprint (c (f"CE insuficiente! A copia exige {copied ['ce_cost']} CE.",Color .RED ))
            self .ui .pause ()
            return None 

        alive_enemies =[e for e in self .enemies if e ["hp"]>0 ]
        if not alive_enemies :
            return None 
        if len (alive_enemies )==1 :
            target =alive_enemies [0 ]
        else :
            opts =[e ["name"]for e in alive_enemies ]
            idx =self .ui .arrow_menu (opts ,title ="Usar copia em qual alvo?")
            if idx <0 :
                return None 
            target =alive_enemies [idx ]

        self .player .ce_current -=copied ["ce_cost"]

        dmg =int (self .player .get_total_str ()*copied .get ("dmg_mult",2.0 ))
        actual =calculate_damage (dmg ,target .get ("def",0 ))
        target ["hp"]-=actual 
        self .ui .tprint (c (f"\nYuta reproduz '{copied ['name']}' contra {target ['name']}: {actual } dano!",
        Color .BRIGHT_MAGENTA +Color .BOLD ))

        effect =copied .get ("effect")
        if effect =="bleed":
            target ["bleed_stacks"]=target .get ("bleed_stacks",0 )+copied .get ("effect_value",3 )
            self .ui .tprint (c (f"{target ['name']} esta sangrando!",Color .RED ))
        elif effect =="burn":
            target ["burn_stacks"]=target .get ("burn_stacks",0 )+copied .get ("effect_value",3 )
            self .ui .tprint (c (f"{target ['name']} esta queimando!",Color .BRIGHT_RED ))
        elif effect =="stun":
            if random .random ()>target .get ("stun_resist",0.0 ):
                target ["stunned_turns"]=target .get ("stunned_turns",0 )+copied .get ("effect_value",1 )
                self .ui .tprint (c (f"{target ['name']} foi atordoado!",Color .YELLOW ))

        if copied .get ("source_adaptive"):
            self .ui .tprint (c ("(A copia carrega um rastro instavel da adaptacao original.)",Color .DIM ))

        self .ui .pause ()
        return None 

    def player_dodge (self ):

        speed =self .player .get_total_speed ()
        ce_cost =10 if speed >=15 else DODGE_CE_COST 
        if self .player .ce_current <ce_cost :
            self .ui .tprint (c ("CE insuficiente para esquiva!",Color .RED ))
            self .ui .pause ()
            return None 
        self .player .ce_current -=ce_cost 

        dodge_bonus =min (70 ,DODGE_BASE_BONUS +(speed //5 )*5 )

        result =keyboard_input .reaction_minigame (self .ui ,wait_min =0.5 ,wait_max =1.4 ,window =0.55 ,
        prompt_wait ="\nFique atento aos movimentos do inimigo...",
        prompt_go ="ESQUIVA AGORA!! (aperte qualquer tecla)",difficulty =self ._reaction_difficulty ())

        if result =="success":
            dodge_bonus =min (95 ,dodge_bonus +25 )
            self .ui .tprint (c (f"\nReflexo perfeito! +{dodge_bonus }% esquiva este turno.",
            Color .BRIGHT_GREEN +Color .BOLD ))
        elif result in ("too_early","too_late"):
            self .ui .tprint (c (f"\nVoce hesitou! Esquiva normal: +{dodge_bonus }% este turno.",
            Color .YELLOW ))
        else :
            self .ui .tprint (c (f"\nVoce se prepara para esquivar! +{dodge_bonus }% esquiva este turno.",
            Color .BRIGHT_CYAN ))

        self .player .add_buff ("dodge_flat",dodge_bonus ,1 ,"Esquiva")
        self .player .add_buff ("black_flash_focus",5 ,1 ,"Concentracao")
        self .ui .tprint (c ("(Concentracao aumentada)",Color .DIM ))

        self .player_hit_streak =0 
        self .ui .pause ()
        return None 

    def player_parry (self ):

        ce_cost =REINFORCE_CE_COST 
        if self .player .ce_current <ce_cost :
            self .ui .tprint (c ("CE insuficiente para o contra-golpe!",Color .RED ))
            self .ui .pause ()
            return None 
        self .player .ce_current -=ce_cost 

        result =keyboard_input .reaction_minigame (self .ui ,wait_min =0.5 ,wait_max =1.5 ,window =0.45 ,
        prompt_wait ="\nVoce se posiciona, esperando o golpe do inimigo...",
        prompt_go ="PARRY AGORA!! (aperte qualquer tecla)",difficulty =self ._reaction_difficulty ())

        success =result =="success"

        if success :
            self .player .add_buff ("incoming_dmg_reduction_pct",90 ,1 ,"Parry")
            alive_enemies =[e for e in self .enemies if e ["hp"]>0 ]
            if alive_enemies :
                target =random .choice (alive_enemies )
                counter_dmg =calculate_damage (int (self .player .get_total_str ()*2.0 ),target .get ("def",0 ))
                target ["hp"]-=counter_dmg 
                self .ui .tprint (c (f"\n!! CONTRA-GOLPE PERFEITO !! Voce bloqueia 90% do proximo dano "
                f"e acerta {target ['name']} de volta: {counter_dmg } dano!",Color .BRIGHT_GREEN +Color .BOLD ))
            else :
                self .ui .tprint (c ("\n!! CONTRA-GOLPE PERFEITO !! Voce bloqueia 90% do proximo dano recebido.",
                Color .BRIGHT_GREEN +Color .BOLD ))
        else :
            self .player .add_buff ("incoming_dmg_pct",15 ,1 ,"Aberto")
            self .ui .tprint (c ("\nVoce erra o timing do contra-golpe e fica exposto! (+15% dano recebido)",
            Color .RED ))

        self .ui .pause ()
        return None 

    def player_ce_reinforce (self ):

        ce_cost =REINFORCE_CE_COST 
        if self .player .ce_current <ce_cost :
            self .ui .tprint (c ("CE insuficiente!",Color .RED ))
            self .ui .pause ()
            return None 
        self .player .ce_current -=ce_cost 
        self .player .add_buff ("def",REINFORCE_DEF_BONUS ,2 ,"Reforco de CE")
        self .ui .tprint (c (f"Voce reforca seu corpo com CE! +{REINFORCE_DEF_BONUS } defesa por 2 turnos.",
        Color .BRIGHT_CYAN ))

        tech =self .player .innate_technique 
        if tech =="Limitless":
            self .player .add_buff ("dodge_flat",20 ,2 ,"Campo Infinito")
            self .ui .tprint (c ("+20% esquiva (Campo Infinito) por 2 turnos",Color .BRIGHT_CYAN ))
        elif tech =="Dez Sombras":
            self .player .add_buff ("shadow_shield",1 ,2 ,"Sombra Protetora")
            self .ui .tprint (c ("Sombra protetora absorve o proximo ataque!",Color .BRIGHT_CYAN ))
        elif tech =="Manipulacao de Sangue":
            self .player .add_buff ("def",50 ,2 ,"Armadura de Sangue")
            self .player .add_debuff ("speed_down",10 ,2 ,"Armadura de Sangue")
            self .ui .tprint (c ("+50 defesa mas -10% velocidade (Armadura de Sangue)",Color .RED ))
        elif tech =="Idle Transfiguration":
            self .player .add_buff ("soul_distort_def",1 ,2 ,"Distorcao da Alma")
            self .ui .tprint (c ("30% chance de refletir 20% do dano (Distorcao da Alma)",Color .MAGENTA ))
        elif tech =="Projection Sorcery":
            self .player .add_buff ("frame_guard",1 ,2 ,"Protecao de Frames")
            self .ui .tprint (c ("Imune a stun por 2 turnos (Protecao de Frames)",Color .BRIGHT_YELLOW ))

        self .player_hit_streak =0 
        self .ui .pause ()
        return None 

    def player_use_item (self ):

        consumables =self .player .get_items_by_type ("consumivel")
        if not consumables :
            self .ui .tprint (c ("Voce nao tem itens consumiveis!",Color .YELLOW ))
            self .ui .pause ()
            return None 
        opts =list (consumables .keys ())
        opts .append ("Voltar")
        idx =self .ui .arrow_menu (opts ,title ="Itens:")
        if idx <0 or idx ==len (opts )-1 :
            return None 
        item_name =opts [idx ]
        result =self .player .use_consumable (item_name ,ui_module =self .ui )
        if result is False :
            self .ui .pause ()
            return "retry"
        self .ui .pause ()
        return None 

    def player_flee (self ):

        if not self .allow_flee :
            self .ui .tprint (c ("Voce nao pode fugir desta batalha!",Color .RED ))
            self .ui .pause ()
            return None 

        if self .player .get_buff_value ("guaranteed_flee_pending")>0 :
            self .ui .tprint (c ("Coelhos de sombra criam uma rotta de fuga!",Color .BRIGHT_CYAN ))
            self .ui .tprint (c ("Voce escapa com sucesso!",Color .BRIGHT_GREEN ))
            self .ui .pause ()
            return "fled"

        alive =[e for e in self .enemies if e .get ("hp",0 )>0 ]
        if not alive :
            return "fled"
        fastest_enemy =max (alive ,key =lambda e :e .get ("speed",10 ))
        player_speed =self .player .get_total_speed ()
        flee_chance =0.4 +(player_speed -fastest_enemy .get ("speed",10 ))*0.02 
        flee_chance =max (0.1 ,min (0.9 ,flee_chance ))

        if self .player .has_item ("Pergaminho de Fuga"):
            flee_chance =1.0 
            self .player .remove_item ("Pergaminho de Fuga")
            self .ui .tprint (c ("Pergaminho de Fuga usado!",Color .BRIGHT_GREEN ))

        self .ui .tprint (c (f"Tentando fugir... ({int (flee_chance *100 )}%)",Color .YELLOW ))
        self .ui .pause ()
        if random .random ()<flee_chance :
            self .ui .tprint (c ("Voce conseguiu fugir!",Color .BRIGHT_GREEN ))
            self .ui .pause ()
            return "fled"
        else :
            self .ui .tprint (c ("Voce falhou em fugir!",Color .RED ))

            self .player .add_buff ("dodge_flat",20 ,1 ,"Adrenalina de Fuga")
            self .ui .tprint (c ("(Adrenalina: +20% esquiva este turno)",Color .DIM ))
            self .ui .pause ()
            return None 

    def player_domain_expansion (self ):

        can ,reason =self .player .can_use_domain ()
        if not can :
            self .ui .tprint (c (f"Dominio indisponivel: {reason }",Color .RED ))
            self .ui .pause ()
            return None 

        domain_name =self .player .get_domain_name ()
        if not domain_name :
            return None 

        if self .player .is_simple_domain ():
            ce_cost =self .player .DOMAIN_SIMPLE_CE_COST 
            if self .player .ce_current <ce_cost :
                self .ui .tprint (c (f"CE insuficiente! Precisa de {ce_cost }.",Color .RED ))
                self .ui .pause ()
                return None 
            self .player .ce_current -=ce_cost 
            self .ui .tprint (c (">> Dominio Simples (Hollow Wicker Basket)!",Color .BRIGHT_CYAN ))
            self .ui .tprint (c ("Voce cria um dominio defensivo que neutraliza ataques amaldicoados.",Color .DIM ))
            self .ui .tprint (c (f"Custo: -{ce_cost } CE.",Color .DIM ))
            self .player .add_buff ("anti_domain",1 ,3 ,"Dominio Simples")
            self .player .add_buff ("def",50 ,3 ,"Dominio Simples")
            self .player .add_buff ("dodge_flat",20 ,3 ,"Dominio Simples")
            self .player .domain_used_count +=1 
            self .ui .pause ()
            return None 

        available_exts =get_available_extensions (self .player )
        domain_ext =None 
        for tech_name ,ext in available_exts :
            if ext .get ("type")=="domain_active"and ext .get ("name")==domain_name :
                domain_ext =ext 
                break 

        if not domain_ext :

            return self ._legacy_domain_expansion (domain_name )

        actual_cost =int (domain_ext ["ce_cost"]/self .player .get_ce_efficiency ())
        if self .player .ce_current <actual_cost :
            self .ui .tprint (c (f"CE insuficiente! Precisa de {actual_cost }.",Color .RED ))
            self .ui .pause ()
            return None 

        self .player .ce_current -=actual_cost 
        self .player .domain_used_count +=1 

        if domain_ext .get ("name")and domain_ext ["name"]not in self .techniques_used_this_combat :
            self .techniques_used_this_combat .append (domain_ext ["name"])

        return self ._activate_domain (domain_ext ,already_paid =True )

    def _legacy_domain_expansion (self ,domain_name ):

        domain =DOMAINS .get (domain_name )
        if not domain :
            self .ui .tprint (c (f"Erro: dominio '{domain_name }' nao encontrado na base.",Color .RED ))
            self .ui .pause ()
            return None 

        self .player .ce_current =0 
        self .player .domain_used_count +=1 
        self .player .domain_active_turns =domain ["effect"].get ("duration",3 )

        self .ui .clear_screen ()
        self .ui .show_ascii (ui .ASCII_DOMAIN ,color =Color .BRIGHT_MAGENTA ,clear =False )
        self .ui .tprint (c (f"!! EXPANSAO DE DOMINIO: {domain_name } !!",Color .BRIGHT_MAGENTA +Color .BOLD +Color .BLINK ))
        self .ui .tprint (c (f"   {domain ['desc']}",Color .DIM ))
        self .ui .pause ()

        base_dmg =int (self .player .get_total_str ()*2.5 *domain ["effect"].get ("dmg_mult",2.0 ))

        if domain ["effect"].get ("scales_with_fingers"):
            finger_mult =1.0 +(self .player .sukuna_fingers_eaten *0.25 )
            base_dmg =int (base_dmg *finger_mult )
            self .ui .tprint (c (f"  [Poder de Sukuna: {self .player .sukuna_fingers_eaten } dedos - dano x{finger_mult :.2f}]",
            Color .BRIGHT_RED +Color .BOLD ))

        for e in self .enemies :
            if e ["hp"]>0 :
                e ["hp"]-=base_dmg 
                self .ui .tprint (c (f"{e ['name']} sofre {base_dmg } de dano CERTeiro!",Color .BRIGHT_RED ))
                if domain ["effect"].get ("stun_target"):
                    e ["stunned_turns"]=e .get ("stunned_turns",0 )+domain ["effect"]["stun_target"]
                if domain ["effect"].get ("instakill_below_pct"):
                    if e ["hp"]/max (1 ,e ["max_hp"])<domain ["effect"]["instakill_below_pct"]:
                        e ["hp"]=0 
                        self .ui .tprint (c (f"!! {e ['name']} foi aniquilado pelo dominio!",Color .BRIGHT_RED ))
                if domain ["effect"].get ("bleed_stacks"):
                    e ["bleed_stacks"]=e .get ("bleed_stacks",0 )+domain ["effect"]["bleed_stacks"]
                    self .ui .tprint (c (f"{e ['name']} sangra do corte do dominio!",Color .RED ))

        self .player .add_buff ("domain_buff",2.0 ,domain ["effect"].get ("duration",3 ),"Dominio Ativo")
        self .player .exhausted_turns =2 
        self .ui .tprint (c ("Voce fica exausto apos usar o dominio. -50% atributos por 2 turnos.",Color .YELLOW ))
        self .ui .pause ()
        return None 

    def player_rct (self ):

        if not self .player .can_use_rct ():
            self .ui .tprint (c ("Voce nao pode usar RCT.",Color .YELLOW ))
            self .ui .pause ()
            return None 

        rct =get_rct_info ()
        actual_cost =int (rct ["ce_cost"]/self .player .get_ce_efficiency ())
        if self .player .ce_current <actual_cost :
            self .ui .tprint (c (f"CE insuficiente! Precisa de {actual_cost }.",Color .RED ))
            self .ui .pause ()
            return None 

        self .player .ce_current -=actual_cost 
        heal =int (self .player .max_hp *rct ["heal_pct"])
        self .player .hp =min (self .player .max_hp ,self .player .hp +heal )
        self .player .exhausted_turns =rct .get ("exhaustion_turns",1 )
        self .ui .tprint (c (f">> Tecnica Reversa! +{heal } HP",Color .BRIGHT_GREEN +Color .BOLD ))
        self .ui .tprint (c ("Voce inverte CE para curar. Exaustao por 1 turno.",Color .DIM ))

        self .ui .tprint (c ("!! ATENCAO: Exaustao por 1 turno — stats reduzidos 50% !!",
        Color .BRIGHT_RED +Color .BOLD ))
        self .ui .pause ()
        return None 

