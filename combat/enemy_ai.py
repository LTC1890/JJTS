from .common import *

class EnemyAIMixin :

    def _smart_pick_move (self ,options ,extract_name =None ):
        if not options :
            return None 
        if len (options )==1 :
            return options [0 ]
        if not getattr (self .player ,"_stolen_adaptation_active",False ):
            return random .choice (options )
        if extract_name is None :
            extract_name =lambda x :x 
        weights =[]
        for opt in options :
            name =extract_name (opt )
            resist =mahoraga_mod .get_player_damage_reduction (self .player ,name )
            weights .append (max (0.05 ,1.0 -resist ))
        return random .choices (options ,weights =weights ,k =1 )[0 ]

    def boss_attempt_rct (self ,enemy ):

        if not enemy .get ("can_active_rct"):
            return False 
        hp_pct =enemy ["hp"]/max (1 ,enemy ["max_hp"])
        if hp_pct >=0.65 :
            return False 
        if enemy .get ("ce",0 )<enemy .get ("rct_ce_cost",80 ):
            return False 
        if random .random ()>enemy .get ("rct_use_chance",0.25 ):
            return False 
        heal_pct =enemy .get ("rct_active_heal_pct",0.18 )
        heal =int (enemy ["max_hp"]*heal_pct )
        enemy ["ce"]=max (0 ,enemy .get ("ce",0 )-enemy .get ("rct_ce_cost",80 ))
        enemy ["hp"]=min (enemy ["max_hp"],enemy ["hp"]+heal )
        self .ui .tprint (c (f"\n{enemy ['name']} ativa Tecnica Reversa! Regenera {heal } HP!",
        Color .BRIGHT_GREEN +Color .BOLD ))
        self .ui .pause ()
        return True 

    def boss_attempt_domain (self ,enemy ):

        if not enemy .get ("domain"):
            return False 
        if enemy .get ("domain_used_count",0 )>=enemy .get ("domain_max_uses",1 ):
            return False 
        if enemy .get ("active_domain"):
            return False 
        domain_ce_cost =enemy .get ("domain_ce_cost",int (enemy .get ("max_ce",1000 )*0.5 ))
        if enemy .get ("ce",0 )<domain_ce_cost :
            return False 
        hp_pct =enemy ["hp"]/max (1 ,enemy ["max_hp"])
        trigger_pct =enemy .get ("domain_trigger_hp_pct",0.45 )
        if hp_pct >trigger_pct and enemy .get ("domain_used_count",0 )>0 :
            return False 
        if hp_pct >trigger_pct and random .random ()>0.15 :
            return False 

        enemy ["ce"]=max (0 ,enemy .get ("ce",0 )-domain_ce_cost )
        enemy ["domain_used_count"]=enemy .get ("domain_used_count",0 )+1 
        dmg_mult =enemy .get ("domain_dmg_mult",3.0 )

        if self .player .active_domain :
            player_wins =self ._resolve_domain_clash (enemy ,player_dmg_mult =1.0 ,enemy_dmg_mult =dmg_mult /3.0 )
            if player_wins :
                punish =int (enemy .get ("max_hp",1000 )*0.08 )
                enemy ["hp"]-=punish 
                self .ui .tprint (c (f"O dominio de {enemy ['name']} se despedaca! ({punish } dano)",Color .BRIGHT_GREEN ))
                self .ui .pause ()
                return True 
            else :
                self .player .active_domain =None 
                punish =int (self .player .max_hp *0.15 )
                actual =self .player .take_damage (punish ,damage_type ="cursed",ignore_def =True )
                self .player .stunned_turns =max (1 ,self .player .stunned_turns +1 )
                self .ui .tprint (c (f"Seu dominio colapsa! Voce toma {actual } dano e fica atordoado.",
                Color .BRIGHT_RED +Color .BOLD ))
                self .ui .pause ()

        self .ui .flash_red (f"!! {enemy ['name']} EXPANDE O DOMINIO: {enemy ['domain']} !!")
        self .ui .pause ()

        dmg =int (enemy .get ("atk",10 )*dmg_mult )

        targets =[]
        if self .player .hp >0 :
            targets .append (("player",self .player ))
        for a in self .allies :
            if a ["hp"]>0 :
                targets .append (("ally",a ))
        if hasattr (self ,"active_shikigamis"):
            for shiki in self .active_shikigamis :
                if shiki .get ("hp",0 )>0 :
                    targets .append (("shikigami",shiki ))

        for tt ,to in targets :
            if tt =="player":
                actual =self .player .take_damage (dmg ,damage_type ="cursed",ignore_def =True )
                self .ui .tprint (c (f"O dominio te atinge: {actual } dano (certeiro)!",Color .BRIGHT_RED +Color .BOLD ))
                domain_effect =enemy .get ("domain_effect")
                if domain_effect =="bleed":
                    self .player .bleed_stacks +=enemy .get ("domain_effect_value",4 )
                    self .ui .tprint (c ("Voce esta sangrando pelo dominio!",Color .RED ))
                elif domain_effect =="stun":
                    if random .random ()>self .player .get_stun_resist_chance ():
                        self .player .stunned_turns =max (1 ,self .player .stunned_turns +enemy .get ("domain_effect_value",1 ))
                        self .ui .tprint (c ("Voce foi atordoado pelo dominio!",Color .YELLOW ))
                elif domain_effect =="burn":
                    self .player .burn_stacks +=enemy .get ("domain_effect_value",4 )
                    self .ui .tprint (c ("Voce esta queimando pelo dominio!",Color .BRIGHT_RED ))
            else :
                actual =calculate_damage (dmg ,to .get ("def",5 ))
                to ["hp"]-=actual 
                self .ui .tprint (c (f"  {to ['name']} atingido pelo dominio: {actual } dano",Color .RED ))

        enemy ["active_domain"]={
        "ce_per_turn":max (200 ,int (domain_ce_cost *0.3 )),
        "dmg_mult":dmg_mult ,
        "effect":enemy .get ("domain_effect"),
        "effect_value":enemy .get ("domain_effect_value",4 ),
        "turns_active":0 ,
        "max_turns":3 ,
        }
        if enemy .get ("technique")=="Ittadakimasu (Hakari Kinji)":
            enemy ["active_domain"]["slot_machine"]=True 
            enemy ["active_domain"]["max_spins"]=3 
            enemy ["active_domain"]["jackpot_chance_per_spin"]=0.08 
            enemy ["active_domain"]["spins_done"]=0 

        return True 

    def ally_action (self ,ally ):

        msgs =allies_mod .ally_take_turn (ally ,self .enemies ,self .player ,self .ui )
        for m in msgs :

            if "BLACK FLASH"in m :
                self .ui .flash_red (m )
                self .ui .show_ascii (ui .ASCII_BLACK_FLASH ,color =Color .BRIGHT_RED ,clear =False )
            else :
                self .ui .tprint (c (m ,Color .BRIGHT_CYAN ))
        self .ui .pause ()

    def _summon_real_mahoraga (self ,summoner ):

        if getattr (self ,"_mahoraga_summoned",False ):
            return 
        self ._mahoraga_summoned =True 

        self .ui .tprint (c ("\n!! MEGUMI INVOCA MAHORAGA DE VERDADE !!",Color .BRIGHT_RED +Color .BOLD +Color .BLINK ))
        self .ui .tprint (c ("'PRIMEIRO ADAPTACAO.' A roda divina gira ao lado de Megumi.",Color .BRIGHT_RED ))
        self .ui .pause ()

        level =max (1 ,self .player .level_system .level )
        mahoraga_ally =create_active_shikigami ("Eight-Handled Sword Mahoraga",level )
        mahoraga_ally ["is_ally"]=False 
        mahoraga_ally ["is_enemy"]=True 
        mahoraga_ally ["is_shikigami"]=False 
        mahoraga_ally ["name"]="Mahoraga (Invocado por Megumi)"
        mahoraga_ally ["rank"]="Grau Especial"
        mahoraga_ally ["max_hp"]=int (mahoraga_ally ["hp"]*1.4 )
        mahoraga_ally ["hp"]=mahoraga_ally ["max_hp"]
        mahoraga_ally ["max_ce"]=mahoraga_ally .get ("max_ce",2000 )
        mahoraga_ally ["ce"]=mahoraga_ally ["max_ce"]
        mahoraga_ally ["xp"]=0 
        mahoraga_ally ["adaptive"]=True 
        mahoraga_ally ["ai_type"]="adaptive_tank"
        mahoraga_ally ["extensions_known"]=["Espada da Roda","Punho Adaptativo","Roda Girante"]
        mahoraga_ally ["buffs"]=[]
        mahoraga_ally ["debuffs"]=[]
        mahoraga_ally ["bleed_stacks"]=0 
        mahoraga_ally ["stunned_turns"]=0 
        mahoraga_ally ["domain_used_count"]=0 
        mahoraga_ally ["drops"]=[]
        mahoraga_ally ["karma_reward"]=0 
        mahoraga_mod .init_adaptation_state (mahoraga_ally )

        self .enemies .append (mahoraga_ally )
        self .ui .tprint (c (f"{mahoraga_ally ['name']} entra na batalha!",Color .BRIGHT_RED +Color .BOLD ))
        self .ui .pause ()

    def _summon_geto_curses (self ,summoner ):

        if getattr (self ,"_geto_curses_summoned",False ):
            return 
        self ._geto_curses_summoned =True 

        self .ui .tprint (c ("\n!! GETO LIBERA MALDICOES CAPTURADAS DOS VASOS !!",Color .BRIGHT_MAGENTA +Color .BOLD +Color .BLINK ))
        self .ui .pause ()

        level_mult =1.0 +max (0 ,self .player .level_system .level )*0.04 
        for _ in range (2 ):
            curse =enemies_mod .generate_curse (rank ="Grau 1",level_mult =level_mult )
            curse ["buffs"]=[]
            curse ["debuffs"]=[]
            curse ["bleed_stacks"]=0 
            curse ["stunned_turns"]=0 
            curse ["domain_used_count"]=0 
            self .enemies .append (curse )
            self .ui .tprint (c (f"  {curse ['name']} surge ao lado de Geto!",Color .BRIGHT_MAGENTA ))
        self .ui .pause ()

    def _pick_unified_action (self ,enemy ,abilities ,extensions ,base_ability_chance ,base_tech_chance ,aggression ,ai_type_bias ):
        candidates =[]
        if extensions and enemy .get ("ce",0 )>30 :
            for ext_name in extensions :
                w =base_tech_chance *aggression *ai_type_bias 
                resist =mahoraga_mod .get_player_damage_reduction (self .player ,ext_name )
                candidates .append (("tech",ext_name ,max (0.02 ,w *(1.0 -resist ))))
        for ab in abilities :
            w =base_ability_chance *aggression *ai_type_bias 
            resist =mahoraga_mod .get_player_damage_reduction (self .player ,ab ["name"])
            candidates .append (("ability",ab ,max (0.02 ,w *(1.0 -resist ))))
        candidates .append (("basic",None ,0.35 ))

        if not candidates :
            return False ,False ,None ,None 

        weights =[c [2 ]for c in candidates ]
        kind ,payload ,_ =random .choices (candidates ,weights =weights ,k =1 )[0 ]
        if kind =="tech":
            return True ,False ,payload ,None 
        if kind =="ability":
            return False ,True ,None ,payload 
        return False ,False ,None ,None 

    def enemy_action (self ,enemy ):

        if enemy .get ("phases"):
            for phase in enemy ["phases"]:
                if enemy ["hp"]/max (1 ,enemy ["max_hp"])<phase ["hp_pct_below"]:

                    if not phase .get ("applied"):
                        buff =phase .get ("buff",{})
                        for attr ,mult in buff .items ():
                            if attr =="atk":
                                enemy ["atk"]=int (enemy ["atk"]*mult )
                            elif attr =="def":
                                enemy ["def"]=int (enemy ["def"]*mult )
                            elif attr =="speed":
                                enemy ["speed"]=int (enemy ["speed"]*mult )
                            elif attr =="dodge_chance":
                                enemy ["dodge_chance"]=min (0.75 ,enemy .get ("dodge_chance",0.1 )+mult )
                            elif attr =="crit_chance":
                                enemy ["crit_chance"]=min (0.75 ,enemy .get ("crit_chance",0.1 )+mult )
                        phase ["applied"]=True 
                        self .ui .tprint (c (phase ["msg"],Color .BRIGHT_RED +Color .BOLD ))
                        self .ui .pause ()

                        if phase .get ("summon_mahoraga"):
                            self ._summon_real_mahoraga (enemy )
                        if phase .get ("summon_curses"):
                            self ._summon_geto_curses (enemy )

                        if phase .get ("new_extensions_known"):
                            enemy ["extensions_known"]=phase ["new_extensions_known"]
                            self .ui .tprint (c (f"!! {enemy ['name']} revela um novo conjunto de tecnicas !!",
                            Color .BRIGHT_YELLOW +Color .BOLD ))
                        if phase .get ("new_abilities_key"):
                            enemy ["abilities"]=list (enemies_mod .BOSS_ABILITIES .get (
                            phase ["new_abilities_key"],enemy .get ("abilities",[])))
                        if phase .get ("new_domain"):
                            enemy ["domain"]=phase ["new_domain"]
                            enemy ["domain_used_count"]=0 
                        if "new_domain_ce_cost"in phase :
                            enemy ["domain_ce_cost"]=phase ["new_domain_ce_cost"]
                        if "new_domain_dmg_mult"in phase :
                            enemy ["domain_dmg_mult"]=phase ["new_domain_dmg_mult"]
                        if phase .get ("hp_bonus_pct"):
                            bonus_hp =int (enemy ["max_hp"]*phase ["hp_bonus_pct"])
                            enemy ["max_hp"]+=bonus_hp 
                            enemy ["hp"]+=bonus_hp 
                            self .ui .tprint (c (f"  (+{bonus_hp } HP maximo)",Color .DIM ))
                        if phase .get ("new_name"):
                            enemy ["name"]=phase ["new_name"]
                        self .ui .pause ()

        if enemy .get ("hp",0 )<=0 :
            return 

        if self .boss_attempt_domain (enemy ):
            return 

        if self .boss_attempt_rct (enemy ):
            return 

        if enemy .get ("adaptive")and not enemy .get ("adapted_this_combat"):
            enemy ["def"]=int (enemy ["def"]*1.05 )
            enemy ["adapted_this_combat"]=True 

        possible_targets =[]
        if self .player .hp >0 :
            possible_targets .append (("player",self .player ))
        for a in self .allies :
            if a ["hp"]>0 :
                possible_targets .append (("ally",a ))
        if hasattr (self ,"active_shikigamis"):
            for shiki in self .active_shikigamis :
                if shiki .get ("hp",0 )>0 :
                    possible_targets .append (("shikigami",shiki ))

        if not possible_targets :
            self .ui .pause ()
            return 

        rank_idx ={"Grau 4":0 ,"Grau 3":1 ,"Grau 2":2 ,"Grau 1":3 ,"Grau Especial":4 }
        enemy_rank_idx =rank_idx .get (enemy .get ("rank","Grau 4"),0 )

        target_type ,target =None ,None 

        if enemy_rank_idx >=2 and random .random ()<0.30 :
            shiki_targets =[t for t in possible_targets if t [0 ]=="shikigami"]
            if shiki_targets :
                target_type ,target =random .choice (shiki_targets )

        if target is None and enemy .get ("ai_type")=="speed_assassin":
            def _speed_of (t ):
                if t [0 ]=="player":
                    return t [1 ].get_total_speed ()
                return t [1 ].get ("speed",10 )
            target_type ,target =max (possible_targets ,key =_speed_of )

        if target is None and enemy_rank_idx >=3 and random .random ()<0.40 :
            low_hp_targets =[]
            for tt ,to in possible_targets :
                if tt =="player":
                    hp_ratio =to .hp /max (1 ,to .max_hp )
                else :
                    hp_ratio =to .get ("hp",0 )/max (1 ,to .get ("max_hp",1 ))
                if hp_ratio <0.30 :
                    low_hp_targets .append ((tt ,to ))
            if low_hp_targets :
                target_type ,target =random .choice (low_hp_targets )

        if target is None and enemy .get ("aggro_player")and self .player .hp >0 :
            target_type ,target ="player",self .player 

        if target is None :
            target_type ,target =random .choice (possible_targets )

        if enemy .get ("instakill_if_lower_rank"):
            if self .player .rank_system .rank !="Grau Especial":
                self .ui .tprint (c (f"\n{enemy ['name']} sorri.",Color .BRIGHT_RED +Color .BOLD ))
                self .ui .tprint (c ("'Voce nao tem chance. O rei das maldicoes apenas sorri.'",Color .BRIGHT_RED ))
                self .ui .tprint (c ("Sukuna te despedaca em um golpe.",Color .BRIGHT_RED +Color .BOLD ))
                self .player .hp =0 
                self .ui .pause ()
                return 

        atk =enemy .get ("atk",10 )

        aggression =CONFIG .get_enemy_ai_aggression ()
        ai_type =enemy .get ("ai_type","basic")
        ai_type_bias ={
        "physical_striker":0.65 ,"combo_swapper":1.20 ,"ranged_aggro":1.15 ,
        "adaptive_tank":0.90 ,"speed_assassin":1.05 ,"smart":1.10 ,
        "basic_smart":1.0 ,"basic":0.85 ,
        }.get (ai_type ,1.0 )

        abilities =enemy .get ("abilities",[])
        hp_pct =enemy ["hp"]/max (1 ,enemy ["max_hp"])
        if enemy .get ("aggressive"):
            base_ability_chance =0.60 
        elif hp_pct <0.30 :
            base_ability_chance =0.70 
        elif hp_pct <0.50 :
            base_ability_chance =0.60 
        else :
            base_ability_chance =ENEMY_ABILITY_CHANCE 

        extensions =enemy .get ("extensions_known",[])
        base_tech_chance =0.4 if ai_type !="ranged_aggro"else 0.55 

        forced_tech_name =None 
        forced_ability =None 
        if getattr (self .player ,"_stolen_adaptation_active",False )and (abilities or extensions ):
            use_tech ,use_ability ,forced_tech_name ,forced_ability =self ._pick_unified_action (
            enemy ,abilities ,extensions ,base_ability_chance ,base_tech_chance ,aggression ,ai_type_bias )
        else :
            use_ability =random .random ()<min (0.95 ,base_ability_chance *aggression *ai_type_bias )and abilities 
            use_tech =(random .random ()<min (0.9 ,base_tech_chance *aggression *ai_type_bias )
            and extensions and enemy .get ("ce",0 )>30 )

        enemy_effect =None 
        enemy_tech_dmg_mult =1.0 
        used_ability =None 

        if use_tech :
            tech_name =forced_tech_name if forced_tech_name is not None else self ._smart_pick_move (extensions )
            self .ui .tprint (c (f"\n{enemy ['name']} usa {tech_name }!",Color .BRIGHT_RED +Color .BOLD ))
            enemy ["ce"]=max (0 ,enemy .get ("ce",0 )-30 )

            tech_lower =tech_name .lower ()
            if any (k in tech_lower for k in ["domain","expansao","coffin","malevolent","unlimited",
            "self-embodiment","chimera"]):

                enemy_effect ="aoe"
                enemy_tech_dmg_mult =2.5 
            elif any (k in tech_lower for k in ["stun","freeze","congel","stop","pare",
            "sleep","durma","frame"]):
                enemy_effect ="stun"
                enemy_tech_dmg_mult =1.2 
            elif any (k in tech_lower for k in ["blood","sangue","sangre","bleed",
            "piercing","supernova","convergence"]):
                enemy_effect ="bleed"
                enemy_tech_dmg_mult =1.8 
            elif any (k in tech_lower for k in ["transfigur","soul","alma","toque"]):
                enemy_effect ="soul"
                enemy_tech_dmg_mult =2.0 
            elif any (k in tech_lower for k in ["fire","fogo","meteor","ember"]):
                enemy_effect ="burn"
                enemy_tech_dmg_mult =2.0 
            elif any (k in tech_lower for k in ["heal","rct","cura"]):

                heal =int (enemy ["max_hp"]*0.2 )
                enemy ["hp"]=min (enemy ["max_hp"],enemy ["hp"]+heal )
                self .ui .tprint (c (f"{enemy ['name']} se cura em {heal } HP!",Color .BRIGHT_GREEN ))
                self .ui .pause ()
                return 
            else :

                enemy_tech_dmg_mult =1.5 
            dmg =int (atk *enemy_tech_dmg_mult )
        elif use_ability :
            used_ability =forced_ability if forced_ability is not None else self ._smart_pick_move (abilities ,extract_name =lambda a :a ["name"])
            self .ui .tprint (c (f"\n{enemy ['name']} usa {used_ability ['name']}!",Color .BRIGHT_RED +Color .BOLD ))
            self .ui .tprint (c (f"   {used_ability ['desc']}",Color .DIM ))
            dmg =int (atk *used_ability .get ("dmg_mult",1.0 ))
        else :
            dmg =atk 

        enemy_black_flash =False 
        rank_idx_bf ={"Grau 4":0 ,"Grau 3":1 ,"Grau 2":2 ,"Grau 1":3 ,"Grau Especial":4 }
        enemy_rank_idx_bf =rank_idx_bf .get (enemy .get ("rank","Grau 4"),0 )

        if enemy_rank_idx_bf >=3 :

            bf_chance =0.08 if enemy_rank_idx_bf ==3 else 0.15 
            if random .random ()<bf_chance :
                enemy_black_flash =True 
                dmg =int (dmg *BLACK_FLASH_DMG_MULT )
                self .ui .flash_red (f"!! {enemy ['name']} acerta um BLACK FLASH !!")
                self .ui .show_ascii (ui .ASCII_BLACK_FLASH ,color =Color .BRIGHT_RED ,clear =False )
                self .ui .pause ()

        if not enemy_black_flash and enemy .get ("can_crit")and random .random ()<enemy .get ("crit_chance",0 ):
            crit_mult =enemy .get ("crit_mult",1.5 )
            dmg =int (dmg *crit_mult )
            self .ui .tprint (c (f"!! {enemy ['name']} acerta um CRITICO! (x{crit_mult :.1f})",Color .BRIGHT_RED +Color .BOLD ))

        if target_type =="player":

            if enemy_effect !="aoe":
                dodge =self .player .get_dodge_chance ()

                if random .random ()<dodge :
                    self .ui .tprint (c (f"\n{enemy ['name']} ataca, mas VOCE ESQUIVA!",Color .BRIGHT_GREEN ))
                    self .ui .pause ()
                    return 

            trait =BIRTH_TRAITS .get (self .player .birth_trait ,{})
            counter =trait .get ("effects",{}).get ("counter_chance",0 )
            if random .random ()<counter :
                self .ui .tprint (c (f"\n{enemy ['name']} ataca, mas voce contra-ataca!",Color .BRIGHT_GREEN ))
                counter_dmg =calculate_damage (int (self .player .get_total_str ()*1.2 ),enemy .get ("def",0 ))
                enemy ["hp"]-=counter_dmg 
                self .ui .tprint (c (f"Counter: {counter_dmg } dano!",Color .BRIGHT_GREEN ))
                self .ui .pause ()
                return 

            incoming_move_name =used_ability ["name"]if used_ability else (tech_name if use_tech else "Ataque Fisico")

            if enemy_effect =="soul":

                actual =dmg 
                self .ui .tprint (c ("(Dano espiritual ignora defesa!)",Color .MAGENTA ))
                if getattr (self .player ,"_stolen_adaptation_active",False ):
                    stolen_resist =mahoraga_mod .get_player_damage_reduction (self .player ,incoming_move_name )
                    if stolen_resist >0 :
                        actual =max (1 ,int (actual *(1.0 -stolen_resist )))
                self .player .hp -=actual 
            else :
                damage_type ="cursed"if use_tech else "physical"
                if getattr (self .player ,"_stolen_adaptation_active",False ):
                    stolen_resist =mahoraga_mod .get_player_damage_reduction (self .player ,incoming_move_name )
                    if stolen_resist >0 :
                        dmg =max (1 ,int (dmg *(1.0 -stolen_resist )))
                def_ignore_pct =used_ability .get ("def_ignore_pct",0.0 )if used_ability else 0.0 
                if def_ignore_pct >0 :
                    reduced_def =int (self .player .get_total_def ()*(1.0 -def_ignore_pct ))
                    actual =calculate_damage (dmg ,reduced_def )
                    self .player .hp =max (0 ,self .player .hp -actual )
                    self .ui .tprint (c (f"({used_ability ['name']} ignora {int (def_ignore_pct *100 )}% da sua defesa!)",
                    Color .DIM ))
                else :
                    actual =self .player .take_damage (dmg ,damage_type =damage_type )
            if getattr (self .player ,"_stolen_adaptation_active",False ):
                mahoraga_mod .register_hit_on_player (self .player ,incoming_move_name ,ui_module =self .ui )
            self .ui .tprint (c (f"\n{enemy ['name']} ataca VOCE! Dano: {actual }",Color .RED ))

            if enemy_effect =="stun":
                if self .player .has_special_buff ("frame_guard"):
                    self .ui .tprint (c ("Protecao de Frames bloqueia o atordoamento!",Color .BRIGHT_YELLOW ))
                else :
                    player_resist =self .player .get_stun_resist_chance ()
                    if random .random ()>player_resist :
                        self .player .stunned_turns =max (1 ,self .player .stunned_turns +1 )
                        self .ui .tprint (c ("Voce foi atordoado!",Color .YELLOW ))
                    else :
                        self .ui .tprint (c ("Voce resiste ao atordoamento!",Color .BRIGHT_CYAN ))
            elif enemy_effect =="bleed":
                self .player .bleed_stacks +=2 
                self .ui .tprint (c ("Voce esta sangrando!",Color .RED ))
            elif enemy_effect =="burn":
                self .player .burn_stacks +=3 
                self .ui .tprint (c ("Voce esta queimando!",Color .BRIGHT_RED ))
            elif enemy_effect =="aoe":
                for a in self .allies :
                    if a ["hp"]>0 :
                        a_dmg =calculate_damage (dmg ,a .get ("def",5 ))
                        a ["hp"]-=a_dmg 
                        self .ui .tprint (c (f"  {a ['name']} tambem atingido: {a_dmg } dano",Color .RED ))
                if hasattr (self ,"active_shikigamis"):
                    for shiki in self .active_shikigamis :
                        if shiki .get ("hp",0 )>0 :
                            s_dmg =calculate_damage (dmg ,shiki .get ("def",5 ))
                            shiki ["hp"]-=s_dmg 
                            self .ui .tprint (c (f"  {shiki ['name']} tambem atingido: {s_dmg } dano",Color .RED ))

            if used_ability :
                effect =used_ability .get ("effect")
                effect_value =used_ability .get ("effect_value",0 )
                effect_chance =used_ability .get ("effect_chance",0 )
                if effect and random .random ()<effect_chance :
                    if effect =="bleed":
                        self .player .bleed_stacks +=effect_value 
                        self .ui .tprint (c (f"Voce esta sangrando! (+{effect_value } stacks)",Color .RED ))
                    elif effect =="stun":
                        if self .player .has_special_buff ("frame_guard"):
                            self .ui .tprint (c ("Protecao de Frames bloqueia o atordoamento!",Color .BRIGHT_YELLOW ))
                        else :
                            player_resist =self .player .get_stun_resist_chance ()
                            if random .random ()>player_resist :
                                self .player .stunned_turns =max (1 ,self .player .stunned_turns +effect_value )
                                self .ui .tprint (c (f"Voce foi atordoado por {effect_value } turno(s)!",Color .YELLOW ))
                            else :
                                self .ui .tprint (c ("Voce resiste ao atordoamento!",Color .BRIGHT_CYAN ))
                    elif effect =="burn":
                        self .player .burn_stacks +=effect_value 
                        self .ui .tprint (c (f"Voce esta queimando! (+{effect_value } stacks)",Color .BRIGHT_RED ))
                    elif effect =="poison":
                        self .player .poison_stacks +=effect_value 
                        self .ui .tprint (c (f"Voce foi envenenado! (+{effect_value } stacks)",Color .GREEN ))
                    elif effect =="lifesteal":
                        heal =int (actual *effect_value )
                        enemy ["hp"]=min (enemy .get ("max_hp",999999 ),enemy ["hp"]+heal )
                        self .ui .tprint (c (f"{enemy ['name']} drena {heal } HP!",Color .BRIGHT_RED ))
                    elif effect =="technique_seal":
                        self .player .add_debuff ("technique_sealed",1 ,effect_value ,"Tecnica Anulada")
                        self .ui .tprint (c (
                        f"\n!! O INVERSOR DE ESPIRITOS ANULA SUA TECNICA AMALDICOADA !!\n"
                        f"Voce nao pode usar 'Usar Tecnica' por {effect_value } turno(s)!",
                        Color .BRIGHT_RED +Color .BOLD ))

            if enemy .get ("always_poison"):
                self .player .poison_stacks +=enemy ["always_poison"]
                self .ui .tprint (c (f"(Veneno passivo: +{enemy ['always_poison']} stacks)",Color .GREEN ))

            trap_val =self .player .get_buff_value ("trap_armed")
            if trap_val >0 :
                trap_dmg =int (self .player .get_total_str ()*trap_val )
                enemy ["hp"]-=trap_dmg 
                self .ui .tprint (c (f"!! ARMADILHA EXPLODE em {enemy ['name']}! {trap_dmg } dano!",
                Color .BRIGHT_YELLOW +Color .BOLD ))

                for b in self .player .buffs [:]:
                    if b ["type"]=="trap_armed":
                        self .player .buffs .remove (b )
                        break 

            if "Talisma de Gojo"in (self .player .equipped .get ("amuletos")or []):
                reflect =int (actual *0.30 )
                enemy ["hp"]-=reflect
                self .ui .tprint (c (f"Talisma reflete {reflect } dano!",Color .BRIGHT_CYAN ))

            pending_reflect =getattr (self .player ,"_pending_reflect_dmg",0 )
            if pending_reflect >0 :
                enemy ["hp"]-=pending_reflect
                self .ui .tprint (c (f"Distorcao da Alma reflete {pending_reflect } dano!",Color .MAGENTA ))
                self .player ._pending_reflect_dmg =0

        elif target_type =="ally":
            dodge =ally_get_dodge (target )
            if random .random ()<dodge :
                self .ui .tprint (c (f"\n{enemy ['name']} ataca, mas {target ['name']} esquivou!",Color .BRIGHT_GREEN ))
                self .ui .pause ()
                return 
            defense =target .get ("def",10 )
            actual =calculate_damage (dmg ,defense )
            target ["hp"]-=actual 
            self .ui .tprint (c (f"\n{enemy ['name']} ataca {target ['name']}! Dano: {actual }",Color .RED ))

            if used_ability :
                effect =used_ability .get ("effect")
                effect_value =used_ability .get ("effect_value",0 )
                effect_chance =used_ability .get ("effect_chance",0 )
                if effect and random .random ()<effect_chance :
                    if effect =="bleed":
                        target ["bleed_stacks"]=target .get ("bleed_stacks",0 )+effect_value 
                        self .ui .tprint (c (f"{target ['name']} esta sangrando! (+{effect_value })",Color .RED ))
                    elif effect =="stun":
                        target ["stunned_turns"]=target .get ("stunned_turns",0 )+effect_value 
                        self .ui .tprint (c (f"{target ['name']} atordoado por {effect_value }t!",Color .YELLOW ))
                    elif effect =="burn":
                        target ["burn_stacks"]=target .get ("burn_stacks",0 )+effect_value 
                        self .ui .tprint (c (f"{target ['name']} esta queimando! (+{effect_value })",Color .BRIGHT_RED ))
                    elif effect =="poison":
                        target ["poison_stacks"]=target .get ("poison_stacks",0 )+effect_value 
                        self .ui .tprint (c (f"{target ['name']} envenenado! (+{effect_value })",Color .GREEN ))
                    elif effect =="lifesteal":
                        heal =int (actual *effect_value )
                        enemy ["hp"]=min (enemy .get ("max_hp",999999 ),enemy ["hp"]+heal )
                        self .ui .tprint (c (f"{enemy ['name']} drena {heal } HP de {target ['name']}!",Color .BRIGHT_RED ))

            if target .get ("lives_sukuna")and target ["hp"]<=0 and target .get ("lives_used",0 )==0 :
                target ["lives_used"]=1 
                target ["hp"]=int (target ["max_hp"]*0.5 )
                self .ui .tprint (c (f"!! Sukuna assume o corpo de {target ['name']} por 1 turno!",Color .BRIGHT_RED +Color .BOLD ))

                alive_enemies =[e for e in self .enemies if e ["hp"]>0 ]
                if alive_enemies :
                    sukuna_target =random .choice (alive_enemies )
                    sukuna_dmg =200 
                    sukuna_target ["hp"]-=sukuna_dmg 
                    self .ui .tprint (c (f"Sukuna despedaca {sukuna_target ['name']}: {sukuna_dmg } dano!",Color .BRIGHT_RED ))

        elif target_type =="shikigami":

            shiki_speed =target .get ("speed",20 )
            shiki_dodge =min (0.40 ,0.05 +shiki_speed *0.005 )
            if random .random ()<shiki_dodge :
                self .ui .tprint (c (f"\n{enemy ['name']} ataca {target ['name']}, mas ele se esquiva das sombras!",
                Color .BRIGHT_CYAN ))
                self .ui .pause ()
                return 

            shiki_def =target .get ("def",10 )
            actual =calculate_damage (dmg ,shiki_def )
            if target .get ("adaptive"):
                shiki_move_name =used_ability ["name"]if used_ability else (tech_name if use_tech else "Ataque Fisico")
                resist =mahoraga_mod .get_damage_reduction (target ,shiki_move_name )
                if resist >0 :
                    actual =max (1 ,int (actual *(1.0 -resist )))
                mahoraga_mod .register_hit (target ,shiki_move_name ,ui_module =self .ui )
            target ["hp"]-=actual 
            self .ui .tprint (c (f"\n{enemy ['name']} ataca {target ['name']}! Dano: {actual }",Color .RED ))

            if used_ability :
                effect =used_ability .get ("effect")
                effect_value =used_ability .get ("effect_value",0 )
                effect_chance =used_ability .get ("effect_chance",0 )
                if effect and random .random ()<effect_chance :
                    if effect =="bleed":
                        target ["bleed_stacks"]=target .get ("bleed_stacks",0 )+effect_value 
                        self .ui .tprint (c (f"{target ['name']} sangrando! (+{effect_value })",Color .RED ))
                    elif effect =="stun":
                        target ["stunned_turns"]=target .get ("stunned_turns",0 )+effect_value 
                        self .ui .tprint (c (f"{target ['name']} atordoado! ({effect_value }t)",Color .YELLOW ))
                    elif effect =="burn":
                        target ["burn_stacks"]=target .get ("burn_stacks",0 )+effect_value 
                        self .ui .tprint (c (f"{target ['name']} queimando! (+{effect_value })",Color .BRIGHT_RED ))
                    elif effect =="poison":
                        target ["poison_stacks"]=target .get ("poison_stacks",0 )+effect_value 
                        self .ui .tprint (c (f"{target ['name']} envenenado! (+{effect_value })",Color .GREEN ))
                    elif effect =="lifesteal":
                        heal =int (actual *effect_value )
                        enemy ["hp"]=min (enemy .get ("max_hp",999999 ),enemy ["hp"]+heal )
                        self .ui .tprint (c (f"{enemy ['name']} drena {heal } HP!",Color .BRIGHT_RED ))

            if target .get ("hp",0 )<=0 :
                self .ui .tprint (c (f"{target ['name']} foi destruido pelo ataque inimigo!",
                Color .BRIGHT_RED +Color .BOLD ))

                if hasattr (self ,"active_shikigamis")and target in self .active_shikigamis :
                    self .active_shikigamis .remove (target )

        self .ui .pause ()

def ally_get_dodge (ally ):

    base =0.05 
    base +=ally .get ("speed",10 )*0.005 
    if ally .get ("ai_type")=="speed_assassin":
        base +=0.20 
    return base
