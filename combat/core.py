from .common import *

class CombatCore :

    def __init__ (self ,player ,enemies ,allies =None ,ui_module =None ,
    allow_flee =True ,special_rewards =None ):
        self .player =player 
        self .enemies =enemies if isinstance (enemies ,list )else [enemies ]
        self .allies =allies or []
        self .ui =ui_module or ui 
        self .allow_flee =allow_flee 
        self .special_rewards =special_rewards or []
        self .turn =1 
        self .combat_log =[]
        self .fled =False 
        self .victory =False 
        self .defeat =False 
        self .sukuna_transformed =False
        self .player_hit_streak =0

        self .techniques_used_this_combat =[]
        self .active_shikigamis =[]
        self ._dragon_bone_stacks =0
        self ._dragon_bone_accumulated =0
        self ._dragon_bone_turns_left =0
        self .pending_charged_techniques =[]
        self ._apply_balance_scaling ()

    def _apply_balance_scaling (self ):
        diff =CONFIG .get_difficulty_mod ()
        hp_mult =diff .get ("enemy_hp",1.0 )
        dmg_mult =diff .get ("enemy_dmg",1.0 )
        def_mult =diff .get ("enemy_def",1.0 )
        speed_mult =diff .get ("enemy_speed",1.0 )
        player_level =max (1 ,self .player .level_system .level )

        for e in self .enemies :
            if e .get ("_balance_scaled"):
                continue 
            e ["_balance_scaled"]=True 

            boss_scale =1.0 
            if e .get ("is_boss"):
                ref_level =BOSS_REFERENCE_LEVEL .get (e .get ("rank"),40 )
                if player_level >ref_level :
                    over =player_level -ref_level 
                    boss_scale =1.0 +min (BOSS_LEVEL_SCALE_CAP ,over *BOSS_LEVEL_SCALE_PER_LEVEL )

            total_hp_mult =hp_mult *boss_scale 
            total_dmg_mult =dmg_mult *boss_scale 
            total_def_mult =def_mult *(1.0 +(boss_scale -1.0 )*0.6 )
            total_speed_mult =speed_mult *(1.0 +(boss_scale -1.0 )*0.15 )

            for key in ("hp","max_hp"):
                if key in e :
                    e [key ]=max (1 ,int (e [key ]*total_hp_mult ))
            if "atk"in e :
                e ["atk"]=max (1 ,int (e ["atk"]*total_dmg_mult ))
            if "def"in e :
                e ["def"]=max (0 ,int (e ["def"]*total_def_mult ))
            if "speed"in e :
                e ["speed"]=max (1 ,int (e ["speed"]*total_speed_mult ))

            aggression =diff .get ("enemy_ai_aggression",1.0 )
            if "dodge_chance"in e :
                e ["dodge_chance"]=min (0.65 ,e ["dodge_chance"]*(0.7 +0.3 *aggression ))
            if "defense_chance"in e :
                e ["defense_chance"]=min (0.65 ,e ["defense_chance"]*(0.7 +0.3 *aggression ))

    def _reaction_difficulty (self ):
        rank_base ={
        "Grau 4":0.05 ,"Grau 3":0.15 ,"Grau 2":0.30 ,"Grau 1":0.50 ,"Grau Especial":0.75 ,
        }
        best =0.0 
        for e in self .enemies :
            if e .get ("hp",0 )<=0 :
                continue 
            score =rank_base .get (e .get ("rank"),0.20 )
            score +=min (0.25 ,e .get ("speed",10 )/2000.0 )
            if e .get ("exclusive_boss"):
                score +=0.15 
            best =max (best ,score )
        return max (0.0 ,min (1.0 ,best ))

    def _domain_power_score (self ,is_player ,entity =None ,domain_dmg_mult =1.0 ):
        if is_player :
            ce_ratio =self .player .ce_current /max (1 ,self .player .max_ce )
            control =self .player .attributes .get ("controle",10 )
            power =control *2.2 +ce_ratio *55 +domain_dmg_mult *12 
        else :
            ce_ratio =entity .get ("ce",0 )/max (1 ,entity .get ("max_ce",1 ))
            power =(entity .get ("atk",100 )/35.0 )+ce_ratio *55 +domain_dmg_mult *12 
        power *=random .uniform (0.85 ,1.15 )
        return power 

    def _resolve_domain_clash (self ,enemy ,player_dmg_mult =1.0 ,enemy_dmg_mult =1.0 ):
        self .ui .clear_screen ()
        self .ui .tprint (c ("\n!!!! CHOQUE DE DOMINIOS !!!!",Color .BRIGHT_RED +Color .BOLD +Color .BLINK ))
        self .ui .tprint (c ("Dois dominios nao podem coexistir no mesmo espaco. Um deles vai ceder.",Color .DIM ))
        player_power =self ._domain_power_score (True ,domain_dmg_mult =player_dmg_mult )
        enemy_power =self ._domain_power_score (False ,entity =enemy ,domain_dmg_mult =enemy_dmg_mult )
        self .ui .tprint (c (f"   Seu dominio: {player_power :.0f} de forca",Color .BRIGHT_CYAN ))
        self .ui .tprint (c (f"   Dominio de {enemy ['name']}: {enemy_power :.0f} de forca",Color .BRIGHT_RED ))
        self .ui .pause ()
        player_wins =player_power >=enemy_power 
        if player_wins :
            self .ui .tprint (c ("!! Seu dominio ESMAGA o do oponente !!",Color .BRIGHT_GREEN +Color .BOLD ))
        else :
            self .ui .tprint (c (f"!! O dominio de {enemy ['name']} ESMAGA o seu !!",Color .BRIGHT_RED +Color .BOLD ))
        self .ui .pause ()
        return player_wins 

    def _tick_enemy_domain (self ,enemy ):
        ad =enemy .get ("active_domain")
        if not ad :
            return 
        ad ["turns_active"]=ad .get ("turns_active",0 )+1 
        ce_cost =ad .get ("ce_per_turn",200 )
        if enemy .get ("ce",0 )<ce_cost or ad ["turns_active"]>ad .get ("max_turns",3 ):
            enemy ["active_domain"]=None 
            self .ui .tprint (c (f"O dominio de {enemy ['name']} se dissipa.",Color .DIM ))
            return 
        enemy ["ce"]=max (0 ,enemy .get ("ce",0 )-ce_cost )
        dmg =int (enemy .get ("atk",10 )*ad .get ("dmg_mult",2.5 )*0.4 )
        actual =self .player .take_damage (dmg ,damage_type ="cursed",ignore_def =True )
        self .ui .tprint (c (f"O dominio de {enemy ['name']} continua te atingindo: {actual } dano (certeiro)!",
        Color .RED ))
        effect =ad .get ("effect")
        if effect =="bleed":
            self .player .bleed_stacks +=ad .get ("effect_value",2 )
        elif effect =="burn":
            self .player .burn_stacks +=ad .get ("effect_value",2 )
        elif effect =="stun":
            if random .random ()>self .player .get_stun_resist_chance ():
                self .player .stunned_turns =max (1 ,self .player .stunned_turns +1 )
                self .ui .tprint (c ("Voce foi atordoado pelo dominio!",Color .YELLOW ))

        if ad .get ("slot_machine"):
            ad ["spins_done"]=ad .get ("spins_done",0 )+1 
            max_spins =ad .get ("max_spins",3 )
            is_jackpot =random .random ()<ad .get ("jackpot_chance_per_spin",0.08 )
            symbols_pool =["BAR","CHERRY","BELL","STAR","TREM"]
            if is_jackpot :
                roll =["7","7","7"]
            else :
                roll =[random .choice (symbols_pool )for _ in range (3 )]
                if roll [0 ]==roll [1 ]==roll [2 ]:
                    roll [2 ]=random .choice ([s for s in symbols_pool if s !=roll [2 ]])
            self .ui .tprint (c (f"\n  [CACA-NIQUEIS DE {enemy ['name']}] {' - '.join (roll )}",
            Color .BRIGHT_YELLOW +Color .BOLD ))
            if is_jackpot :
                self .ui .tprint (c (f"  !!!!! JACKPOT 7-7-7 !!!!! {enemy ['name']} se torna IMBATIVEL nesta batalha!",
                Color .BRIGHT_RED +Color .BOLD +Color .BLINK ))
                enemy ["infinite_resources_active"]=True 
                enemy ["hp"]=enemy ["max_hp"]
                enemy ["ce"]=enemy ["max_ce"]
            self .ui .pause ()

            if ad .get ("spins_done",0 )>=max_spins and enemy .get ("active_domain"):
                self .ui .tprint (c (f"\n  A maquina de {enemy ['name']} trava e quebra apos {max_spins } giros!",
                Color .DIM ))
                enemy ["active_domain"]=None 

    def start (self ):

        self .player .reset_combat_state ()
        self .techniques_used_this_combat =[]
        self .active_shikigamis =[]
        mahoraga_mod .reset_stolen_adaptation (self .player )
        self .player .infinite_resources_active =False 
        self .player .dmg_taken_this_combat =0 
        self .player .rika_summoned =False 
        self .player .rika_ce_upkeep =0 
        self .player .copied_technique =None 
        if self .player .dmg_buff_next_battle >0 :
            buff_val =self .player .dmg_buff_next_battle 
            self .player .add_buff ("attack_flat",int (self .player .get_total_str ()*buff_val ),
            999 ,"Selo de Forca")
            self .ui .tprint (c (f"\n[Selo de Forca ativo: +{int (buff_val *100 )}% dano nesta batalha!]",
            Color .BRIGHT_YELLOW ))
            self .player .dmg_buff_next_battle =0.0 
        for e in self .enemies :
            e ["buffs"]=e .get ("buffs",[])
            e ["debuffs"]=e .get ("debuffs",[])
            e ["bleed_stacks"]=0
            e ["stunned_turns"]=0
            e ["domain_used_count"]=0
            if e .get ("adaptive"):
                mahoraga_mod .init_adaptation_state (e )

        self ._dragon_bone_stacks =0
        self ._dragon_bone_accumulated =0
        self ._dragon_bone_turns_left =0
        self .pending_charged_techniques =[]

        self .ui .clear_screen ()
        self .ui .combat_separator ()
        self .ui .tprint (c ("!! COMBATE INICIADO !!",Color .BRIGHT_RED +Color .BOLD ))
        self .ui .combat_separator ()
        self .ui .tprint ("\nInimigos:")
        for e in self .enemies :
            rank_str =c (f"[{e .get ('rank','?')}]",Color .BRIGHT_RED )
            self .ui .tprint (f"  - {e ['name']} {rank_str }")
        if self .allies :
            self .ui .tprint (c ("\nAliados:",Color .BRIGHT_GREEN ))
            for a in self .allies :
                self .ui .tprint (f"  - {a ['name']}")
        self .ui .pause ()

        if not self .enemies or all (e .get ("hp",0 )<=0 for e in self .enemies ):
            return self .end_combat ("victory")

        while True :
            result =self .run_turn ()
            if result :
                if result =="revived":

                    self .defeat =False 
                    self .player .stunned_turns =0 
                    continue 
                return result 

    def run_turn (self ):

        if self .player .infinite_resources_active :
            self .player .hp =self .player .max_hp 
            self .player .ce_current =self .player .max_ce 

        if getattr (self .player ,"rika_summoned",False ):
            rika_alive =any (a .get ("is_rika_summon")and a ["hp"]>0 for a in self .allies )
            if not rika_alive :
                self .player .rika_summoned =False 
            else :
                upkeep =getattr (self .player ,"rika_ce_upkeep",15 )
                if self .player .ce_current <upkeep :
                    self .player .rika_summoned =False 
                    self .allies =[a for a in self .allies if not a .get ("is_rika_summon")]
                    self .ui .tprint (c ("\nRika nao tem mais CE suficiente para se manter manifestada e se dissipa.",
                    Color .YELLOW ))
                    self .ui .pause ()
                else :
                    self .player .ce_current -=upkeep 

        self .ui .clear_screen ()
        self .ui .combat_separator ()
        self .ui .tprint (c (f"TURNO {self .turn }",Color .BRIGHT_YELLOW +Color .BOLD ))
        self .ui .combat_separator ()

        self .display_combat_state ()

        all_combatants =[]

        all_combatants .append ({
        "type":"player","obj":self .player ,
        "speed":self .player .get_total_speed ()
        })

        for a in self .allies :
            if a ["hp"]>0 :
                all_combatants .append ({"type":"ally","obj":a ,"speed":a .get ("speed",10 )})

        for e in self .enemies :
            if e ["hp"]>0 :
                all_combatants .append ({"type":"enemy","obj":e ,"speed":e .get ("speed",10 )})

        all_combatants .sort (key =lambda x :x ["speed"],reverse =True )

        if self .turn ==1 :
            for c_dict in all_combatants :
                if c_dict ["type"]=="enemy"and c_dict ["obj"].get ("first_strike_guaranteed"):
                    all_combatants .remove (c_dict )
                    all_combatants .insert (0 ,c_dict )
                    self .ui .tprint (c (f"\n{c_dict ['obj']['name']} ataca antes que voce possa reagir!",
                    Color .BRIGHT_RED +Color .BOLD ))
                    self .ui .pause ()
                    break 

        for combatant in all_combatants :

            if self .player .is_dead ():
                return self .end_combat ("defeat")
            if all (e ["hp"]<=0 for e in self .enemies ):
                return self .end_combat ("victory")

            ctype =combatant ["type"]
            obj =combatant ["obj"]

            if ctype =="player":
                if self .player .is_stunned ():
                    self .ui .tprint (c ("Voce esta atordoado e nao pode agir!",Color .YELLOW ))
                    self .ui .pause ()
                    self .player .stunned_turns -=1 
                    continue 

                if self .player .get_debuff_value ("charging")>0 :
                    self .ui .tprint (c ("Voce esta concentrando CE para uma tecnica carregada...",Color .YELLOW ))
                    self .ui .pause ()
                    continue

                if hasattr (self ,"pending_charged_techniques")and self .pending_charged_techniques :
                    fired =[]
                    for pending in self .pending_charged_techniques :
                        ext =pending ["ext"]
                        target =pending ["target"]
                        ce_cost =pending ["ce_cost"]
                        hp_cost =pending ["hp_cost"]
                        if self .player .ce_current <ce_cost :
                            self .ui .tprint (c (f"\n!! Carga de {ext ['name']} falhou: CE insuficiente ({self .player .ce_current }/{ce_cost }) !!",Color .BRIGHT_RED ))
                            continue
                        self .player .ce_current -=ce_cost
                        self .ui .tprint (c (f"\n!! TECNICA CARREGADA DISPARA: {ext ['name']} !!",Color .BRIGHT_YELLOW +Color .BOLD ))
                        self .ui .tprint (c (f"-{ce_cost } CE consumido.",Color .BRIGHT_CYAN ))
                        if hp_cost >0 :
                            self .player .hp =max (1 ,self .player .hp -hp_cost )
                            self .ui .tprint (c (f"Custo de sangue: -{hp_cost } HP",Color .RED ))
                        alive_enemies =[e for e in self .enemies if e ["hp"]>0 ]
                        if target =="all":
                            self .execute_technique (ext ,target ="all")
                        elif isinstance (target ,dict ):
                            if target .get ("hp",0 )>0 :
                                self .execute_technique (ext ,target =target )
                            else :
                                if alive_enemies :
                                    new_t =alive_enemies [0 ]
                                    self .execute_technique (ext ,target =new_t )
                        else :
                            if alive_enemies :
                                self .execute_technique (ext ,target =alive_enemies [0 ])
                        if ext .get ("one_use_per_battle"):
                            if ext ["name"]not in self .techniques_used_this_combat :
                                self .techniques_used_this_combat .append (ext ["name"])
                        fired .append (pending )
                    for f in fired :
                        if f in self .pending_charged_techniques :
                            self .pending_charged_techniques .remove (f )
                    self .ui .pause ()
                    if all (e ["hp"]<=0 for e in self .enemies ):
                        return self .end_combat ("victory")
                    if self .player .is_dead ():
                        return self .end_combat ("defeat")
                    continue

                if self .player .check_sukuna_takeover (ui_module =self .ui ):

                    takeover_msgs =self .player .sukuna_takeover_attack (self .enemies ,ui_module =self .ui )
                    for msg in takeover_msgs :
                        self .ui .tprint (c (msg ,Color .BRIGHT_RED ))
                    self .ui .pause ()

                    if all (e ["hp"]<=0 for e in self .enemies ):
                        return self .end_combat ("victory")
                    if self .player .is_dead ():
                        return self .end_combat ("defeat")
                    continue 

                result =self .player_action ()
                while result =="retry":
                    result =self .player_action ()
                if result =="fled":
                    return self .end_combat ("fled")
                if result =="transformed":
                    return self .end_combat ("transformed")

                if hasattr (self ,"active_shikigamis")and self .active_shikigamis :
                    for shiki in self .active_shikigamis [:]:
                        if shiki .get ("hp",0 )<=0 :
                            self .ui .tprint (c (f"{shiki ['name']} foi destruido!",Color .RED ))
                            self .active_shikigamis .remove (shiki )
                            continue 

                        tick_msgs ,still_active =tick_shikigami (shiki ,self .player ,ui_module =self .ui )
                        if not still_active :
                            for m in tick_msgs :
                                self .ui .tprint (c (m ,Color .DIM ))
                            if shiki in self .active_shikigamis :
                                self .active_shikigamis .remove (shiki )
                            continue 
                        for m in tick_msgs :
                            self .ui .tprint (c (m ,Color .DIM ))

                        if shiki .get ("attacks"):
                            attack_msgs =shikigami_take_turn (shiki ,self .enemies ,self .player ,ui_module =self .ui )
                            for m in attack_msgs :
                                self .ui .tprint (c (m ,Color .BRIGHT_BLACK ))

                    if self .active_shikigamis :
                        self .ui .pause ()
            elif ctype =="ally":
                if obj .get ("stunned_turns",0 )>0 :
                    obj ["stunned_turns"]-=1 
                    self .ui .tprint (c (f"{obj ['name']} esta atordoado.",Color .YELLOW ))
                    self .ui .pause ()
                    continue 
                self .ally_action (obj )
            elif ctype =="enemy":
                if obj .get ("stunned_turns",0 )>0 :
                    obj ["stunned_turns"]-=1 
                    self .ui .tprint (c (f"{obj ['name']} esta atordoado.",Color .YELLOW ))
                    self .ui .pause ()
                    continue 
                self .enemy_action (obj )

        if self .player .is_dead ():
            return self .end_combat ("defeat")

        tick_msgs =self .player .tick_buffs ()
        for msg in tick_msgs :
            self .ui .tprint (c (msg ,Color .RED ))
        if getattr (self .player ,"_stolen_adaptation_active",False ):
            mahoraga_mod .tick_stolen_adaptation (self .player ,ui_module =self .ui )
        for a in self .allies :
            if a ["hp"]>0 :
                self .tick_combatant_buffs (a )
        for e in self .enemies :
            if e ["hp"]>0 :
                if e .get ("infinite_resources_active"):
                    e ["hp"]=e ["max_hp"]
                    e ["ce"]=e ["max_ce"]
                self .tick_combatant_buffs (e )
                if e .get ("active_domain"):
                    self ._tick_enemy_domain (e )

        if self .player .active_domain :
            if not self .player .active_domain .get ("ticked_this_turn",False ):
                self ._tick_active_domain ()
            else :

                self .player .active_domain ["ticked_this_turn"]=False 

        self .turn +=1 
        return None 

    def tick_combatant_buffs (self ,c_obj ):

        if c_obj .get ("hp",0 )<=0 :
            return 
        for buff in c_obj .get ("buffs",[])[:]:
            buff ["duration"]-=1
            if buff ["duration"]<=0 :
                c_obj ["buffs"].remove (buff )
        for debuff in c_obj .get ("debuffs",[])[:]:
            debuff ["duration"]-=1
            if debuff ["duration"]<=0 :
                dtype =debuff .get ("type","")
                dval =debuff .get ("value",0 )
                if dtype =="def_debuff"and dval >0 :
                    c_obj ["def"]=c_obj .get ("def",0 )+dval
                    orig =c_obj .get ("_original_def")
                    if orig is not None and c_obj ["def"]>=orig :
                        c_obj ["def"]=orig
                    self .ui .tprint (c (f"{c_obj ['name']} recuperou defesa.",Color .BRIGHT_GREEN ))
                elif dtype =="speed_debuff"and dval >0 :
                    c_obj ["speed"]=c_obj .get ("speed",0 )+dval
                    orig =c_obj .get ("_original_speed")
                    if orig is not None and c_obj ["speed"]>=orig :
                        c_obj ["speed"]=orig
                    self .ui .tprint (c (f"{c_obj ['name']} recuperou velocidade.",Color .BRIGHT_GREEN ))
                c_obj ["debuffs"].remove (debuff )

        if c_obj .get ("bleed_stacks",0 )>0 :
            bleed_resist =c_obj .get ("bleed_resist",0.0 )
            bleed_dmg =int (c_obj ["bleed_stacks"]*BLEED_DMG_PER_STACK *(1.0 -bleed_resist ))
            c_obj ["hp"]-=bleed_dmg 
            self .ui .tprint (c (f"{c_obj ['name']} sangra: {bleed_dmg } dano.",Color .RED ))
            c_obj ["bleed_stacks"]=max (0 ,c_obj ["bleed_stacks"]-1 )

        if c_obj .get ("burn_stacks",0 )>0 :
            burn_resist =c_obj .get ("burn_resist",0.0 )
            burn_dmg =int (c_obj ["burn_stacks"]*BURN_DMG_PER_STACK *(1.0 -burn_resist ))
            c_obj ["hp"]-=burn_dmg 
            self .ui .tprint (c (f"{c_obj ['name']} queima: {burn_dmg } dano.",Color .BRIGHT_RED ))
            c_obj ["burn_stacks"]=max (0 ,c_obj ["burn_stacks"]-1 )

        if c_obj .get ("poison_stacks",0 )>0 :
            poison_resist =c_obj .get ("poison_resist",0.0 )
            poison_dmg =int (c_obj ["poison_stacks"]*POISON_DMG_PER_STACK *(1.0 -poison_resist ))
            c_obj ["hp"]-=poison_dmg
            self .ui .tprint (c (f"{c_obj ['name']} envenenado: {poison_dmg } dano.",Color .GREEN ))
            c_obj ["poison_stacks"]=max (0 ,c_obj ["poison_stacks"]-1 )

        if c_obj .get ("rct_pct",0.0 )>0 and c_obj .get ("hp",0 )>0 :
            rct_heal =int (c_obj .get ("max_hp",1 )*c_obj ["rct_pct"])
            if rct_heal >0 :
                before =c_obj ["hp"]
                c_obj ["hp"]=min (c_obj .get ("max_hp",c_obj ["hp"]),c_obj ["hp"]+rct_heal )
                healed =c_obj ["hp"]-before 
                if healed >0 :
                    self .ui .tprint (c (f"{c_obj ['name']} regenera {healed } HP (Tecnica Reversa)!",Color .BRIGHT_GREEN ))

    def _register_adaptation_hit (self ,target ,dmg_type ):

        if not target .get ("adaptive"):
            return 
        counts =target .setdefault ("_adapt_counts",{})
        counts [dmg_type ]=counts .get (dmg_type ,0 )+1 
        hits =counts [dmg_type ]

        thresholds =[3 ,6 ,10 ,15 ]
        step =0 
        for t in thresholds :
            if hits >=t :
                step +=1 
        applied =target .setdefault ("_adapt_applied",{})
        prev_step =applied .get (dmg_type ,0 )
        if step <=prev_step :
            return 
        applied [dmg_type ]=step 

        resist_per_step =0.12 
        new_resist =min (0.85 ,step *resist_per_step )

        if dmg_type =="physical":
            target ["_adapt_physical_resist"]=new_resist 
        elif dmg_type =="ce":
            target ["_adapt_ce_resist"]=new_resist 
        elif dmg_type =="bleed":
            target ["bleed_resist"]=new_resist 
        elif dmg_type =="burn":
            target ["burn_resist"]=new_resist 
        elif dmg_type =="poison":
            target ["poison_resist"]=new_resist 
        elif dmg_type =="stun":
            base_stun =target .get ("_adapt_base_stun_resist",target .get ("stun_resist",0.0 ))
            target ["_adapt_base_stun_resist"]=base_stun 
            target ["stun_resist"]=min (0.95 ,base_stun +new_resist )

        label ={"physical":"ataques fisicos","ce":"tecnicas de CE","bleed":"sangramento",
        "burn":"queimaduras","stun":"atordoamento","poison":"veneno"}.get (dmg_type ,dmg_type )
        self .ui .tprint (c (f"\n!! A RODA DE MAHORAGA GIRA !! Adaptacao completa contra {label } "
        f"(+{int (new_resist *100 )}% resistencia)!",Color .BRIGHT_MAGENTA +Color .BOLD ))
        self .ui .pause ()

    def get_adaptive_physical_reduction (self ,target ):

        return target .get ("_adapt_physical_resist",0.0 )if target .get ("adaptive")else 0.0 

    def get_adaptive_ce_reduction (self ,target ):

        return target .get ("_adapt_ce_resist",0.0 )if target .get ("adaptive")else 0.0 

    def display_combat_state (self ):

        print ()

        p =self .player 
        print (c (f"  {p .name } (Voce) [Lv.{p .level_system .level } {p .rank_system .full_rank_name ()}]",
        Color .BRIGHT_GREEN +Color .BOLD ))
        print ("    "+self .ui .hp_bar (p .hp ,p .max_hp ,length =25 ))
        print ("    "+self .ui .ce_bar (p .ce_current ,p .max_ce ,length =25 ))
        if p .bleed_stacks >0 :
            print (c (f"    [Sangramento: {p .bleed_stacks }]",Color .RED ))
        if p .burn_stacks >0 :
            print (c (f"    [Queimando: {p .burn_stacks }]",Color .BRIGHT_RED ))
        if p .poison_stacks >0 :
            print (c (f"    [Envenenado: {p .poison_stacks }]",Color .GREEN ))
        if p .stunned_turns >0 :
            print (c (f"    [Atordoado: {p .stunned_turns } turnos]",Color .YELLOW ))
        if p .exhausted_turns >0 :
            print (c (f"    [Exausto: {p .exhausted_turns }t (-50% stats)]",Color .DIM ))
        if p .domain_active_turns >0 :
            print (c (f"    [DOMINIO ATIVO: {p .domain_active_turns } turnos]",Color .BRIGHT_MAGENTA +Color .BOLD ))
        if p .active_domain :
            ad =p .active_domain 
            print (c (f"    [EXPANSAO ATIVA: {ad ['name']} | {ad ['ce_per_turn']} CE/t | ativo ha {ad ['turns_active']}t]",
            Color .BRIGHT_MAGENTA +Color .BOLD ))
        if p .sukuna_takeover_active :
            print (c (f"    [!! SUKUNA NO CONTROLE: {p .sukuna_takeover_turns_left }t | +88% stats !!]",Color .BRIGHT_RED +Color .BOLD +Color .BLINK ))
        if p .frame_stacks >0 :
            print (c (f"    [Frame Stacks: {p .frame_stacks }/5]",Color .BRIGHT_YELLOW ))
        if getattr (p ,"_stolen_adaptation_active",False ):
            turns_left =getattr (p ,"_stolen_adaptation_turns_left",0 )
            print (c (f"    [ADAPTACAO ROUBADA ATIVA: proxima cobranca em {turns_left }t (300 CE)]",
            Color .BRIGHT_MAGENTA +Color .BOLD ))
        print ()

        if hasattr (self ,"active_shikigamis")and self .active_shikigamis :
            for shiki in self .active_shikigamis :
                if shiki .get ("hp",0 )>0 :
                    print (c (f"  {shiki ['name']} [Shikigami]",Color .BRIGHT_BLACK ))
                    print ("    "+self .ui .hp_bar (shiki ["hp"],shiki ["max_hp"],length =25 ))
                    if shiki .get ("duration")is not None :
                        print (c (f"    [Duracao: {shiki ['duration']}t | CE/turno: {shiki .get ('ce_cost_per_turn',0 )}]",
                        Color .DIM ))
                    else :
                        print (c (f"    [CE/turno: {shiki .get ('ce_cost_per_turn',0 )}]",Color .DIM ))
                    print ()

        for a in self .allies :
            if a ["hp"]>0 :
                print (c (f"  {a ['name']} [Aliado]",Color .BRIGHT_CYAN ))
                print ("    "+self .ui .hp_bar (a ["hp"],a ["max_hp"],length =25 ))
                if a .get ("ce",0 )>0 :
                    print ("    "+self .ui .ce_bar (a ["ce"],a ["max_ce"],length =25 ))
                print ()
            else :
                print (c (f"  {a ['name']} [CAIDO]",Color .DIM ))
                print ()

        for i ,e in enumerate (self .enemies ):
            if e ["hp"]>0 :
                rank_color =Color .BRIGHT_RED if e .get ("rank")=="Grau Especial"else Color .YELLOW 
                print (c (f"  {e ['name']} [{e .get ('rank','?')}] (Inimigo {i +1 })",rank_color +Color .BOLD ))

                if e .get ("is_boss"):
                    print ("    "+self .ui .hp_bar (e ["hp"],e ["max_hp"],length =25 ))
                else :
                    pct =e ["hp"]/max (1 ,e ["max_hp"])
                    if pct >0.7 :
                        hp_text ="Saudavel"
                    elif pct >0.4 :
                        hp_text ="Ferido"
                    elif pct >0.15 :
                        hp_text ="Gravemente ferido"
                    else :
                        hp_text ="Quase morto"
                    print (c (f"    HP: {hp_text }",Color .DIM ))
                if e .get ("bleed_stacks",0 )>0 :
                    print (c (f"    [Sangrando: {e ['bleed_stacks']}]",Color .RED ))
                if e .get ("burn_stacks",0 )>0 :
                    print (c (f"    [Queimando: {e ['burn_stacks']}]",Color .BRIGHT_RED ))
                if e .get ("poison_stacks",0 )>0 :
                    print (c (f"    [Envenenado: {e ['poison_stacks']}]",Color .GREEN ))
                if e .get ("stunned_turns",0 )>0 :
                    print (c ("    [Atordoado]",Color .YELLOW ))
                if e .get ("frame_locks",0 )>0 :
                    print (c (f"    [Frame Locks: {e ['frame_locks']}/3]",Color .BRIGHT_YELLOW ))
                if e .get ("soul_marks",0 )>0 :
                    print (c (f"    [Alma Distorcida: {e ['soul_marks']}]",Color .MAGENTA ))
                if e .get ("adaptive"):
                    adapted =mahoraga_mod .most_adapted_moves (e ,limit =3 )
                    if adapted :
                        adapted_str =", ".join (f"{name } ({int (resist *100 )}%)"for name ,resist in adapted )
                        print (c (f"    [Adaptado contra: {adapted_str }]",Color .BRIGHT_MAGENTA ))
                print ()
            else :
                print (c (f"  {e ['name']} [DERROTADO]",Color .DIM ))
                print ()

        self .ui .separator (char ="-",length =60 ,color =Color .DIM )

