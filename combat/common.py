
import random 
import sys 
import os 
import time 

_COMBAT_DIR =os .path .dirname (os .path .abspath (__file__ ))
_PROJECT_ROOT =os .path .dirname (_COMBAT_DIR )
sys .path .insert (0 ,_COMBAT_DIR )
sys .path .insert (0 ,_PROJECT_ROOT )
for _sub in ("data","systems","interface"):
    sys .path .insert (0 ,os .path .join (_PROJECT_ROOT ,_sub ))

import ui
from ui import Color ,c
import keyboard_input 
import allies as allies_mod
from techniques import (DOMAINS ,get_rct_info ,BIRTH_TRAITS ,
get_available_extensions )
from items import ITEMS_DB ,roll_enemy_drop
from shikigami import (shikigami_take_turn ,tick_shikigami ,
SHIKIGAMI_DB ,create_active_shikigami )
from config import CONFIG
from player import calculate_damage
import mahoraga as mahoraga_mod
import enemies as enemies_mod

BLACK_FLASH_DMG_MULT =2.5 
BLACK_FLASH_CE_GAIN_PCT =0.20 
ENEMY_ABILITY_CHANCE =0.40 
DODGE_CE_COST =15 
DODGE_BASE_BONUS =30 
REINFORCE_CE_COST =20 
REINFORCE_DEF_BONUS =40 
BLEED_DMG_PER_STACK =5 
BURN_DMG_PER_STACK =7 
POISON_DMG_PER_STACK =4 
DEFENDED_DMG_REDUCTION =0.40 

BOSS_REFERENCE_LEVEL ={
"Grau 4":5 ,"Grau 3":15 ,"Grau 2":30 ,"Grau 1":55 ,"Grau Especial":85 ,
}
BOSS_LEVEL_SCALE_PER_LEVEL =0.035 
BOSS_LEVEL_SCALE_CAP =5.0 

