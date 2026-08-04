
import os
import sys
import json
import time
import shutil
import hashlib
import subprocess
import urllib.request

REPO_OWNER = "LTC1890"
REPO_NAME = "JJTS"
BRANCH = os.environ.get("UPDATER_BRANCH", "main")
BASE_URL = os.environ.get(
    "UPDATER_BASE_URL",
    f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}",
)
TIMEOUT = 15
UA = "JJTS-Updater/1.0"

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = os.path.join(GAME_DIR, "_update_tmp")

PROTECTED_SEGMENTS = ("saved games", "__pycache__", "_update_tmp", ".git")
PROTECTED_FILES = ("jjts_config.json", ".game_version")

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
RED = "\033[31m"
WHITE = "\033[37m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_WHITE = "\033[97m"

def _use_color():
    if not sys.stdout.isatty():
        return False
    if os.name == "nt":
        try:
            os.system("")
        except Exception:
            pass
    return True

_COLOR = _use_color()
_TTY = sys.stdout.isatty()
_INNER = 74

def _c(text, code):
    return f"{code}{text}{RESET}" if _COLOR else text

def _box_width():
    try:
        w = shutil.get_terminal_size((80, 24)).columns
    except Exception:
        w = 80
    return max(44, min(74, w - 2))

def _clear():
    if _TTY:
        os.system("cls" if os.name == "nt" else "clear")

def _url(path):
    return BASE_URL.rstrip("/") + "/" + path

def _fetch(path, timeout=TIMEOUT):
    req = urllib.request.Request(_url(path), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()

def _fetch_json(path):
    try:
        return json.loads(_fetch(path).decode("utf-8"))
    except Exception:
        return None

def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def _parse_version(s):
    parts = []
    for p in str(s).split("."):
        digits = ""
        for ch in p:
            if ch.isdigit():
                digits += ch
            else:
                break
        parts.append(int(digits) if digits else 0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])

def _fmt_version(v):
    return ".".join(str(p) for p in v)

def _local_version():
    path = os.path.join(GAME_DIR, "version.json")
    try:
        with open(path, encoding="utf-8") as f:
            return _parse_version(json.load(f).get("version", "0.0.0"))
    except Exception:
        return (0, 0, 0)

def _local_version_str():
    path = os.path.join(GAME_DIR, "version.json")
    try:
        with open(path, encoding="utf-8") as f:
            return str(json.load(f).get("version", "0.0.0"))
    except Exception:
        return "0.0.0"

def _local_manifest_sha():
    path = os.path.join(GAME_DIR, "manifest.json")
    try:
        return _sha256_file(path)
    except Exception:
        return None

def _auto_update_enabled():
    try:
        sys.path.insert(0, GAME_DIR)
        from config import CONFIG

        return bool(getattr(CONFIG, "auto_update", True))
    except Exception:
        return True

def _is_protected(path):
    parts = path.replace("\\", "/").split("/")
    if any(p in PROTECTED_SEGMENTS for p in parts):
        return True
    if path.replace("\\", "/") in PROTECTED_FILES:
        return True
    return False

def _needs_update(item):
    rel = item["path"].replace("/", os.sep)
    local = os.path.join(GAME_DIR, rel)
    if not os.path.exists(local):
        return True
    try:
        return _sha256_file(local) != item["sha256"]
    except Exception:
        return True

def _cleanup_tmp():
    shutil.rmtree(TMP_DIR, ignore_errors=True)

_STATUS_ROWS = 3

def _bar(pct):
    pct = max(0.0, min(1.0, pct))
    avail = _INNER - 12
    n = int(avail * pct)
    return "[" + "#" * n + "-" * (avail - n) + "] {:3.0f}%".format(pct * 100)

def _status_print(file_text, bar_text, extra_text=""):
    raw = [
        file_text.ljust(_INNER),
        bar_text.ljust(_INNER),
        (extra_text or "").ljust(_INNER),
    ]
    rows = [_c(raw[0], WHITE), _c(raw[1], GREEN), _c(raw[2], DIM)]
    if _TTY:
        sys.stdout.write("\033[{}A".format(_STATUS_ROWS))
        sys.stdout.write("\n".join(rows))
        sys.stdout.flush()
    else:
        print("> " + raw[0].strip())
        print("> " + raw[1].strip())
        if raw[2].strip():
            print("> " + raw[2].strip())

def _show_screen(local_str, new_str, changelog, content_only=False):
    global _INNER
    _INNER = _box_width()
    _clear()
    line = "=" * _INNER
    print(_c("+" + line + "+", CYAN))
    print(_c("|" + " " * _INNER + "|", CYAN))
    print(_c("|" + _c("JJTS UPDATER", BRIGHT_CYAN + BOLD).center(_INNER + len(RESET)) + "|", CYAN))
    print(_c("|" + " " * _INNER + "|", CYAN))
    if content_only:
        msg = _c(f"Novo conteudo disponivel (v{new_str})", BRIGHT_YELLOW + BOLD)
    else:
        msg = _c(f"v{local_str}  ->  v{new_str}", BRIGHT_YELLOW + BOLD)
    print(_c("|" + msg.center(_INNER + len(RESET)) + "|", CYAN))
    if changelog:
        for raw_line in changelog.splitlines()[:4]:
            text = raw_line[: _INNER - 4]
            print(_c("|" + ("  " + text).ljust(_INNER) + "|", DIM))
    print(_c("|" + " " * _INNER + "|", CYAN))
    _status_print("Preparando download...", _bar(0.0), "")
    print(_c("|" + " " * _INNER + "|", CYAN))
    print(_c("|" + _c("Nao feche esta janela", DIM).center(_INNER + len(RESET)) + "|", CYAN))
    print(_c("+" + line + "+", CYAN))

def _download_all(items):
    total = sum(i["size"] for i in items)
    done = 0
    staged = []
    for idx, item in enumerate(items, 1):
        rel = item["path"].replace("/", os.sep)
        dest = os.path.join(TMP_DIR, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        req = urllib.request.Request(_url(item["path"]), headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp, open(dest, "wb") as f:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                f.write(chunk)
                done += len(chunk)
                pct = done / total if total else 1.0
                _status_print(
                    "Baixando: " + item["path"],
                    _bar(pct),
                    "arquivo {} de {}".format(idx, len(items)),
                )
        if _sha256_file(dest) != item["sha256"]:
            raise IOError("Hash invalido: " + item["path"])
        staged.append((item, dest))
    return staged

def _apply(staged):
    for item, src in staged:
        rel = item["path"].replace("/", os.sep)
        dest = os.path.join(GAME_DIR, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        os.replace(src, dest)

def _write_manifest(data):
    path = os.path.join(GAME_DIR, "manifest.json")
    with open(path, "wb") as f:
        f.write(data)

def _relaunch():
    main_py = os.path.join(GAME_DIR, "main.py")
    try:
        subprocess.Popen([sys.executable, main_py], cwd=GAME_DIR)
        return True
    except Exception:
        return False

def check_and_update(force=False, silent=True):

    if not (force or _auto_update_enabled()):
        return False
    try:
        new_info = _fetch_json("version.json")
        if not new_info:
            if not silent:
                print(_c("Nao foi possivel verificar atualizacoes (sem conexao).", YELLOW))
            return False
        new_str = str(new_info.get("version", "0.0.0"))
        new_ver = _parse_version(new_str)
        local = _local_version()
        content_only = new_ver <= local

        manifest_bytes = _fetch("manifest.json")
        if not manifest_bytes:
            return False
        try:
            manifest = json.loads(manifest_bytes.decode("utf-8"))
        except Exception:
            return False
        remote_manifest_sha = hashlib.sha256(manifest_bytes).hexdigest()
        manifest_changed = _local_manifest_sha() != remote_manifest_sha

        items = [i for i in manifest.get("files", []) if not _is_protected(i["path"])]
        changed = [i for i in items if _needs_update(i)]
        if not changed and not manifest_changed:
            if not silent:
                print(_c(f"Voce esta na versao mais recente (v{_local_version_str()}).", BRIGHT_GREEN))
            return False

        _show_screen(_local_version_str(), new_str, str(new_info.get("changelog", "")), content_only)
        _cleanup_tmp()
        os.makedirs(TMP_DIR, exist_ok=True)
        staged = _download_all(changed)
        _status_print("Aplicando atualizacao...", _bar(1.0), "")
        _apply(staged)
        _write_manifest(manifest_bytes)
        _cleanup_tmp()
        if content_only:
            _status_print(
                _c("Conteudo atualizado com sucesso!", BRIGHT_GREEN + BOLD),
                _bar(1.0),
                _c("Reiniciando o jogo...", BRIGHT_CYAN),
            )
        else:
            _status_print(
                _c(f"Atualizado para v{new_str}!", BRIGHT_GREEN + BOLD),
                _bar(1.0),
                _c("Reiniciando o jogo...", BRIGHT_CYAN),
            )
        time.sleep(1.2)
        if os.environ.get("UPDATER_NO_RELAUNCH") == "1":
            return True
        if _relaunch():
            return True
        print(_c("\nReinicie o jogo para aplicar todas as mudancas.", DIM))
        return False
    except Exception:
        _cleanup_tmp()
        return False

if __name__ == "__main__":
    ok = check_and_update(force=True, silent=False)
    sys.exit(0 if ok else 1)
