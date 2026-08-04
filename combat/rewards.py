from .common import *

class RewardsMixin :

    def end_combat (self ,result ):

        self .ui .clear_screen ()
        self .ui .combat_separator ()

        if self .player .xp_mult_battles_left >0 :
            self .player .xp_mult_battles_left -=1 
            if self .player .xp_mult_battles_left <=0 :
                self .player .level_system .xp_mult =1.0 
                self .ui .tprint (c ("[O buff de XP do clima amaldicoado se dissipou.]",Color .DIM ))

        if result =="victory":
            self .victory =True 
            self .ui .tprint (c ("!! VITORIA !!",Color .BRIGHT_GREEN +Color .BOLD ))
            self .ui .tprint (c ("Todos os inimigos foram derrotados.",Color .GREEN ))

            total_xp =0 
            total_money =0 
            items_dropped =[]
            for e in self .enemies :
                xp =e .get ("xp",50 )

                diff =CONFIG .get_difficulty_mod ()
                xp =int (xp *diff .get ("xp_mult",1.0 ))
                total_xp +=xp 
                drop_mult =diff .get ("drop_mult",1.0 )
                money =random .randint (25 ,140 )*e .get ("drops_mult",1.0 )*drop_mult 
                total_money +=int (money )

                drops =roll_enemy_drop (e .get ("rank","Grau 4"),
                self .player .get_total_luck (),difficulty_mult =drop_mult )

                if e .get ("is_boss")and e .get ("drops"):
                    drops =list (e ["drops"])
                else :
                    drops =list (drops )
                if e .get ("is_boss")and e .get ("rare_drops"):
                    for rd in e ["rare_drops"]:
                        chance =rd .get ("chance",0 )
                        item_name =rd .get ("item")
                        if item_name and random .random ()<chance :
                            drops .append (item_name )
                            self .ui .tprint (c (f"  !! DROP RARO: {item_name } !!",Color .BRIGHT_YELLOW +Color .BOLD ))
                items_dropped .extend (drops )

                self .player .karma .on_curse_kill (e .get ("rank","Grau 4"))
                self .player .kills_total +=1 

            for it in items_dropped :
                if it =="Dedo de Sukuna":
                    self .player .sukuna_fingers_in_inventory +=1 
                else :
                    self .player .add_item (it )

            self .player .money +=total_money 
            self .player .process_auto_sell (ui_module =self .ui )

            leveled_up ,levels =self .player .level_system .add_xp (total_xp )
            rank_up ,new_rank =self .player .rank_system .add_xp (total_xp )

            tech_xp =0 
            tech_leveled =False 
            tech_levels =0 
            stage_changed =False 
            if self .player .has_technique_evolution ():
                tech_xp =int (total_xp *0.5 )
                tech_leveled ,tech_levels ,stage_changed =self .player .add_technique_xp (tech_xp )

            self .ui .tprint (c (f"\n+{total_xp } XP",Color .BRIGHT_YELLOW ))
            if tech_xp >0 :
                self .ui .tprint (c (f"+{tech_xp } XP para tecnica ({self .player .get_technique_stage_label ()})",
                Color .BRIGHT_MAGENTA ))
            self .ui .tprint (c (f"+{total_money } ienes",Color .BRIGHT_YELLOW ))
            if items_dropped :
                self .ui .tprint (c ("\nItens dropados:",Color .BRIGHT_GREEN ))
                for it in items_dropped :
                    self .ui .tprint (f"  - {it }")

            if leveled_up :
                self .ui .tprint (c (f"\n!! LEVEL UP! +{levels } nivel(s). Novo level: {self .player .level_system .level }",Color .BRIGHT_YELLOW +Color .BOLD ))
                self .ui .tprint (c (f"+{5 *levels } pontos de atributo disponiveis.",Color .BRIGHT_GREEN ))

            if tech_leveled :
                self .ui .tprint (c (f"\n!! TECNICA SUBIU! +{tech_levels } nivel(s). Nivel da tecnica: {self .player .technique_level }",
                Color .BRIGHT_MAGENTA +Color .BOLD ))
                if stage_changed :
                    stage_label =self .player .get_technique_stage_label ()
                    self .ui .tprint (c (f"!!! STAGE CHANGE: {stage_label } !!!",Color .BRIGHT_MAGENTA +Color .BOLD +Color .BLINK ))
                    if self .player .innate_technique =="Limitless"and self .player ._get_technique_stage ()=="Despertado":
                        self .ui .tprint (c ("A tecnica Limitless despertou! Novas skills disponiveis (Red, Hollow Purple, etc.)",
                        Color .BRIGHT_CYAN ))

            if rank_up :
                self .ui .tprint (c (f"\n!! PROMOCAO DE RANK! Novo rank: {self .player .rank_system .full_rank_name ()}",Color .BRIGHT_MAGENTA +Color .BOLD ))

            if self .player .sukuna_takeover_active and self .player .sukuna_takeover_turns_left >0 :
                karma_loss =random .randint (10 ,50 )
                self .player .karma .add_karma (-karma_loss )
                self .ui .tprint (c ("\nSukuna estava no controle quando a batalha acabou. Ele matou inocentes!",
                Color .BRIGHT_RED +Color .BOLD ))
                self .ui .tprint (c (f"-{karma_loss } karma (caos colateral).",Color .RED ))
                self .player .reset_combat_sukuna_state ()

            self .player .reset_combat_sukuna_state ()
            self .player .battles_won +=1 

            if leveled_up and self .player .auto_allocate_build :
                self .player .apply_auto_allocate (levels ,ui_module =self .ui )

            try :
                from save_system import autosave_after_battle 
                autosave_after_battle (self .player ,ui_module =self .ui )
            except Exception :
                pass 

            if self .special_rewards :
                self .ui .tprint (c ("\nRecompensas especiais:",Color .BRIGHT_CYAN ))
                for r in self .special_rewards :
                    self .ui .tprint (f"  - {r }")

        elif result =="defeat":
            self .defeat =True 
            self .ui .tprint (c ("!! DERROTA !!",Color .BRIGHT_RED +Color .BOLD ))
            self .ui .tprint (c ("Voce caiu em batalha.",Color .RED ))

            if self .player .has_item ("Pedra de Vida"):
                self .player .remove_item ("Pedra de Vida")
                revive_hp =int (self .player .max_hp *0.50 )
                self .player .hp =revive_hp 
                self .player .bleed_stacks =0 
                self .player .burn_stacks =0 
                self .player .poison_stacks =0 
                self .player .stunned_turns =0 
                self .player .exhausted_turns =0 
                self .ui .tprint (c ("\n!! PEDRA DE VIDA ATIVADA !!",Color .BRIGHT_GREEN +Color .BOLD +Color .BLINK ))
                self .ui .tprint (c (f"Voce revive com {revive_hp } HP!",Color .BRIGHT_GREEN ))
                self .ui .tprint (c ("A Pedra de Vida foi consumida.",Color .YELLOW ))
                self .ui .pause ()
                self .player .battles_lost +=1 
                return "revived"

            self .player .battles_lost +=1 
            lost_money =self .player .money //4 
            self .player .money =max (0 ,self .player .money -lost_money )
            self .ui .tprint (c (f"-{lost_money } ienes",Color .YELLOW ))

            if CONFIG .is_permadeath ():
                self .ui .tprint (c ("\n!! SELO DE DEDO - PERMADEATH TOTAL !!",Color .BRIGHT_RED +Color .BLINK +Color .BOLD ))
                self .ui .tprint (c ("Seu personagem morreu permanentemente.",Color .RED ))
                if CONFIG .wipes_all_saves_on_death ():
                    self .ui .tprint (c ("TODOS os saves deste personagem serao APAGADOS.",Color .BRIGHT_RED ))
                else :
                    self .ui .tprint (c ("O save sera marcado como MORTO.",Color .RED ))
                self .ui .pause ()
                try :
                    from save_system import wipe_all_saves_for_character ,save_death_to_all_slots 
                    if CONFIG .wipes_all_saves_on_death ():
                        wipe_all_saves_for_character (self .player .name ,ui_module =self .ui )
                    else :
                        save_death_to_all_slots (self .player ,ui_module =self .ui )
                except Exception :
                    pass 
                return "permadeath"
            else :

                if CONFIG .auto_save :
                    try :
                        from save_system import save_death_to_all_slots
                        save_death_to_all_slots (self .player ,ui_module =self .ui )
                    except Exception :
                        pass

        elif result =="fled":
            self .fled =True 
            self .ui .tprint (c ("Voce fugiu da batalha.",Color .YELLOW ))
            self .player .reset_combat_sukuna_state ()
            self .player .karma .add_reputacao (-1 )
            try :
                from save_system import autosave_after_battle
                autosave_after_battle (self .player ,ui_module =self .ui )
            except Exception :
                pass 

        elif result =="transformed":
            self .sukuna_transformed =True
            self .ui .tprint (c ("!! SUKUNA ASSUMIU O CONTROLE !!",Color .BRIGHT_RED +Color .BOLD +Color .BLINK ))
            self .ui .tprint (c ("Voce nao eh mais voce.",Color .RED ))
            self .ui .pause ()

            try :
                from save_system import save_death_to_all_slots
                save_death_to_all_slots (self .player ,ui_module =self .ui )
            except Exception :
                pass
            return "transformed"

        self .ui .combat_separator ()
        self .ui .pause ()
        return result 

