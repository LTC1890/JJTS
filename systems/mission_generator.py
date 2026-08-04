import os
import sys
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
for _sub in ("data", "systems", "interface"):
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), _sub))

from ui import Color, c

MISSION_LOCATIONS = [
    "Escola Abandonada", "Estacao de Trem Desativada", "Bosque de Bambu",
    "Predio Comercial Vazio", "Tunel do Metro", "Santuario Esquecido",
    "Hospital Desativado", "Complexo Industrial", "Vila Isolada nas Montanhas",
    "Porto Antigo", "Biblioteca Municipal Fechada", "Ponte Abandonada",
    "Templo em Ruinas", "Bairro Evacuado", "Estacionamento Subterraneo",
    "Feira de Rua Deserta", "Casa de Cha Antiga", "Cemiterio nos Arredores",
]

MISSION_CLIENTS = [
    ("Sra. Tanaka", "moradora local"), ("Kenji", "estudante assustado"),
    ("Insp. Mori", "policial da area"), ("Sr. Watanabe", "dono de loja"),
    ("Yui", "funcionaria da prefeitura"), ("Prof. Saito", "diretor de escola"),
    ("Haru", "entregador"), ("Sra. Kobayashi", "enfermeira"),
    ("Renji", "feiticeiro veterano"), ("Anonimo", "informante nervoso"),
    ("Comite da Vila", "conselho local"), ("Aiko", "sacerdotisa de santuario"),
]

TYPE_VERB_PHRASES = {
    "combat": [
        "Exorcismo em {loc}",
        "Eliminar ameaca: {loc}",
        "Patrulha em {loc}",
    ],
    "dungeon": [
        "Investigar {loc}",
        "Explorar e purificar {loc}",
        "Incidente em {loc}",
    ],
    "fetch": [
        "Recuperar itens em {loc}",
        "Itens perdidos: {loc}",
    ],
}

TYPE_DESC_TEMPLATES = {
    "combat": "{client} ({role}) relata avistamentos de maldicoes perto de {loc}. Va la e resolva antes que alguem se machuque.",
    "dungeon": "{client} ({role}) pede para investigar estranhos incidentes em {loc}. Ninguem sabe exatamente o que esta la dentro.",
    "fetch": "{client} ({role}) perdeu itens importantes em {loc} durante um incidente amaldicoado recente.",
}

RANK_DANGER_RANGE = {
    "Grau 4": (1, 5), "Grau 3": (4, 10), "Grau 2": (8, 16),
    "Grau 1": (14, 24), "Grau Especial": (20, 32),
}

RANK_REWARD_BASE = {
    "Grau 4": (80, 90), "Grau 3": (220, 200), "Grau 2": (500, 420),
    "Grau 1": (1100, 900), "Grau Especial": (2600, 2100),
}

BONUS_OBJECTIVES = [
    {"id": "no_damage", "desc": "Vencer sem tomar dano", "bonus_xp_mult": 0.6, "bonus_money_mult": 0.5},
    {"id": "turn_limit", "desc": "Vencer em ate {n} turnos", "bonus_xp_mult": 0.5, "bonus_money_mult": 0.4, "turn_limit": 6},
    {"id": "no_technique", "desc": "Vencer sem usar nenhuma tecnica amaldicoada", "bonus_xp_mult": 0.55, "bonus_money_mult": 0.45},
]

TYPE_SHORT_TAG = {
    "combat": "LUTA", "dungeon": "EXPLORA", "fetch": "BUSCA",
    "boss": "BOSS", "procedural_boss": "BOSS",
}

def _truncate(text, max_len=34):
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."

def format_mission_label(mission):
    mtype = mission.get("type", "combat")
    type_tag = TYPE_SHORT_TAG.get(mtype, "MISSAO")
    rank_label = mission.get("rank", mission.get("boss_rank", "?"))

    priority_tag = None
    if mission.get("questline_id"):
        priority_tag = "SEQ"
    elif mission.get("urgent"):
        priority_tag = f"URGENTE {mission.get('urgent_expires_in', '?')}x"
    elif mission.get("rare"):
        priority_tag = "RARA"
    elif mission.get("bonus_objective"):
        priority_tag = "BONUS"

    prefix = f"[{priority_tag}] " if priority_tag else f"[{type_tag}] "
    name = _truncate(mission["name"], 32)
    return f"{prefix}{name} ({rank_label}) - {mission['xp_reward']}xp/${mission['money_reward']}"

def mission_preview_lines(mission):
    lines = []
    if mission.get("client_name"):
        lines.append(f"Cliente: {mission['client_name']} ({mission.get('client_role', '')})")
    if mission.get("questline_id"):
        lines.append(f"Sequencia: {mission['questline_name']} - parte {mission['questline_stage'] + 1}/{mission['questline_total_stages']}")
    if mission.get("urgent"):
        lines.append(f"URGENTE - expira em {mission.get('urgent_expires_in', '?')} visita(s) ao quadro se nao aceita agora")
    if mission.get("bonus_objective"):
        lines.append(f"Objetivo bonus: {mission['bonus_objective']['desc']}")
    return lines

def generate_procedural_mission(player, rank=None, force_bonus=False, force_urgent=False):
    if rank is None:
        rank = player.rank_system.rank

    mtype = random.choices(["combat", "dungeon", "fetch"], weights=[0.5, 0.35, 0.15])[0]
    location = random.choice(MISSION_LOCATIONS)
    client_name, client_role = random.choice(MISSION_CLIENTS)

    name = random.choice(TYPE_VERB_PHRASES[mtype]).format(loc=location)
    desc = TYPE_DESC_TEMPLATES[mtype].format(client=client_name, role=client_role, loc=location)

    base_xp, base_money = RANK_REWARD_BASE.get(rank, (100, 100))
    variance = random.uniform(0.85, 1.25)
    xp_reward = int(base_xp * variance)
    money_reward = int(base_money * variance)

    mission = {
        "name": name,
        "type": mtype,
        "rank": rank,
        "desc": desc,
        "xp_reward": xp_reward,
        "money_reward": money_reward,
        "client_name": client_name,
        "client_role": client_role,
        "procedural": True,
    }

    if mtype == "combat":
        mission["num_enemies"] = random.choice([1, 1, 2, 2, 3])
        if random.random() < 0.3:
            mission["allow_allies"] = True
    elif mtype == "dungeon":
        dmin, dmax = RANK_DANGER_RANGE.get(rank, (1, 10))
        mission["min_danger"] = dmin
        mission["max_danger"] = dmax
    elif mtype == "fetch":
        mission["items_required"] = random.randint(2, 4)

    if random.random() < 0.15:
        mission["karma_bonus"] = random.randint(2, 6)

    if mtype in ("combat",) and (force_bonus or random.random() < 0.35):
        bonus = dict(random.choice(BONUS_OBJECTIVES))
        mission["bonus_objective"] = bonus

    if force_urgent or random.random() < 0.10:
        mission["urgent"] = True
        mission["urgent_expires_in"] = random.randint(2, 4)
        mission["xp_reward"] = int(mission["xp_reward"] * 1.8)
        mission["money_reward"] = int(mission["money_reward"] * 1.8)

    return mission

def check_bonus_objective(mission, player, combat_turns, ui_module):
    bonus = mission.get("bonus_objective")
    if not bonus:
        return 0, 0

    met = False
    if bonus["id"] == "no_damage":
        met = player.dmg_taken_this_combat <= 0
    elif bonus["id"] == "turn_limit":
        met = combat_turns is not None and combat_turns <= bonus.get("turn_limit", 6)
    elif bonus["id"] == "no_technique":
        met = combat_turns is not None and len(getattr(player, "_last_combat_techniques_used", [])) == 0

    if not met:
        ui_module.tprint(c(f"\n(Objetivo bonus nao cumprido: {bonus['desc']})", Color.DIM))
        return 0, 0

    bonus_xp = int(mission["xp_reward"] * bonus.get("bonus_xp_mult", 0.5))
    bonus_money = int(mission["money_reward"] * bonus.get("bonus_money_mult", 0.5))
    ui_module.tprint(c(f"\n!! OBJETIVO BONUS CUMPRIDO: {bonus['desc']} !!", Color.BRIGHT_YELLOW + Color.BOLD))
    ui_module.tprint(c(f"+{bonus_xp} XP bonus, +{bonus_money} ienes bonus", Color.BRIGHT_YELLOW))
    return bonus_xp, bonus_money

def tick_urgent_contract(player, ui_module=None):
    contract = getattr(player, "urgent_contract", None)
    if not contract:
        return
    contract["urgent_expires_in"] -= 1
    if contract["urgent_expires_in"] <= 0:
        if ui_module:
            ui_module.tprint(c(f"\nO contrato urgente '{contract['name']}' expirou.", Color.DIM))
        player.urgent_contract = None

QUESTLINES = {
    "colecionador_de_dedos": {
        "name": "O Colecionador de Dedos",
        "min_rank_idx": 1,
        "stages": [
            {
                "name": "Rastros do Colecionador",
                "type": "dungeon", "min_danger": 6, "max_danger": 12,
                "xp_reward": 350, "money_reward": 280,
                "desc": "Rumores falam de um feiticeiro renegado colecionando Dedos de Sukuna por meios brutais. Investigue os rastros dele.",
                "story_intro": "Um informante nervoso te entrega um mapa rasurado. 'Ele estava aqui. Tome cuidado, essa pessoa nao e normal.'",
                "story_outro": "Voce encontra um acampamento abandonado as pressas. Uma pista aponta para o proximo esconderijo.",
            },
            {
                "name": "O Covil do Colecionador",
                "type": "combat", "num_enemies": 2, "rank": "Grau 2",
                "xp_reward": 600, "money_reward": 480, "allow_allies": True,
                "desc": "Voce encontrou o covil. Maldicoes capturadas guardam o local.",
                "story_intro": "O cheiro de CE amaldicoado e sufocante aqui dentro. Algo errado aconteceu neste lugar.",
                "story_outro": "Voce derrota os guardioes. No fundo do covil, uma porta reforcada leva mais fundo.",
            },
            {
                "name": "Confronto Final: O Colecionador",
                "type": "procedural_boss", "boss_rank": "Grau 1",
                "xp_reward": 1200, "money_reward": 900,
                "desc": "O Colecionador em pessoa te espera. Termine essa historia.",
                "story_intro": "'Mais um feiticeiro querendo brincar de heroi. Vou adicionar seus dedos a colecao tambem.'",
                "story_outro": "O Colecionador cai. Voce encontra uma pequena caixa de metal entre os pertences dele.",
            },
        ],
        "final_reward_item": "Dedo de Sukuna",
        "final_reward_karma": 15,
    },
    "praga_da_vila": {
        "name": "A Praga da Vila Isolada",
        "min_rank_idx": 0,
        "stages": [
            {
                "name": "Chamado de Socorro",
                "type": "combat", "num_enemies": 1, "rank": "Grau 4",
                "xp_reward": 150, "money_reward": 120,
                "desc": "Uma vila isolada nas montanhas pede ajuda urgente contra maldicoes cada vez mais frequentes.",
                "story_intro": "O Comite da Vila te recebe com desconfianca. 'Feiticeiros nunca vieram tao rapido antes. Algo esta muito errado.'",
                "story_outro": "Voce afasta a primeira onda, mas sente que a origem do problema esta mais fundo na montanha.",
            },
            {
                "name": "A Origem da Praga",
                "type": "dungeon", "min_danger": 4, "max_danger": 9,
                "xp_reward": 300, "money_reward": 250,
                "desc": "Siga o rastro de CE amaldicoado ate a origem da praga que assola a vila.",
                "story_intro": "O caminho na montanha esta coberto por uma neblina anormal, densa de energia amaldicoada.",
                "story_outro": "No topo, voce encontra um santuario profanado - a fonte de tudo isso.",
            },
            {
                "name": "Selar o Santuario",
                "type": "procedural_boss", "boss_rank": "Grau 3",
                "xp_reward": 500, "money_reward": 400,
                "desc": "Uma maldicao nascida da profanacao do santuario guarda a origem da praga.",
                "story_intro": "A maldicao se ergue da terra profanada, disforme e furiosa.",
                "story_outro": "Com a maldicao selada, a neblina se dissipa. A vila esta salva.",
            },
        ],
        "final_reward_item": "Cristal de CE",
        "final_reward_karma": 8,
    },
}

def get_active_questline_mission(player):
    progress = getattr(player, "questline_progress", None)
    if not progress:
        return None
    qid = progress.get("id")
    stage = progress.get("stage", 0)
    questline = QUESTLINES.get(qid)
    if not questline or stage >= len(questline["stages"]):
        return None
    stage_data = dict(questline["stages"][stage])
    stage_data["questline_id"] = qid
    stage_data["questline_stage"] = stage
    stage_data["questline_name"] = questline["name"]
    stage_data["questline_total_stages"] = len(questline["stages"])
    return stage_data

def maybe_offer_new_questline(player):
    if getattr(player, "questline_progress", None):
        return None
    completed = getattr(player, "questlines_completed", [])
    rank_idx = ["Grau 4", "Grau 3", "Grau 2", "Grau 1", "Grau Especial"].index(player.rank_system.rank) \
        if player.rank_system.rank in ["Grau 4", "Grau 3", "Grau 2", "Grau 1", "Grau Especial"] else 0
    candidates = [qid for qid, q in QUESTLINES.items()
                  if qid not in completed and q["min_rank_idx"] <= rank_idx]
    if not candidates:
        return None
    if random.random() < 0.25:
        return random.choice(candidates)
    return None
