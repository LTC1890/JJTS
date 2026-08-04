from .common import *
from .core import CombatCore
from .player_actions import PlayerActionsMixin
from .enemy_ai import EnemyAIMixin, ally_get_dodge
from .rewards import RewardsMixin

class Combat (CombatCore ,PlayerActionsMixin ,EnemyAIMixin ,RewardsMixin ):
    pass
