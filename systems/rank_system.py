
from enemies import RANK_INFO ,RANK_ORDER 

class RankSystem :

    def __init__ (self ):
        self .rank ="Grau 4"
        self .sub_rank =None 
        self .total_xp =0 
        self .xp_in_rank =0 

    def get_rank_info (self ):
        return RANK_INFO .get (self .rank ,{})

    def get_xp_to_next_rank (self ):
        return self .get_rank_info ().get ("xp_to_next_rank",999999 )

    def add_xp (self ,amount ):

        self .total_xp +=amount 
        self .xp_in_rank +=amount 
        leveled_up =False 
        while self .xp_in_rank >=self .get_xp_to_next_rank ()and self .rank !="Grau Especial":
            self .xp_in_rank -=self .get_xp_to_next_rank ()
            self .promote ()
            leveled_up =True 
        return leveled_up ,self .rank 

    def promote (self ):

        idx =RANK_ORDER .index (self .rank )
        if idx <len (RANK_ORDER )-1 :
            self .rank =RANK_ORDER [idx +1 ]
            self .sub_rank =None 

            if self .rank =="Grau 2":
                self .sub_rank ="Semi-1"

    def demote (self ):

        idx =RANK_ORDER .index (self .rank )
        if idx >0 :
            self .rank =RANK_ORDER [idx -1 ]
            self .sub_rank =None 

    def can_promote_sub_rank (self ):

        return self .rank =="Grau 2"and self .sub_rank =="Semi-1"

    def promote_sub_rank (self ):
        if self .can_promote_sub_rank ():
            self .sub_rank ="Semi-2"
            return True 
        return False 

    def full_rank_name (self ):
        if self .rank =="Grau 2"and self .sub_rank :
            return f"Grau 2 ({self .sub_rank })"
        return self .rank 

    def to_dict (self ):
        return {
        "rank":self .rank ,
        "sub_rank":self .sub_rank ,
        "total_xp":self .total_xp ,
        "xp_in_rank":self .xp_in_rank ,
        }

    def from_dict (self ,data ):
        self .rank =data .get ("rank","Grau 4")
        self .sub_rank =data .get ("sub_rank")
        self .total_xp =data .get ("total_xp",0 )
        self .xp_in_rank =data .get ("xp_in_rank",0 )

class LevelSystem :

    def __init__ (self ):
        self .level =1 
        self .xp =0 
        self .attribute_points =0 
        self .xp_mult =1.0 

    def xp_to_next_level (self ):

        return int (100 *(self .level **1.5 ))

    def add_xp (self ,amount ):

        amount =int (amount *self .xp_mult )
        self .xp +=amount 
        levels_gained =0 
        while self .xp >=self .xp_to_next_level ():
            self .xp -=self .xp_to_next_level ()
            self .level +=1 
            self .attribute_points +=5 
            levels_gained +=1 
        return levels_gained >0 ,levels_gained 

    def spend_point (self ,attr_name ,player ):

        if self .attribute_points <=0 :
            return False 
        if attr_name not in player .attributes :
            return False 
        player .attributes [attr_name ]+=1 
        self .attribute_points -=1 

        player .recalculate_derived ()
        return True 

    def to_dict (self ):
        return {
        "level":self .level ,
        "xp":self .xp ,
        "attribute_points":self .attribute_points ,
        "xp_mult":self .xp_mult ,
        }

    def from_dict (self ,data ):
        self .level =data .get ("level",1 )
        self .xp =data .get ("xp",0 )
        self .attribute_points =data .get ("attribute_points",0 )
        self .xp_mult =data .get ("xp_mult",1.0 )
