
import random

from ui import Color, c

ADAPT_HIT_THRESHOLDS = [2, 4, 7, 11, 16]
ADAPT_RESIST_PER_STEP = 0.16
ADAPT_RESIST_CAP = 0.92

GENERIC_RESIST_PER_HIT = 0.006
GENERIC_RESIST_CAP = 0.25

STOLEN_ADAPT_CE_COST = 700
STOLEN_ADAPT_CYCLE_TURNS = 2

def _move_key(move_name):

    if not move_name:
        return "golpe_desconhecido"
    return move_name.strip().lower()

def init_adaptation_state(target):

    target.setdefault("_adapt_move_counts", {})
    target.setdefault("_adapt_move_resist", {})
    target.setdefault("_adapt_generic_resist", 0.0)
    target.setdefault("_adapt_log", [])
    return target

def register_hit(target, move_name, ui_module=None, silent=False):

    if not target.get("adaptive"):
        return False

    init_adaptation_state(target)
    key = _move_key(move_name)

    counts = target["_adapt_move_counts"]
    counts[key] = counts.get(key, 0) + target.get("adapt_speed_mult", 1)
    hits = counts[key]

    target["_adapt_generic_resist"] = min(
        GENERIC_RESIST_CAP,
        target["_adapt_generic_resist"] + GENERIC_RESIST_PER_HIT,
    )

    step = 0
    for t in ADAPT_HIT_THRESHOLDS:
        if hits >= t:
            step += 1

    resist_map = target["_adapt_move_resist"]
    prev_step = resist_map.get(key, {}).get("step", 0)
    if step <= prev_step:
        return False

    new_resist = min(ADAPT_RESIST_CAP, step * ADAPT_RESIST_PER_STEP)
    resist_map[key] = {"step": step, "resist": new_resist, "display_name": move_name}

    target["_adapt_log"].append(move_name)

    if not silent and ui_module:
        if new_resist >= ADAPT_RESIST_CAP:
            ui_module.tprint(c(
                f"\n!! A RODA DE MAHORAGA GIRA - ADAPTACAO COMPLETA !!\n"
                f"{target.get('name', 'O alvo')} agora ignora quase totalmente '{move_name}'. "
                f"Mude de estrategia!",
                Color.BRIGHT_MAGENTA + Color.BOLD,
            ))
        else:
            ui_module.tprint(c(
                f"\nA roda de Mahoraga gira... adaptacao a '{move_name}' "
                f"aumenta para {int(new_resist * 100)}%!",
                Color.BRIGHT_MAGENTA,
            ))
        ui_module.pause()

    return True

def get_damage_reduction(target, move_name):

    if not target.get("adaptive"):
        return 0.0
    init_adaptation_state(target)
    key = _move_key(move_name)
    specific = target["_adapt_move_resist"].get(key, {}).get("resist", 0.0)
    generic = target.get("_adapt_generic_resist", 0.0)

    combined = 1.0 - (1.0 - specific) * (1.0 - generic)
    return min(0.97, combined)

def apply_adaptation(target, move_name, raw_damage, ui_module=None, silent=False):

    reduction = get_damage_reduction(target, move_name)
    register_hit(target, move_name, ui_module=ui_module, silent=silent)
    if reduction <= 0:
        return raw_damage
    return max(1, int(raw_damage * (1.0 - reduction)))

def most_adapted_moves(target, limit=3):

    if not target.get("adaptive"):
        return []
    resist_map = target.get("_adapt_move_resist", {})
    ranked = sorted(resist_map.values(), key=lambda v: v["resist"], reverse=True)
    return [(r["display_name"], r["resist"]) for r in ranked[:limit] if r["resist"] > 0]

def reset_adaptation(target):

    target["_adapt_move_counts"] = {}
    target["_adapt_move_resist"] = {}
    target["_adapt_generic_resist"] = 0.0
    target["_adapt_log"] = []

STOLEN_ADAPT_RESIST_CAP = 0.70
STOLEN_ADAPT_RESIST_PER_STEP = 0.14

def can_use_stolen_adaptation(player):

    has_sukuna_body = bool(getattr(player, "sukuna_mastered", False))
    has_ten_shadows = getattr(player, "innate_technique", None) == "Dez Sombras"
    return has_sukuna_body and has_ten_shadows

def activate_stolen_adaptation(player, ui_module=None):

    if not can_use_stolen_adaptation(player):
        if ui_module:
            ui_module.tprint(c(
                "\nVoce precisa ter Sukuna dominado no corpo (dedo ingerido) "
                "E a tecnica inata Dez Sombras para roubar a Adaptacao de Mahoraga.",
                Color.RED,
            ))
            ui_module.pause()
        return False

    if player.ce_current < STOLEN_ADAPT_CE_COST:
        if ui_module:
            ui_module.tprint(c(
                f"\nCE insuficiente! A Adaptacao Roubada exige {STOLEN_ADAPT_CE_COST} CE "
                "para o primeiro ciclo.",
                Color.RED,
            ))
            ui_module.pause()
        return False

    player.ce_current -= STOLEN_ADAPT_CE_COST
    player._stolen_adaptation_active = True
    player._stolen_adaptation_turns_left = STOLEN_ADAPT_CYCLE_TURNS
    player._stolen_adapt_move_counts = {}
    player._stolen_adapt_move_resist = {}

    if ui_module:
        ui_module.tprint(c(
            "\n!! VOCE ROUBA A ADAPTACAO DE MAHORAGA !!",
            Color.BRIGHT_RED + Color.BOLD + Color.BLINK,
        ))
        ui_module.tprint(c(
            "Sukuna ri dentro de voce. 'Interessante... usando a roda contra os outros.'",
            Color.BRIGHT_RED,
        ))
        ui_module.tprint(c(
            f"-{STOLEN_ADAPT_CE_COST } CE | Ativa por ciclos de {STOLEN_ADAPT_CYCLE_TURNS } turnos.",
            Color.DIM,
        ))
        ui_module.pause()
    return True

def tick_stolen_adaptation(player, ui_module=None):

    if not getattr(player, "_stolen_adaptation_active", False):
        return

    player._stolen_adaptation_turns_left -= 1
    if player._stolen_adaptation_turns_left > 0:
        return

    if player.ce_current >= STOLEN_ADAPT_CE_COST:
        player.ce_current -= STOLEN_ADAPT_CE_COST
        player._stolen_adaptation_turns_left = STOLEN_ADAPT_CYCLE_TURNS
        if ui_module:
            ui_module.tprint(c(
                f"[Adaptacao Roubada continua: -{STOLEN_ADAPT_CE_COST} CE]",
                Color.DIM,
            ))
    else:
        player._stolen_adaptation_active = False
        player._stolen_adaptation_turns_left = 0
        player._stolen_adapt_move_counts = {}
        player._stolen_adapt_move_resist = {}
        if ui_module:
            ui_module.tprint(c(
                "\nA Adaptacao Roubada se dissipa - CE insuficiente para manter a roda girando.",
                Color.YELLOW,
            ))
            ui_module.tprint(c(
                "Toda a resistencia acumulada contra os golpes do inimigo se perde.",
                Color.DIM,
            ))
            ui_module.pause()

def register_hit_on_player(player, move_name, ui_module=None):

    if not getattr(player, "_stolen_adaptation_active", False):
        return False

    if not hasattr(player, "_stolen_adapt_move_counts"):
        player._stolen_adapt_move_counts = {}
        player._stolen_adapt_move_resist = {}

    key = _move_key(move_name)
    counts = player._stolen_adapt_move_counts
    counts[key] = counts.get(key, 0) + 1
    hits = counts[key]

    step = 0
    for t in ADAPT_HIT_THRESHOLDS:
        if hits >= t:
            step += 1

    resist_map = player._stolen_adapt_move_resist
    prev_step = resist_map.get(key, {}).get("step", 0)
    if step <= prev_step:
        return False

    new_resist = min(STOLEN_ADAPT_RESIST_CAP, step * STOLEN_ADAPT_RESIST_PER_STEP)
    resist_map[key] = {"step": step, "resist": new_resist, "display_name": move_name}

    if ui_module:
        ui_module.tprint(c(
            f"\n[Adaptacao Roubada gira contra '{move_name}': "
            f"+{int(new_resist * 100)}% resistencia!]",
            Color.BRIGHT_MAGENTA,
        ))
        ui_module.pause()
    return True

def get_player_damage_reduction(player, move_name):

    if not getattr(player, "_stolen_adaptation_active", False):
        return 0.0
    if not hasattr(player, "_stolen_adapt_move_resist"):
        return 0.0
    key = _move_key(move_name)
    return player._stolen_adapt_move_resist.get(key, {}).get("resist", 0.0)

def reset_stolen_adaptation(player):

    player._stolen_adaptation_active = False
    player._stolen_adaptation_turns_left = 0
    player._stolen_adapt_move_counts = {}
    player._stolen_adapt_move_resist = {}
