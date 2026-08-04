
import random 

def calculate_damage (dmg ,defense ):

    if dmg <=0 :
        return 1 
    if defense <=0 :
        return max (1 ,int (dmg ))
    reduction =min (0.75 ,defense /(defense +140.0 ))
    actual =int (dmg *(1.0 -reduction ))
    return max (1 ,actual )

from ui import Color ,c
from config import CONFIG
from techniques import (INNATE_TECHNIQUES ,BIRTH_TRAITS ,
roll_innate_technique ,roll_birth_trait ,
roll_heavenly_restriction ,can_use_rct )
from rank_system import RankSystem ,LevelSystem
from karma import KarmaSystem
from items import ITEMS_DB

class Player :

    def __init__ (self ,name ="Despertado"):
        self .name =name 
        self .attributes ={
        "forca":random .randint (5 ,15 ),
        "ce":random .randint (3 ,12 ),
        "controle":random .randint (4 ,12 ),
        "velocidade":random .randint (5 ,14 ),
        "vigor":random .randint (5 ,14 ),
        "sorte":random .randint (3 ,13 ),
        }
        self .innate_technique ="Sem Tecnica"
        self .birth_trait ="Nenhum Traço"
        self .heavenly_restriction =False 

        self .hp =0 
        self .max_hp =0 
        self .ce_current =0 
        self .max_ce =0 
        self .stamina =100 
        self .max_stamina =100 

        self .rank_system =RankSystem ()
        self .level_system =LevelSystem ()
        self .karma =KarmaSystem ()

        self .dodge_bonus =0 
        self .defense_buff =0 
        self .attack_buff =0 
        self .speed_buff =0 
        self .buffs =[]
        self .debuffs =[]
        self .bleed_stacks =0 
        self .burn_stacks =0 
        self .poison_stacks =0 
        self .stunned_turns =0 
        self .exhausted_turns =0 
        self .domain_active_turns =0 
        self .domain_used_count =0 

        self .sukuna_fingers_eaten =0 
        self .sukuna_control_pct =0 
        self .sukuna_fingers_in_inventory =0 

        self .inventory ={}
        self .equipped ={"arma":None ,"amuletos":[None ,None ,None ,None ,None ]}
        self .money =200 

        self .auto_allocate_build =None
        self .auto_sell_list =[]
        self .technique_roulette_count =0 
        self .trait_roulette_count =0 

        self .kills_total =0 
        self .battles_won =0 
        self .battles_lost =0 
        self .missions_completed =0 
        self .dungeons_explored =0 
        self .gojo_met =False 
        self .heitor_unlocked =False 
        self .infinite_resources_active =False 
        self .dmg_taken_this_combat =0 
        self .rika_summoned =False 
        self .rika_ce_upkeep =0 
        self .copied_technique =None 
        self .urgent_contract =None 
        self .questline_progress =None 
        self .questlines_completed =[]
        self ._last_combat_turns =None 
        self ._last_combat_techniques_used =[]
        self .playtime_turns =0 

        self .learned_simple_domain =False 
        self .learned_rct =False 
        self .gojo_trained_count =0 
        self .nanami_trained_count =0 
        self .todo_trained_count =0 

        self .completed_stories =set ()
        self .mentors_used_once =set ()
        self .xp_mult_battles_left =0 
        self .dmg_buff_next_battle =0.0 

        self .mentor_last_used ={}

        self .tamed_shikigami =[]
        self .sukuna_mastered =False 
        self .sukuna_takeover_active =False 
        self .sukuna_takeover_turns_left =0 
        self .sukuna_takeover_triggered_this_battle =False 
        self .sukuna_takeover_duration =5 

        self .technique_xp =0 
        self .technique_level =1 

        self .active_domain =None 
        self .active_domain_used_count =0 

        self .frame_stacks =0
        self .frame_locks_enemy ={}

        self ._pending_reflect_dmg =0

        self .location ="Escola Jujutsu"

    def generate_character (self ,ui_module =None ):

        if ui_module :
            ui_module .screen_header (ui_module .ASCII_AWAKENING ,"O DESPERTAR",color =ui_module .Color .BRIGHT_MAGENTA )
            ui_module .tprint ("\nA energia amaldicoada dentro de voce comeca a se manifestar...")
            ui_module .pause ()

        self .heavenly_restriction =roll_heavenly_restriction ()

        if self .heavenly_restriction :

            self .attributes ["ce"]=1 
            self .attributes ["controle"]=1 
            self .attributes ["forca"]=30 
            self .attributes ["velocidade"]=25 
            self .attributes ["vigor"]=25 
            self .max_ce =5 
            self .ce_current =5 
            self .innate_technique ="Sem Tecnica"
            if ui_module :
                candidates =[n for n in INNATE_TECHNIQUES if n !="Sem Tecnica"]
                ui_module .roulette_reveal (candidates ,"RESTRICAO CELESTIAL",label ="Sorteando destino",
                color =ui_module .Color .BRIGHT_YELLOW ,spins =16 )
                ui_module .tprint (c ("\n!!! RESTRICAO CELESTIAL - EXTREMAMENTE RARO !!!",
                ui_module .Color .BRIGHT_YELLOW +ui_module .Color .BOLD ))
                ui_module .section ("Restricao Celestial",[
                "Sua CE eh quase zero, mas seu corpo transcende o humano.",
                "Forca, velocidade e reflexos sao absurdos.",
                ],color =ui_module .Color .BRIGHT_YELLOW )
                ui_module .pause ()
        else :

            self .innate_technique =roll_innate_technique ()
            tech =INNATE_TECHNIQUES [self .innate_technique ]
            if ui_module :
                candidates =[n for n ,d in INNATE_TECHNIQUES .items ()if d .get ("weight",0 )>0 ]
                ui_module .roulette_reveal (candidates ,self .innate_technique ,label ="Sorteando tecnica inata",
                color =ui_module .Color .BRIGHT_MAGENTA ,spins =16 )
                weight =tech .get ("weight",5 )
                if weight <=1 :
                    rarity ="!!! LENDARIO !!!" 
                elif weight <=3 :
                    rarity ="RARO" 
                elif weight <=6 :
                    rarity ="INCOMUM" 
                else :
                    rarity ="COMUM" 
                ui_module .tprint (c (f"\n[{rarity }]",ui_module .Color .BRIGHT_YELLOW +ui_module .Color .BOLD ))
                ui_module .section (f"Tecnica Inata: {self .innate_technique }",[tech ["desc"]],
                color =ui_module .Color .BRIGHT_MAGENTA )
                ui_module .pause ()

        self .birth_trait =roll_birth_trait ()
        trait =BIRTH_TRAITS [self .birth_trait ]
        if ui_module :
            trait_candidates =[n for n ,d in BIRTH_TRAITS .items ()if d .get ("weight",0 )>0 ]
            ui_module .roulette_reveal (trait_candidates ,self .birth_trait ,label ="Sorteando traco de nascimento",
            color =ui_module .Color .BRIGHT_BLUE ,spins =16 )
            t_weight =trait .get ("weight",5 )
            if t_weight <=1 :
                t_rarity ="!!! LENDARIO !!!" 
            elif t_weight <=3 :
                t_rarity ="RARO" 
            elif t_weight <=6 :
                t_rarity ="INCOMUM" 
            else :
                t_rarity ="COMUM" 
            ui_module .tprint (c (f"\n[{t_rarity }]",ui_module .Color .BRIGHT_YELLOW +ui_module .Color .BOLD ))
            ui_module .section (f"Traco de Nascimento: {self .birth_trait }",[trait ["desc"]],
            color =ui_module .Color .BRIGHT_BLUE )
            ui_module .pause ()

        self .recalculate_derived ()

        self .hp =self .max_hp 
        self .ce_current =self .max_ce 

        if ui_module :
            ui_module .tprint (c ("\nDespertar completo.",Color .BRIGHT_GREEN ))
            ui_module .pause ()

    def recalculate_derived (self ):
        a =self .attributes 

        hp_base =80 +a ["vigor"]*12 +(self .level_system .level *18 )

        trait =BIRTH_TRAITS .get (self .birth_trait ,{})
        trait_effects =trait .get ("effects",{})

        if self .heavenly_restriction :
            hp_base =250 +a ["vigor"]*22 +(self .level_system .level *25 )

        for item_name in self ._iter_equipped_items ():
            if item_name and item_name in ITEMS_DB :
                eff =ITEMS_DB [item_name ].get ("effect",{})
                if "hp_bonus"in eff :
                    hp_base +=eff ["hp_bonus"]
                if "hp_max_pct_bonus"in eff :
                    hp_base =int (hp_base *(1.0 +eff ["hp_max_pct_bonus"]))

        if self .sukuna_fingers_eaten >0 :
            hp_base +=self .sukuna_fingers_eaten *80 

        if "hp_max_penalty"in trait_effects :
            hp_base =int (hp_base *trait_effects ["hp_max_penalty"])

        try :
            hp_base =int (hp_base *CONFIG .get_player_hp_mult ())
        except Exception :
            pass 

        old_max =self .max_hp 
        self .max_hp =hp_base 
        if old_max >0 :
            if self .max_hp <old_max :
                self .hp =min (self .hp ,self .max_hp )
            else :
                ratio =self .hp /old_max 
                self .hp =min (self .max_hp ,int (self .max_hp *ratio ))
        else :
            self .hp =self .max_hp 

        if self .heavenly_restriction :
            self .max_ce =5 
        else :
            ce_base =40 +a ["ce"]*7 +(self .level_system .level *8 )
            if "ce_max_bonus"in trait_effects :
                ce_base =int (ce_base *trait_effects ["ce_max_bonus"])
            if "ce_max_penalty"in trait_effects :
                ce_base =int (ce_base *trait_effects ["ce_max_penalty"])
            try :
                ce_base =int (ce_base *CONFIG .get_player_ce_mult ())
            except Exception :
                pass 
            self .max_ce =ce_base 

        if self .ce_current >self .max_ce :
            self .ce_current =self .max_ce 

    def _iter_equipped_items (self ):
        if self .equipped .get ("arma"):
            yield self .equipped ["arma"]
        amuletos =self .equipped .get ("amuletos")or []
        for amul in amuletos :
            if amul :
                yield amul 

    def _iter_equipped_amulets (self ):
        amuletos =self .equipped .get ("amuletos")or []
        for amul in amuletos :
            if amul :
                yield amul 

    def add_buff (self ,buff_type ,value ,duration ,name =""):
        self .buffs .append ({
        "type":buff_type ,
        "value":value ,
        "duration":duration ,
        "name":name or buff_type ,
        })

    def add_debuff (self ,debuff_type ,value ,duration ,name =""):
        self .debuffs .append ({
        "type":debuff_type ,
        "value":value ,
        "duration":duration ,
        "name":name or debuff_type ,
        })

    def tick_buffs (self ):

        msgs =[]
        for buff in self .buffs [:]:
            buff ["duration"]-=1 
            if buff ["duration"]<=0 :
                msgs .append (f"Buff '{buff ['name']}' expirou.")
                self .buffs .remove (buff )
        for debuff in self .debuffs [:]:
            debuff ["duration"]-=1 
            if debuff ["duration"]<=0 :
                msgs .append (f"Debuff '{debuff ['name']}' expirou.")
                self .debuffs .remove (debuff )

        if self .bleed_stacks >0 :
            bleed_dmg =self .bleed_stacks *5 
            self .hp -=bleed_dmg 
            if self .hp <0 :self .hp =0 
            msgs .append (f"Sangramento causa {bleed_dmg } de dano.")
            self .bleed_stacks =max (0 ,self .bleed_stacks -1 )

        if self .burn_stacks >0 :
            burn_dmg =self .burn_stacks *7 
            self .hp -=burn_dmg 
            if self .hp <0 :self .hp =0 
            msgs .append (f"Queimadura causa {burn_dmg } de dano.")
            self .burn_stacks =max (0 ,self .burn_stacks -1 )

        if self .poison_stacks >0 :
            poison_dmg =self .poison_stacks *4
            self .hp -=poison_dmg
            if self .hp <0 :self .hp =0
            msgs .append (f"Veneno causa {poison_dmg } de dano.")
            self .poison_stacks =max (0 ,self .poison_stacks -1 )

        if self .exhausted_turns >0 :
            self .exhausted_turns -=1

        ce_drain =self .get_buff_value ("ce_drain")
        if ce_drain >0 :
            self .ce_current =max (0 ,self .ce_current -ce_drain )
            msgs .append (f"Campo de CE drena {ce_drain } de CE.")

        if self .domain_active_turns >0 :
            self .domain_active_turns -=1

        return msgs 

    def get_buff_value (self ,buff_type ,default =0 ):

        return sum (b ["value"]for b in self .buffs if b ["type"]==buff_type )

    def get_debuff_value (self ,debuff_type ,default =0 ):
        return sum (d ["value"]for d in self .debuffs if d ["type"]==debuff_type )

    def get_total_str (self ):

        base =self .attributes ["forca"]
        if self .heavenly_restriction :
            base =int (base *2.0 )
        tech =INNATE_TECHNIQUES .get (self .innate_technique ,{})
        tech_bonus =tech .get ("passive_bonus",{}).get ("physical_bonus",1.0 )
        if tech_bonus >1.0 :
            base =int (base *tech_bonus )

        for item_name in self ._iter_equipped_items ():
            if item_name and item_name in ITEMS_DB :
                eff =ITEMS_DB [item_name ].get ("effect",{})
                base +=eff .get ("str_bonus",0 )
        if self .sukuna_fingers_eaten >0 :
            base =int (base *(1.0 +self .get_sukuna_finger_bonus ()))
            base +=self .sukuna_fingers_eaten *5 
        base +=self .level_system .level *2 

        base +=self .get_buff_value ("str")
        base +=self .get_buff_value ("attack_flat")

        base -=self .get_debuff_value ("str_down")
        base =int (base *self .get_sukuna_takeover_modifier ())
        if self .exhausted_turns >0 :
            base =int (base *0.5 )
        return max (1 ,base )

    def get_total_def (self ):

        base =self .attributes .get ("vigor",10 )//2 

        if self .heavenly_restriction :
            base =int (base *2.5 )

        tech =INNATE_TECHNIQUES .get (self .innate_technique ,{})
        tech_bonus =tech .get ("passive_bonus",{}).get ("ce_reinforcement",1.0 )
        if tech_bonus >1.0 :
            base =int (base *tech_bonus )
        if self .innate_technique =="Limitless":
            if self .technique_level >=15 :
                base =int (base *1.6 )
            else :
                base =int (base *1.3 )

        for item_name in self ._iter_equipped_items ():
            if item_name and item_name in ITEMS_DB :
                eff =ITEMS_DB [item_name ].get ("effect",{})
                base +=eff .get ("def_bonus",0 )
        if self .sukuna_fingers_eaten >0 :
            base =int (base *(1.0 +min (0.80 ,self .sukuna_fingers_eaten *0.10 )))

        base +=self .get_buff_value ("defense_flat")
        base +=self .get_buff_value ("def")
        base =int (base *self .get_sukuna_takeover_modifier ())
        if self .exhausted_turns >0 :
            base =int (base *0.5 )
        return max (1 ,base )

    def get_total_speed (self ):

        base =self .attributes ["velocidade"]
        if self .heavenly_restriction :
            base =int (base *2.0 )
        tech =INNATE_TECHNIQUES .get (self .innate_technique ,{})
        if "speed"in tech .get ("passive_bonus",{}):
            base =int (base *tech ["passive_bonus"]["speed"])

        trait =BIRTH_TRAITS .get (self .birth_trait ,{})
        if "speed_bonus"in trait .get ("effects",{}):
            base =int (base *trait ["effects"]["speed_bonus"])

        for item_name in self ._iter_equipped_items ():
            if item_name and item_name in ITEMS_DB :
                eff =ITEMS_DB [item_name ].get ("effect",{})
                base +=eff .get ("speed_bonus",0 )
                if "speed_bonus_pct"in eff :
                    base =int (base *(1.0 +eff ["speed_bonus_pct"]))
        if self .sukuna_fingers_eaten >0 :
            base =int (base *(1.0 +self .get_sukuna_finger_bonus ()))
            base +=self .sukuna_fingers_eaten *5 

        speed_buff =self .get_buff_value ("speed")
        if speed_buff >0 :
            base +=speed_buff 
        base =int (base *self .get_sukuna_takeover_modifier ())
        if self .exhausted_turns >0 :
            base =int (base *0.5 )
        return max (1 ,base )

    def get_total_luck (self ):

        base =self .attributes ["sorte"]
        trait =BIRTH_TRAITS .get (self .birth_trait ,{})
        if "luck"in trait .get ("effects",{}):
            base =int (base *trait ["effects"]["luck"])
        if self .birth_trait =="Sorte de Sukuna":
            base =int (base *2.0 )

        for item_name in self ._iter_equipped_items ():
            if item_name and item_name in ITEMS_DB :
                eff =ITEMS_DB [item_name ].get ("effect",{})
                base +=eff .get ("luck_bonus",0 )
        base =int (base *self .get_sukuna_takeover_modifier ())
        return max (1 ,base )

    def get_total_control (self ):

        base =self .attributes ["controle"]
        trait =BIRTH_TRAITS .get (self .birth_trait ,{})
        if "control_bonus"in trait .get ("effects",{}):
            base =int (base *trait ["effects"]["control_bonus"])
        tech =INNATE_TECHNIQUES .get (self .innate_technique ,{})
        if "control_bonus"in tech .get ("passive_bonus",{}):
            base =int (base *tech ["passive_bonus"]["control_bonus"])
        base =int (base *self .get_sukuna_takeover_modifier ())
        return max (1 ,base )

    def get_ce_efficiency (self ):

        base =1.0 
        tech =INNATE_TECHNIQUES .get (self .innate_technique ,{})
        if "ce_efficiency"in tech .get ("passive_bonus",{}):
            base *=tech ["passive_bonus"]["ce_efficiency"]
        trait =BIRTH_TRAITS .get (self .birth_trait ,{})
        if "ce_efficiency"in trait .get ("effects",{}):
            base *=trait ["effects"]["ce_efficiency"]
        if self .birth_trait =="Seis Olhos (Six Eyes)"and self .innate_technique =="Limitless":
            base *=1.7 
        base *=self .get_sukuna_takeover_modifier ()
        return base 

    def get_dodge_chance (self ):

        base =0.05 
        speed =self .get_total_speed ()
        base +=speed *0.005 
        tech =INNATE_TECHNIQUES .get (self .innate_technique ,{})
        if "dodge"in tech .get ("passive_bonus",{}):
            base *=tech ["passive_bonus"]["dodge"]
        trait =BIRTH_TRAITS .get (self .birth_trait ,{})
        if "dodge"in trait .get ("effects",{}):
            base *=trait ["effects"]["dodge"]
        if self .birth_trait =="Seis Olhos (Six Eyes)":
            base +=0.45 
        if self .innate_technique =="Projection Sorcery":
            base +=0.25 
        if self .get_buff_value ("boogie_dodge")>0 :
            base +=0.15 

        if self .sukuna_fingers_eaten >0 :
            base *=max (0.5 ,1.0 -self .sukuna_fingers_eaten *0.05 )
        base +=self .get_buff_value ("dodge_flat")*0.01 
        return min (0.85 ,base )

    def get_black_flash_chance (self ):

        base =0.05 
        base +=self .get_total_luck ()*0.005 

        trait =BIRTH_TRAITS .get (self .birth_trait ,{})
        if "counter_chance"in trait .get ("effects",{}):
            base +=trait ["effects"]["counter_chance"]
        if "crit_chance_bonus"in trait .get ("effects",{}):
            base +=trait ["effects"]["crit_chance_bonus"]
        if self .get_buff_value ("boogie_crit")>0 :
            base +=0.15 
        for item_name in self ._iter_equipped_items ():
            if item_name and item_name in ITEMS_DB :
                eff =ITEMS_DB [item_name ].get ("effect",{})
                if "black_flash_bonus"in eff :
                    base +=eff ["black_flash_bonus"]
                if "crit_bonus"in eff :
                    base +=eff ["crit_bonus"]
        if self .sukuna_fingers_eaten >0 :
            base +=self .sukuna_fingers_eaten *0.03 
        return min (0.95 ,base )

    def add_item (self ,item_name ,qty =1 ):
        self .inventory [item_name ]=self .inventory .get (item_name ,0 )+qty 

    def remove_item (self ,item_name ,qty =1 ):
        if item_name not in self .inventory :
            return False 
        if self .inventory [item_name ]<qty :
            return False 
        self .inventory [item_name ]-=qty 
        if self .inventory [item_name ]<=0 :
            del self .inventory [item_name ]
        return True 

    def has_item (self ,item_name ):
        return self .inventory .get (item_name ,0 )>0 

    def get_items_by_type (self ,type_name ):

        return {n :q for n ,q in self .inventory .items ()
        if n in ITEMS_DB and ITEMS_DB [n ]["type"]==type_name }

    def use_consumable (self ,item_name ,ui_module =None ):

        if item_name not in self .inventory :
            return False 
        item =ITEMS_DB .get (item_name )
        if not item or item ["type"]!="consumivel":
            return False 

        eff =item ["effect"]

        if "revive_pct"in eff :
            if ui_module :
                ui_module .tprint (c (f"{item_name } eh um selo passivo.",Color .YELLOW ))
                ui_module .tprint (c ("Ele se ativa SOZINHO quando voce morre em batalha, revivendo com "
                f"{int (eff ['revive_pct']*100 )}% HP.",Color .DIM ))
                ui_module .tprint (c ("Nao precisa (e nao pode) ser ativado manualmente.",Color .DIM ))
            return False 
        if "guaranteed_flee"in eff :
            if ui_module :
                ui_module .tprint (c (f"{item_name } eh passivo.",Color .YELLOW ))
                ui_module .tprint (c ("Ele se ativa SOZINHO quando voce tenta fugir em combate.",Color .DIM ))
                ui_module .tprint (c ("Apenas tente fugir e o pergaminho garantira a fuga.",Color .DIM ))
            return False 

        msg =f"Usou {item_name }. "
        if "hp_restore"in eff :
            heal =eff ["hp_restore"]
            old_hp =self .hp 
            self .hp =min (self .max_hp ,self .hp +heal )
            actual =self .hp -old_hp 
            msg +=f"+{actual } HP. "
        if "hp_restore_full"in eff :
            self .hp =self .max_hp 
            msg +="HP maximo. "
        if "ce_restore"in eff :
            self .ce_current =min (self .max_ce ,self .ce_current +eff ["ce_restore"])
            msg +=f"+{eff ['ce_restore']} CE. "
        if "ce_restore_full"in eff :
            self .ce_current =self .max_ce 
            msg +="CE maximo. "
        if "dmg_buff_next_battle"in eff :
            self .dmg_buff_next_battle =eff ["dmg_buff_next_battle"]
            msg +=f"+{int (eff ['dmg_buff_next_battle']*100 )}% dano na proxima batalha. "
        if "remove_sukuna_finger"in eff and eff ["remove_sukuna_finger"]:
            if self .sukuna_fingers_eaten >0 :
                self .sukuna_fingers_eaten -=1 

                self .sukuna_control_pct =max (0 ,self .sukuna_control_pct -20 )
                if self .sukuna_fingers_eaten ==0 :
                    self .sukuna_mastered =False 
                msg +="1 Dedo de Sukuna removido com seguranca! -20% controle do Sukuna. "
                self .recalculate_derived ()
            else :
                msg +="(Nenhum dedo ingerido para remover.) "

        self .remove_item (item_name )
        if ui_module :
            ui_module .tprint (c (msg ,Color .GREEN ))
        return True 

    def use_cursed_item (self ,item_name ,ui_module =None ):

        if item_name not in self .inventory :
            return False 
        item =ITEMS_DB .get (item_name )
        if not item or item ["type"]!="amaldicoado":
            return False 

        eff =item .get ("effect",{})
        msg =f"Voce usa {item_name }...\n"

        if "random_curse_or_item"in eff :
            if random .random ()<0.5 :

                from items import roll_loot 
                loot =roll_loot (1.5 )
                if loot =="Dedo de Sukuna":
                    self .sukuna_fingers_in_inventory +=1 
                else :
                    self .add_item (loot )
                msg +=f"A caixa se abre revelando: {loot }!"
            else :

                dmg =random .randint (20 ,60 )
                self .hp =max (1 ,self .hp -dmg )
                msg +=f"A caixa era uma armadilha! Maldicao emerge e te ataca: -{dmg } HP."

                self .add_item ("Osso de Maldicao")
                msg +=" Voce conseguiu sair com um Osso de Maldicao."

        elif "mental_damage"in eff :

            if self .attributes .get ("controle",0 )>5 :
                self .attributes ["controle"]-=2 
                msg +="O espelho mostra seu futuro sombrio. -2 Controle."

            mental_dmg =int (self .hp *0.10 )
            self .hp =max (1 ,self .hp -mental_dmg )
            msg +=f" Dano mental: -{mental_dmg } HP."

            self .level_system .xp_mult =1.5 
            self .xp_mult_battles_left =3 
            msg +=" Em troca, voce ganha +50% XP por 3 batalhas."
            self .recalculate_derived ()

        elif "possession_risk"in eff :

            if random .random ()<0.5 :
                self .attributes ["forca"]+=5 
                self .attributes ["ce"]+=3 
                msg +="Sukuna abencoado! +5 Forca, +3 CE."
                self .recalculate_derived ()
                self .hp =self .max_hp 
            else :
                if self .sukuna_mastered :
                    self .sukuna_control_pct =min (100 ,self .sukuna_control_pct +30 )
                    msg +=f"O anel intensifica a presenca de Sukuna! Controle Sukuna: +30% (agora {self .sukuna_control_pct }%)."
                    if self .sukuna_control_pct >=100 :
                        msg +=" SUKUNA ASSUMIU O CONTROLE TOTAL!"
                        if ui_module :
                            ui_module .tprint (c (msg ,Color .BRIGHT_RED +Color .BOLD ))
                        self .remove_item (item_name )
                        return "transformed"
                else :
                    dmg =random .randint (30 ,80 )
                    self .hp =max (1 ,self .hp -dmg )
                    msg +=f"Sukuna rejeita voce! -{dmg } HP."

        elif "random_status_points"in eff :
            n_points =random .randint (3 ,5 )
            attr_keys =list (self .attributes .keys ())
            gained ={}
            for _ in range (n_points ):
                attr =random .choice (attr_keys )
                self .attributes [attr ]=self .attributes .get (attr ,0 )+1 
                gained [attr ]=gained .get (attr ,0 )+1 
            msg +=f"Selo de Status concedeu {n_points } pontos: "
            msg +=", ".join (f"+{v } {k }"for k ,v in gained .items ())+"."
            self .recalculate_derived ()

        elif "summon_random_canon_boss"in eff :
            from enemies import BOSSES 
            eligible =[name for name ,b in BOSSES .items ()
            if not b .get ("is_sorcerer_boss")and name !="Sukuna"]
            if not eligible :
                msg +="O anel esta vazio..."
            else :
                chosen =random .choice (eligible )
                from enemies import get_boss 
                boss =get_boss (chosen )
                if boss :
                    from combat import Combat 
                    combat_inst =Combat (self ,[boss ],ui_module )
                    result =combat_inst .start ()
                    msg +=f"O Anel do Caos invocou {chosen }!"
                    if result =="defeat"or result =="permadeath"or result =="transformed":
                        self .remove_item (item_name )
                        if ui_module :
                            ui_module .tprint (c (msg ,Color .MAGENTA ))
                        return result if result =="transformed"else True 
                else :
                    msg +="O anel falhou em invocar algo."

        self .remove_item (item_name )
        if ui_module :
            ui_module .tprint (c (msg ,Color .MAGENTA ))
        return True 

    def get_usable_items (self ):

        usable ={}
        for name ,qty in self .inventory .items ():
            item =ITEMS_DB .get (name )
            if item and item ["type"]in ("consumivel","amaldicoado"):
                usable [name ]=qty 
        return usable 

    def take_damage (self ,dmg ,damage_type ="physical",ignore_def =False ):

        if ignore_def :
            actual =dmg 
        else :
            defense =self .get_total_def ()
            actual =calculate_damage (dmg ,defense )
            if damage_type =="physical":

                trait =BIRTH_TRAITS .get (self .birth_trait ,{})
                if "physical_defense"in trait .get ("effects",{}):
                    actual =int (actual /trait ["effects"]["physical_defense"])

            for item_name in self ._iter_equipped_items ():
                if item_name and item_name in ITEMS_DB :
                    e =ITEMS_DB [item_name ].get ("effect",{})
                    if damage_type =="cursed"and "ce_dmg_reduce"in e :
                        actual =int (actual *(1.0 -e ["ce_dmg_reduce"]))

        if self .get_buff_value ("shadow_shield")>0 :

            self ._consume_buff ("shadow_shield")
            return 0

        if self .get_buff_value ("incoming_dmg_reduction_pct")>0 :
            reduction =self .get_buff_value ("incoming_dmg_reduction_pct")
            actual =int (actual *(1.0 -reduction /100.0 ))
            self ._consume_buff ("incoming_dmg_reduction_pct")

        if self .get_buff_value ("incoming_dmg_pct")>0 :
            increase =self .get_buff_value ("incoming_dmg_pct")
            actual =int (actual *(1.0 +increase /100.0 ))
            self ._consume_buff ("incoming_dmg_pct")

        if self .get_buff_value ("soul_distort_def")>0 :
            if random .random ()<0.30 :
                reflected =int (actual *0.20 )
                self ._pending_reflect_dmg =getattr (self ,"_pending_reflect_dmg",0 )+reflected
        self .hp -=actual
        if self .hp <0 :
            self .hp =0
        self .dmg_taken_this_combat +=actual 
        return actual

    def _consume_buff (self ,buff_type ):
        for b in self .buffs [:]:
            if b ["type"]==buff_type :
                self .buffs .remove (b )
                return

    def has_special_buff (self ,buff_type ):
        return self .get_buff_value (buff_type )>0

    def restore_ce (self ,amount ):
        if self .sukuna_takeover_active :
            return 
        self .ce_current =min (self .max_ce ,self .ce_current +amount )

    def spend_ce (self ,amount ):

        actual_cost =int (amount /self .get_ce_efficiency ())
        if self .ce_current <actual_cost :
            return False 
        self .ce_current -=actual_cost 
        return True 

    def is_dead (self ):
        return self .hp <=0 

    def is_stunned (self ):
        return self .stunned_turns >0 

    def is_exhausted (self ):
        return self .exhausted_turns >0 

    DOMAIN_SIMPLE_MIN_LEVEL =10 
    DOMAIN_FULL_MIN_LEVEL =20 
    DOMAIN_SIMPLE_CE_COST =25 
    DOMAIN_FULL_MIN_CE_PCT =0.70 

    def has_domain_available (self ):

        if self .sukuna_mastered and self .level_system .level >=self .DOMAIN_FULL_MIN_LEVEL :
            return True 
        tech =INNATE_TECHNIQUES .get (self .innate_technique ,{})
        if tech .get ("domain")and self .level_system .level >=self .DOMAIN_FULL_MIN_LEVEL :
            return True 
        if self .learned_simple_domain and self .level_system .level >=self .DOMAIN_SIMPLE_MIN_LEVEL :
            return True 
        return False 

    def can_use_domain (self ):

        if self .domain_used_count >=1 :
            return False ,"Dominio ja usado nesta batalha"

        is_simple =False 
        if self .sukuna_mastered and self .level_system .level >=self .DOMAIN_FULL_MIN_LEVEL :
            is_simple =False 
        else :
            tech =INNATE_TECHNIQUES .get (self .innate_technique ,{})
            if tech .get ("domain")and self .level_system .level >=self .DOMAIN_FULL_MIN_LEVEL :
                is_simple =False 
            elif self .learned_simple_domain and self .level_system .level >=self .DOMAIN_SIMPLE_MIN_LEVEL :
                is_simple =True 
            else :
                if self .level_system .level <self .DOMAIN_SIMPLE_MIN_LEVEL :
                    return False ,f"Requer Level {self .DOMAIN_SIMPLE_MIN_LEVEL }+ (Dominio Simples)"
                return False ,"Sua tecnica nao tem dominio"

        if is_simple :

            if self .ce_current <self .DOMAIN_SIMPLE_CE_COST :
                return False ,f"Precisa de {self .DOMAIN_SIMPLE_CE_COST } CE (Dominio Simples)"
        else :

            required_ce =int (self .max_ce *self .DOMAIN_FULL_MIN_CE_PCT )
            if self .ce_current <required_ce :
                pct_have =int ((self .ce_current /max (1 ,self .max_ce ))*100 )
                pct_need =int (self .DOMAIN_FULL_MIN_CE_PCT *100 )
                return False ,f"CE insuficiente: {pct_have }% (precisa {pct_need }%)"

        return True ,"OK"

    def get_domain_name (self ):

        if self .sukuna_mastered and self .level_system .level >=self .DOMAIN_FULL_MIN_LEVEL :
            if self .sukuna_fingers_eaten >=18 :
                return "Malevolent Shrine"
            if self .sukuna_fingers_eaten >=12 :
                return "Incomplete Malevolent Shrine"
        tech =INNATE_TECHNIQUES .get (self .innate_technique ,{})
        if tech .get ("domain")and self .level_system .level >=self .DOMAIN_FULL_MIN_LEVEL :
            return tech .get ("domain")
        if self .learned_simple_domain and self .level_system .level >=self .DOMAIN_SIMPLE_MIN_LEVEL :
            return "Dominio Simples"
        return None 

    def is_simple_domain (self ):

        name =self .get_domain_name ()
        return name =="Dominio Simples"

    def reset_combat_state (self ):

        self .buffs .clear ()
        self .debuffs .clear ()
        self .bleed_stacks =0 
        self .burn_stacks =0 
        self .poison_stacks =0 
        self .stunned_turns =0 
        self .exhausted_turns =0 
        self .domain_active_turns =0 
        self .domain_used_count =0 
        self .dodge_bonus =0 
        self .defense_buff =0 
        self .attack_buff =0 
        self .speed_buff =0 
        self .sukuna_takeover_active =False 
        self .sukuna_takeover_turns_left =0 
        self .sukuna_takeover_triggered_this_battle =False 
        self .active_domain =None 
        self .active_domain_used_count =0 
        self .frame_stacks =0 
        self .frame_locks_enemy ={}

    def xp_to_next_technique_level (self ):

        return int (200 *(self .technique_level **1.5 ))

    def add_technique_xp (self ,amount ):

        self .technique_xp +=amount 
        levels_gained =0 
        stage_changed =False 
        old_stage =self ._get_technique_stage ()
        while self .technique_xp >=self .xp_to_next_technique_level ():
            self .technique_xp -=self .xp_to_next_technique_level ()
            self .technique_level +=1 
            levels_gained +=1 
        new_stage =self ._get_technique_stage ()
        if new_stage !=old_stage :
            stage_changed =True 
        return levels_gained >0 ,levels_gained ,stage_changed 

    def _get_technique_stage (self ):

        if self .innate_technique =="Limitless":
            if self .technique_level >=15 :
                return "Despertado"
            return "J"
        return "Padrao"

    def get_technique_stage_label (self ):

        stage =self ._get_technique_stage ()
        if stage =="J":
            return "Limitless (J) - Juventude"
        elif stage =="Despertado":
            return "Limitless - Despertado"
        return self .innate_technique 

    TECHNIQUES_WITH_XP_EVOLUTION ={"Limitless"}

    def has_technique_evolution (self ):

        return self .innate_technique in self .TECHNIQUES_WITH_XP_EVOLUTION 

    def can_use_rct (self ):
        return can_use_rct (self )

    SUKUNA_MAX_FINGERS =20 

    def eat_sukuna_finger (self ,ui_module =None ):

        if self .sukuna_fingers_in_inventory <=0 :
            return "no_finger"

        if self .sukuna_fingers_eaten >=self .SUKUNA_MAX_FINGERS :
            if ui_module :
                ui_module .tprint (c ("Voce ja ingeriu o maximo de dedos (20). Sukuna esta no maximo de poder.",Color .BRIGHT_RED ))
            return "max_reached"

        control =self .get_total_control ()
        luck =self .get_total_luck ()

        n =self .sukuna_fingers_eaten 
        death_chance =min (0.85 ,0.50 +n *0.03 )
        transform_chance =min (0.50 ,0.20 +n *0.02 )
        vomit_chance =max (0.10 ,0.25 -n *0.02 )
        success_chance =max (0.01 ,0.05 -n *0.005 )

        total =death_chance +transform_chance +vomit_chance +success_chance 
        death_chance /=total 
        transform_chance /=total 
        vomit_chance /=total 
        success_chance /=total 

        control_bonus =(control *0.005 )+(luck *0.003 )
        death_chance =max (0.10 ,death_chance -control_bonus )
        success_chance =min (0.40 ,success_chance +control_bonus *0.5 )

        total =death_chance +transform_chance +vomit_chance +success_chance 
        death_chance /=total 
        transform_chance /=total 
        vomit_chance /=total 
        success_chance /=total 

        roll =random .random ()

        if roll <death_chance :
            self .sukuna_fingers_in_inventory -=1 
            self .hp =0 
            if ui_module :
                ui_module .tprint (c ("Voce engole o dedo. Uma dor insuportavel percorre seu corpo.",Color .RED ))
                ui_module .tprint (c ("SUA CABECA EXPLODE EM ENERGIA MALDICOADA.",Color .BRIGHT_RED +Color .BOLD ))
                ui_module .tprint (c ("Sukuna ri enquanto voce morre. 'Fraco.'",Color .BRIGHT_RED ))
            return "death"
        elif roll <death_chance +transform_chance :
            self .sukuna_fingers_in_inventory -=1 
            if ui_module :
                ui_module .tprint (c ("O dedo entra. Sukuna ASSUME O CONTROLE.",Color .BRIGHT_RED +Color .BOLD ))
                ui_module .tprint (c ("Voce nao eh mais voce. Voce eh uma maldicao.",Color .RED ))
            return "transformed"
        elif roll <death_chance +transform_chance +vomit_chance :

            self .sukuna_fingers_in_inventory -=1 
            if ui_module :
                ui_module .tprint (c ("Voce tenta engolir, mas seu corpo REJEITA.",Color .YELLOW ))
                ui_module .tprint ("Voce vomita o dedo. Ele cai no chao.")
            return "vomit"
        else :

            self .sukuna_fingers_in_inventory -=1 
            self .sukuna_fingers_eaten +=1 
            self .sukuna_mastered =True 

            self .sukuna_control_pct =min (45 ,self .sukuna_control_pct +2 )

            unlocked =self ._check_sukuna_stage_unlocked (self .sukuna_fingers_eaten )
            if ui_module :
                ui_module .tprint (c ("Voce engole o dedo. Poder INFINITO flui em voce!",Color .BRIGHT_YELLOW +Color .BOLD ))
                ui_module .tprint (c (f"Dedos ingeridos: {self .sukuna_fingers_eaten }/{self .SUKUNA_MAX_FINGERS }",Color .BRIGHT_RED ))
                ui_module .tprint (c (f"Chance de Sukuna controlar: {self .sukuna_control_pct }% (max 45%)",Color .YELLOW ))
                if unlocked :
                    ui_module .tprint (c (f"!! STAGE DESBLOQUEADO: {unlocked } !!",Color .BRIGHT_MAGENTA +Color .BOLD ))
            self .recalculate_derived ()
            self .hp =self .max_hp 
            return "success"

    def _check_sukuna_stage_unlocked (self ,fingers ):

        stages ={
        1 :"Despertar dos Cortes (Dismantle + Cleave)",
        6 :"Aprimoramento (Dismantle/Cleave +0.3x, unlock Spiderweb Cut)",
        7 :"Chamas de Fuga (unlock Open: Fire Arrow)",
        8 :"Poder Crescente (todas +0.5x, unlock World Cutting Slash)",
        12 :"Domínio Incompleto (Incomplete Malevolent Shrine, todas +1x)",
        18 :"Poder Total (Malevolent Shrine completo, todas +3x)",
        }
        return stages .get (fingers )

    def get_sukuna_finger_bonus (self ):

        n =self .sukuna_fingers_eaten 
        if n ==0 :
            return 0.0 
        if n <=8 :
            return n *0.25 

        return 2.0 +(n -8 )*0.55 

    def get_sukuna_skill_bonus (self ):

        n =self .sukuna_fingers_eaten 
        bonus =0.0 

        bonus +=n *0.10 

        if n >=6 :
            bonus +=0.3 
        if n >=8 :
            bonus +=0.5 
        if n >=12 :
            bonus +=1.0 
        if n >=18 :
            bonus +=3.0 
        return bonus 

    def get_sukuna_def_ignore (self ):

        n =self .sukuna_fingers_eaten 
        if n ==0 :
            return 0.15 

        pct =0.15 
        if n >=6 :
            pct =0.25 
        if n >=8 :
            pct =0.40 
        if n >=12 :
            pct =0.50 
        if n >=18 :
            pct =0.75 
        return pct 

    def get_sukuna_unlocked_skills (self ):

        n =self .sukuna_fingers_eaten 
        skills =[]
        if n >=1 :
            skills .extend (["Dismantle","Cleave"])
        if n >=6 :
            skills .append ("Spiderweb Cut")
        if n >=7 :
            skills .append ("Open: Fire Arrow")
        if n >=8 :
            skills .append ("World Cutting Slash")
        return skills 

    def has_incomplete_malevolent_shrine (self ):

        return self .sukuna_fingers_eaten >=12 

    def has_malevolent_shrine (self ):

        return self .sukuna_fingers_eaten >=18 

    SUKUNA_TAKEOVER_CHANCE =0.05 
    SUKUNA_TAKEOVER_DURATION =5 
    SUKUNA_TAKEOVER_STAT_BONUS =0.88 

    def check_sukuna_takeover (self ,ui_module =None ):

        if not self .sukuna_mastered :
            return False 
        if self .sukuna_fingers_eaten ==0 :
            return False 

        if self .sukuna_takeover_active :
            if self .sukuna_takeover_turns_left >0 :
                if ui_module :
                    ui_module .tprint (c (f"\n!! Sukuna mantem o controle! ({self .sukuna_takeover_turns_left }t restante)",
                    Color .BRIGHT_RED +Color .BOLD ))
                return True 
            else :

                self .sukuna_takeover_active =False 
                if ui_module :
                    ui_module .tprint (c ("\nSukuna devolve o controle a voce. Por enquanto.",Color .YELLOW ))
                return False 

        if self .sukuna_takeover_triggered_this_battle :
            return False 

        chance =self .SUKUNA_TAKEOVER_CHANCE +(self .sukuna_fingers_eaten *0.02 )
        chance =min (0.45 ,chance )

        if random .random ()<chance :

            self .sukuna_takeover_active =True 
            self .sukuna_takeover_turns_left =self .SUKUNA_TAKEOVER_DURATION 
            self .sukuna_takeover_triggered_this_battle =True 
            if ui_module :
                ui_module .tprint (c ("\n!! SUKUNA ASSUME O CONTROLE !!",Color .BRIGHT_RED +Color .BOLD +Color .BLINK ))
                ui_module .tprint (c ("'Saia do meu caminho, inseto.'",Color .BRIGHT_RED ))
                ui_module .tprint (c (f"Duracao: {self .SUKUNA_TAKEOVER_DURATION } turnos | +{int (self .SUKUNA_TAKEOVER_STAT_BONUS *100 )}% em todos os stats de combate",
                Color .BRIGHT_YELLOW ))
                ui_module .tprint (c ("(CE e HP nao regeneram durante o controle de Sukuna)",Color .DIM ))
                ui_module .tprint (c ("(Sukuna pode fazer tudo menos fugir)",Color .DIM ))
            return True 

        self .sukuna_takeover_triggered_this_battle =True 
        return False 

    def sukuna_takeover_attack (self ,enemies ,ui_module =None ):

        msgs =[]

        if not enemies :
            return msgs 

        alive_enemies =[e for e in enemies if e .get ("hp",0 )>0 ]
        if not alive_enemies :
            return msgs 

        base_dmg =int ((80 +(self .sukuna_fingers_eaten *30 )+int (self .get_total_str ()*2.2 ))*self .get_sukuna_takeover_modifier ())
        for enemy in alive_enemies :
            half_def =enemy .get ("def",0 )*0.5 
            actual_dmg =calculate_damage (base_dmg ,half_def )
            actual_dmg +=int (enemy .get ("max_hp",0 )*0.025 )
            enemy ["hp"]-=actual_dmg 

            enemy ["bleed_stacks"]=enemy .get ("bleed_stacks",0 )+3 
            msgs .append (f"  Sukuna usa Cleave em {enemy ['name']}: {actual_dmg } dano brutal! (sangrando)")

        karma_loss =random .randint (10 ,50 )
        self .karma .add_karma (-karma_loss )
        self .karma .add_reputacao (-5 )
        msgs .append (f"  Sukuna causa caos colateral! -{karma_loss } karma (matou inocentes).")

        self .sukuna_takeover_turns_left -=1 

        if self .sukuna_takeover_turns_left <=0 :
            self .sukuna_takeover_active =False 
            msgs .append ("  Sukuna devolve o controle a voce. Por enquanto.")

        return msgs 

    def get_sukuna_takeover_modifier (self ):

        if self .sukuna_takeover_active :
            return 1.0 +self .SUKUNA_TAKEOVER_STAT_BONUS 
        return 1.0 

    def reset_combat_sukuna_state (self ):

        self .sukuna_takeover_active =False 
        self .sukuna_takeover_turns_left =0 
        self .sukuna_takeover_triggered_this_battle =False 

    def rest_full (self ):

        self .reset_combat_state ()
        self .hp =self .max_hp 
        self .ce_current =self .max_ce 
        self .stamina =self .max_stamina 

    def rest_partial (self ):
        self .hp =min (self .max_hp ,self .hp +int (self .max_hp *0.3 ))
        self .ce_current =min (self .max_ce ,self .ce_current +int (self .max_ce *0.3 ))
        self .stamina =min (self .max_stamina ,self .stamina +30 )

    def apply_auto_allocate (self ,levels_gained =None ,points =None ,ui_module =None ):
        if points is None :
            points =max (0 ,int (levels_gained or 0 ))*5 
        total_points =points 
        if not self .auto_allocate_build or total_points <=0 :
            return 
        scheme =self .auto_allocate_build 
        if not isinstance (scheme ,dict )or not scheme :
            return 
        weight_total =sum (scheme .values ())
        if weight_total <=0 :
            return 
        total_points =min (total_points ,self .level_system .attribute_points )
        if total_points <=0 :
            return 
        distributed ={k :0 for k in scheme }
        for _ in range (total_points ):
            roll =random .randint (1 ,weight_total )
            cur =0 
            for attr ,w in scheme .items ():
                cur +=w 
                if roll <=cur :
                    self .attributes [attr ]=self .attributes .get (attr ,0 )+1 
                    distributed [attr ]=distributed .get (attr ,0 )+1 
                    break 
        self .level_system .attribute_points =max (0 ,self .level_system .attribute_points -total_points )
        self .recalculate_derived ()
        if ui_module :
            summary =", ".join (f"+{v } {k }"for k ,v in distributed .items ()if v >0 )
            ui_module .tprint (c (f"[Auto-Alocate: {summary }]",Color .DIM ))

    def process_auto_sell (self ,ui_module =None ):
        if not self .auto_sell_list :
            return

        sold_summary ={}
        for item_name in list (self .auto_sell_list ):
            if item_name in self .inventory and self .inventory [item_name ]>0 :
                item =ITEMS_DB .get (item_name ,{})
                if item .get ("price",0 )<=0 :
                    continue 
                qty =self .inventory [item_name ]
                sell_price =max (5 ,item .get ("price",0 )//2 )
                total =sell_price *qty 
                for _ in range (qty ):
                    self .remove_item (item_name )
                self .money +=total 
                sold_summary [item_name ]=(qty ,total )
        if ui_module and sold_summary :
            ui_module .tprint (c ("[Auto-Sell]:",Color .DIM ))
            for name ,(qty ,total )in sold_summary .items ():
                ui_module .tprint (c (f"  Vendido {qty }x {name } por {total } ienes",Color .DIM ))

    def get_stun_resist_chance (self ):
        trait =BIRTH_TRAITS .get (self .birth_trait ,{})
        base =0.0 
        if "stun_resist"in trait .get ("effects",{}):
            base +=(trait ["effects"]["stun_resist"]-1.0 )
        if self .heavenly_restriction :
            base +=0.15 
        try :
            base +=CONFIG .get_stun_resist_bonus ()
        except Exception :
            pass 
        return max (0.0 ,min (0.85 ,base ))

    def display_status (self ,ui_module =None ):

        if not ui_module :
            return 
        ui_module .screen_header (ui_module .ASCII_CHARACTER ,f"STATUS DE {self .name .upper ()}",
        color =ui_module .Color .BRIGHT_MAGENTA )
        print ()

        core_lines =[
        f"Level: {self .level_system .level } | Rank: {self .rank_system .full_rank_name ()}",
        f"Karma: {self .karma .karma } ({self .karma .get_alinhamento ()})",
        f"Local: {self .location }",
        ]
        ui_module .section ("Resumo",core_lines ,color =ui_module .Color .BRIGHT_CYAN )
        print ()

        print (c ("  HP:  ",Color .WHITE )+ui_module .hp_bar (self .hp ,self .max_hp ,length =30 ))
        print (c ("  CE:  ",Color .WHITE )+ui_module .ce_bar (self .ce_current ,self .max_ce ,length =30 ))
        if self .has_technique_evolution ():
            xp_now =self .technique_xp 
            xp_next =self .xp_to_next_technique_level ()
            stage_label =self .get_technique_stage_label ()
            print (c ("  Tecnica: ",Color .WHITE )+c (f"{stage_label } (Lv.{self .technique_level })",
            Color .BRIGHT_MAGENTA ))
            print (c ("  XP Tecnica: ",Color .WHITE )+ui_module .xp_bar (xp_now ,xp_next ,length =30 ))
        print ()

        attr_labels ={
        "forca":"Forca Fisica","ce":"Energia Amaldicoada","controle":"Controle de CE",
        "velocidade":"Velocidade","vigor":"Vigor (HP)","sorte":"Sorte",
        }
        attr_lines =[f"{attr_labels .get (k ,k )}: {v }"for k ,v in self .attributes .items ()]
        if self .level_system .attribute_points >0 :
            attr_lines .append (f">> {self .level_system .attribute_points } pontos disponiveis! <<")
        ui_module .section ("Atributos",attr_lines ,color =ui_module .Color .BRIGHT_CYAN )
        print ()

        effective_lines =[
        f"Forca total: {self .get_total_str ()}",
        f"Defesa total: {self .get_total_def ()}",
        f"Velocidade total: {self .get_total_speed ()}",
        f"Sorte total: {self .get_total_luck ()}",
        f"Controle total: {self .get_total_control ()}",
        f"Esquiva: {int (self .get_dodge_chance ()*100 )}%",
        f"Black Flash: {int (self .get_black_flash_chance ()*100 )}%",
        f"Eficiencia de CE: {self .get_ce_efficiency ():.2f}x",
        ]
        ui_module .section ("Stats Efetivos",effective_lines ,color =ui_module .Color .BRIGHT_GREEN )
        print ()

        tech =INNATE_TECHNIQUES .get (self .innate_technique ,{})
        identity_lines =[
        f"Tecnica Inata: {self .innate_technique }",
        f"Traco de Nascimento: {self .birth_trait }",
        ]
        if self .heavenly_restriction :
            identity_lines .append ("!! RESTRICAO CELESTIAL !!")
        domain_name =self .get_domain_name ()
        if domain_name :
            domain_kind ="Simples (defensivo)"if self .is_simple_domain ()else "Completo (offensivo)"
            identity_lines .append (f"Dominio: {domain_name } ({domain_kind })")
        if self .learned_rct :
            identity_lines .append ("Tecnica Reversa (aprendido)")
        ui_module .section ("Identidade",identity_lines ,color =ui_module .Color .BRIGHT_MAGENTA )
        print ()

        if self .sukuna_fingers_eaten >0 or self .sukuna_fingers_in_inventory >0 or self .sukuna_mastered :
            sukuna_lines =[
            f"Dedos ingeridos: {self .sukuna_fingers_eaten }",
            f"Dedos no inventario: {self .sukuna_fingers_in_inventory }",
            f"Controle do Sukuna: {self .sukuna_control_pct }%",
            ]
            if self .sukuna_mastered :
                sukuna_lines .append ("Status: Sukuna dominado (pode usar Malevolent Shrine)")
            ui_module .section ("Sukuna",sukuna_lines ,color =ui_module .Color .BRIGHT_RED )
            print ()

        equip_lines =[]
        arma =self .equipped .get ("arma")
        equip_lines .append (f"Arma: {arma if arma else '(vazio)'}")
        amuletos =self .equipped .get ("amuletos")or [None ]*5 
        for i ,amul in enumerate (amuletos [:5 ],1 ):
            equip_lines .append (f"Amuleto {i }: {amul if amul else '(vazio)'}")
        equip_lines .append (f"Dinheiro: {self .money } ienes")
        ui_module .section ("Equipamento",equip_lines ,color =ui_module .Color .BRIGHT_CYAN )
        print ()

        stat_lines =[
        f"Maldicoes exorcizadas: {self .kills_total }",
        f"Batalhas vencidas: {self .battles_won }",
        f"Missoes completas: {self .missions_completed }",
        f"Masmorras exploradas: {self .dungeons_explored }",
        f"Civis salvos: {self .karma .civis_salvos }",
        ]
        ui_module .section ("Estatisticas",stat_lines ,color =ui_module .Color .BRIGHT_YELLOW )
        print ()

        ui_module .pause ()

    def to_dict (self ):
        return {
        "name":self .name ,
        "attributes":self .attributes ,
        "innate_technique":self .innate_technique ,
        "birth_trait":self .birth_trait ,
        "heavenly_restriction":self .heavenly_restriction ,
        "hp":self .hp ,
        "max_hp":self .max_hp ,
        "ce_current":self .ce_current ,
        "max_ce":self .max_ce ,
        "stamina":self .stamina ,
        "max_stamina":self .max_stamina ,
        "sukuna_fingers_eaten":self .sukuna_fingers_eaten ,
        "sukuna_control_pct":self .sukuna_control_pct ,
        "sukuna_fingers_in_inventory":self .sukuna_fingers_in_inventory ,
        "inventory":self .inventory ,
        "equipped":self .equipped ,
        "money":self .money ,
        "kills_total":self .kills_total ,
        "battles_won":self .battles_won ,
        "battles_lost":self .battles_lost ,
        "missions_completed":self .missions_completed ,
        "dungeons_explored":self .dungeons_explored ,
        "gojo_met":self .gojo_met ,
"heitor_unlocked":self .heitor_unlocked ,
"urgent_contract":self .urgent_contract ,
"questline_progress":self .questline_progress ,
"questlines_completed":self .questlines_completed ,
        "playtime_turns":self .playtime_turns ,
        "learned_simple_domain":self .learned_simple_domain ,
        "learned_rct":self .learned_rct ,
        "gojo_trained_count":self .gojo_trained_count ,
        "nanami_trained_count":self .nanami_trained_count ,
        "todo_trained_count":self .todo_trained_count ,
        "location":self .location ,
        "completed_stories":list (self .completed_stories ),
        "mentors_used_once":list (self .mentors_used_once ),
        "xp_mult_battles_left":self .xp_mult_battles_left ,
        "dmg_buff_next_battle":self .dmg_buff_next_battle ,
        "mentor_last_used":self .mentor_last_used ,
        "tamed_shikigami":list (self .tamed_shikigami ),
        "sukuna_mastered":self .sukuna_mastered ,
        "technique_xp":self .technique_xp ,
        "technique_level":self .technique_level ,
        "auto_allocate_build":self .auto_allocate_build ,
        "auto_sell_list":list (self .auto_sell_list )if self .auto_sell_list else [],
        "technique_roulette_count":self .technique_roulette_count ,
        "trait_roulette_count":self .trait_roulette_count ,
        "rank_system":self .rank_system .to_dict (),
        "level_system":self .level_system .to_dict (),
        "karma":self .karma .to_dict (),
        }

    def from_dict (self ,data ):

        if not isinstance (data ,dict ):
            data ={}
        self .name =data .get ("name","Despertado")or "Despertado"

        attrs =data .get ("attributes",{})
        if not isinstance (attrs ,dict ):
            attrs ={}
        default_attrs ={
        "forca":10 ,"ce":10 ,"controle":10 ,
        "velocidade":10 ,"vigor":10 ,"sorte":10 ,
        }
        for k ,v in default_attrs .items ():
            if k not in attrs or not isinstance (attrs [k ],(int ,float )):
                attrs [k ]=v 
        self .attributes =attrs 

        self .innate_technique =data .get ("innate_technique","Sem Tecnica")or "Sem Tecnica"
        self .birth_trait =data .get ("birth_trait","Nenhum Traço")or "Nenhum Traço"
        self .heavenly_restriction =bool (data .get ("heavenly_restriction",False ))

        def _int (key ,default ):
            v =data .get (key ,default )
            try :
                return int (v )
            except (TypeError ,ValueError ):
                return default 
        self .hp =_int ("hp",100 )
        self .max_hp =_int ("max_hp",100 )
        self .ce_current =_int ("ce_current",50 )
        self .max_ce =_int ("max_ce",50 )
        self .stamina =_int ("stamina",100 )
        self .max_stamina =_int ("max_stamina",100 )

        self .sukuna_fingers_eaten =_int ("sukuna_fingers_eaten",0 )
        self .sukuna_control_pct =max (0 ,min (100 ,_int ("sukuna_control_pct",0 )))
        self .sukuna_fingers_in_inventory =_int ("sukuna_fingers_in_inventory",0 )

        inv =data .get ("inventory",{})
        if not isinstance (inv ,dict ):
            inv ={}
        clean_inv ={}
        for k ,v in inv .items ():
            try :
                clean_inv [k ]=int (v )
            except (TypeError ,ValueError ):
                clean_inv [k ]=1 
        self .inventory =clean_inv 

        equipped =data .get ("equipped",{})
        if not isinstance (equipped ,dict ):
            equipped ={}
        amuletos =equipped .get ("amuletos")
        if not isinstance (amuletos ,list )or len (amuletos )!=5 :
            amuletos =[None ,None ,None ,None ,None ]
            old_amul =equipped .get ("amuleto")
            if old_amul :
                amuletos [0 ]=old_amul 
        self .equipped ={
        "arma":equipped .get ("arma"),
        "amuletos":amuletos ,
        }

        aab =data .get ("auto_allocate_build",None )
        if isinstance (aab ,str ):
            aab =None
        elif not isinstance (aab ,dict ):
            aab =None
        else :
            clean_aab ={}
            valid_attrs ={"forca","ce","controle","velocidade","vigor","sorte"}
            for k ,v in aab .items ():
                if k in valid_attrs :
                    try :
                        w =int (v )
                        if w >0 :
                            clean_aab [k ]=w
                    except (TypeError ,ValueError ):
                        pass
            aab =clean_aab if clean_aab else None
        self .auto_allocate_build =aab
        asl =data .get ("auto_sell_list",[])
        if not isinstance (asl ,list ):
            asl =[]
        self .auto_sell_list =[str (x )for x in asl ]
        self .technique_roulette_count =_int ("technique_roulette_count",0 )
        self .trait_roulette_count =_int ("trait_roulette_count",0 )

        self .money =_int ("money",200 )
        self .kills_total =_int ("kills_total",0 )
        self .battles_won =_int ("battles_won",0 )
        self .battles_lost =_int ("battles_lost",0 )
        self .missions_completed =_int ("missions_completed",0 )
        self .dungeons_explored =_int ("dungeons_explored",0 )
        self .gojo_met =bool (data .get ("gojo_met",False ))
        self .heitor_unlocked =bool (data .get ("heitor_unlocked",False ))
        self .urgent_contract =data .get ("urgent_contract",None )
        self .questline_progress =data .get ("questline_progress",None )
        self .questlines_completed =data .get ("questlines_completed",[])
        self .playtime_turns =_int ("playtime_turns",0 )
        self .learned_simple_domain =bool (data .get ("learned_simple_domain",False ))
        self .learned_rct =bool (data .get ("learned_rct",False ))
        self .gojo_trained_count =_int ("gojo_trained_count",0 )
        self .nanami_trained_count =_int ("nanami_trained_count",0 )
        self .todo_trained_count =_int ("todo_trained_count",0 )
        self .location =data .get ("location","Escola Jujutsu")or "Escola Jujutsu"

        def _to_set (val ):
            if isinstance (val ,set ):
                return val 
            if isinstance (val ,(list ,tuple )):
                return set (str (x )for x in val )
            return set ()
        self .completed_stories =_to_set (data .get ("completed_stories",[]))
        self .mentors_used_once =_to_set (data .get ("mentors_used_once",[]))

        self .xp_mult_battles_left =_int ("xp_mult_battles_left",0 )
        if self .xp_mult_battles_left <=0 :
            self .level_system .xp_mult =1.0 
        self .dmg_buff_next_battle =float (data .get ("dmg_buff_next_battle",0.0 ))

        mlu =data .get ("mentor_last_used",{})
        if not isinstance (mlu ,dict ):
            mlu ={}
        self .mentor_last_used =mlu 

        ts =data .get ("tamed_shikigami",[])
        if not isinstance (ts ,list ):
            ts =[]
        self .tamed_shikigami =[str (x )for x in ts ]

        self .sukuna_mastered =bool (data .get ("sukuna_mastered",False ))or (self .sukuna_fingers_eaten >0 )

        self .technique_xp =_int ("technique_xp",0 )
        self .technique_level =max (1 ,_int ("technique_level",1 ))

        self .sukuna_takeover_active =False 
        self .sukuna_takeover_turns_left =0 
        self .sukuna_takeover_triggered_this_battle =False 
        self .active_domain =None 
        self .active_domain_used_count =0 
        self .frame_stacks =0 
        self .frame_locks_enemy ={}

        self .rank_system .from_dict (data .get ("rank_system",{}))
        self .level_system .from_dict (data .get ("level_system",{}))
        self .karma .from_dict (data .get ("karma",{}))
        if self .xp_mult_battles_left <=0 :
            self .level_system .xp_mult =1.0
