
import argparse
import datetime
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.dirname(HERE)

EXCLUDE_SEGMENTS = {
    "saved games",
    "__pycache__",
    "_update_tmp",
    ".git",
}
EXCLUDE_FILES = {
    "jjts_config.json",
    "manifest.json",
    ".game_version",
    ".gitignore",
    "publish.py",
    "build_manifest.py",
    "strip_comments.py",
}

def excluded(rel):
    parts = rel.split("/")
    if any(p in EXCLUDE_SEGMENTS for p in parts):
        return True
    if rel.split("/")[-1] in EXCLUDE_FILES:
        return True
    return False

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            chunk = chunk.replace(b"\r\n", b"\n")
            h.update(chunk)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Gera manifest.json + version.json")
    parser.add_argument("-v", "--version", required=True, help="Versao nova (ex: 1.8.0)")
    parser.add_argument("-c", "--changelog", default="", help="Notas da versao")
    args = parser.parse_args()

    with open(
        os.path.join(GAME_DIR, "version.json"), "w", encoding="utf-8", newline="\n"
    ) as f:
        json.dump(
            {"version": args.version, "changelog": args.changelog},
            f,
            indent=2,
            ensure_ascii=False,
        )

    files = []
    for root, dirs, names in os.walk(GAME_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_SEGMENTS]
        for name in sorted(names):
            if name.endswith(".pyc"):
                continue
            full = os.path.join(root, name)
            rel = os.path.relpath(full, GAME_DIR).replace(os.sep, "/")
            if excluded(rel):
                continue
            files.append(
                {
                    "path": rel,
                    "size": os.path.getsize(full),
                    "sha256": sha256_file(full),
                }
            )
    files.sort(key=lambda f: f["path"])

    manifest = {
        "version": args.version,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="seconds"
        ),
        "files": files,
    }
    with open(
        os.path.join(GAME_DIR, "manifest.json"), "w", encoding="utf-8", newline="\n"
    ) as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    total = sum(fi["size"] for fi in files)
    print(f"manifest.json: {len(files)} arquivos, {total} bytes")
    print(f"version.json : v{args.version}")

if __name__ == "__main__":
    main()
