
class KarmaSystem :

    ALINHAMENTOS =[
    (-100 ,-50 ,"Renegado das Maldicoes"),
    (-49 ,-20 ,"Feiticeiro Suspeito"),
    (-19 ,19 ,"Feiticeiro Neutro"),
    (20 ,49 ,"Feiticeiro Honrado"),
    (50 ,100 ,"Salvador da Humanidade"),
    ]

    def __init__ (self ):
        self .karma =0 
        self .reputacao =0 
        self .kill_count_curse =0 
        self .kill_count_human =0 
        self .civis_salvos =0 
        self .civis_ignorados =0 
        self .gojo_relation =0 
        self .sukuna_relation =0 
        self .renegade_quests_done =0 

    def add_karma (self ,amount ):

        self .karma =max (-100 ,min (100 ,self .karma +amount ))

    def add_reputacao (self ,amount ):
        self .reputacao =max (-100 ,min (100 ,self .reputacao +amount ))

    def on_curse_kill (self ,curse_rank ):

        bonus ={"Grau 4":1 ,"Grau 3":2 ,"Grau 2":4 ,
        "Grau 1":7 ,"Grau Especial":15 }.get (curse_rank ,1 )
        self .add_karma (bonus )
        self .add_reputacao (bonus )
        self .kill_count_curse +=1 

    def on_human_kill (self ):

        self .add_karma (-15 )
        self .add_reputacao (-10 )
        self .kill_count_human +=1 

    def on_civil_salvo (self ):
        self .add_karma (3 )
        self .add_reputacao (2 )
        self .civis_salvos +=1 

    def on_civil_ignorado (self ):
        self .add_karma (-2 )
        self .add_reputacao (-1 )
        self .civis_ignorados +=1 

    def on_renegade_quest (self ):
        self .add_karma (-5 )
        self .renegade_quests_done +=1 

        self .sukuna_relation =min (100 ,self .sukuna_relation +3 )

    def on_train_with_gojo (self ):
        self .gojo_relation =min (100 ,self .gojo_relation +5 )

    def on_ally_betray (self ):
        self .add_karma (-25 )
        self .add_reputacao (-20 )
        self .gojo_relation =max (-100 ,self .gojo_relation -20 )

    def get_alinhamento (self ):
        for low ,high ,label in self .ALINHAMENTOS :
            if low <=self .karma <=high :
                return label 
        return "Feiticeiro Neutro"

    def is_renegado (self ):
        return self .karma <-30 

    def is_heroi (self ):
        return self .karma >50 

    def can_meet_gojo (self ):

        return self .karma >-50 

    def gojo_likes_player (self ):
        return self .gojo_relation >20 and self .karma >0 

    def can_ally_with_curse (self ):

        return self .karma <-50 

    def sukuna_offers_pact (self ):

        return self .karma <-30 and self .sukuna_relation >20 

    def to_dict (self ):
        return {
        "karma":self .karma ,
        "reputacao":self .reputacao ,
        "kill_count_curse":self .kill_count_curse ,
        "kill_count_human":self .kill_count_human ,
        "civis_salvos":self .civis_salvos ,
        "civis_ignorados":self .civis_ignorados ,
        "gojo_relation":self .gojo_relation ,
        "sukuna_relation":self .sukuna_relation ,
        "renegade_quests_done":self .renegade_quests_done ,
        }

    def from_dict (self ,data ):
        self .karma =data .get ("karma",0 )
        self .reputacao =data .get ("reputacao",0 )
        self .kill_count_curse =data .get ("kill_count_curse",0 )
        self .kill_count_human =data .get ("kill_count_human",0 )
        self .civis_salvos =data .get ("civis_salvos",0 )
        self .civis_ignorados =data .get ("civis_ignorados",0 )
        self .gojo_relation =data .get ("gojo_relation",0 )
        self .sukuna_relation =data .get ("sukuna_relation",0 )
        self .renegade_quests_done =data .get ("renegade_quests_done",0 )
