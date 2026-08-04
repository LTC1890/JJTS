
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.dirname(HERE)
STRIP = os.path.join(HERE, "strip_comments.py")
BUILD = os.path.join(HERE, "build_manifest.py")

def run(cmd, cwd=GAME_DIR):
    print(">", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd)

def git(*args):
    return subprocess.run(
        ["git", *args], cwd=GAME_DIR, text=True, capture_output=True
    )

def current_version():
    try:
        with open(os.path.join(GAME_DIR, "version.json"), encoding="utf-8") as f:
            return str(json.load(f).get("version", "0.0.0"))
    except Exception:
        return "0.0.0"

def bump(version):
    parts = [int(p) for p in version.split(".")]
    while len(parts) < 3:
        parts.append(0)
    parts[-1] += 1
    return ".".join(str(p) for p in parts)

def main():
    parser = argparse.ArgumentParser(description="Publica nova versao do JJTS no GitHub")
    parser.add_argument("-v", "--version", help="Versao (padrao: bump patch automatico)")
    parser.add_argument("-c", "--changelog", help="Notas da versao (padrao: vazio)")
    parser.add_argument("--repo", help="URL do repositorio (ex: https://github.com/USER/REPO.git)")
    parser.add_argument("--no-push", action="store_true", help="Prepara tudo, mas nao faz push")
    args = parser.parse_args()

    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        print("Git nao inicializado - rodando git init -b main")
        run(["git", "init", "-b", "main"])

    if not git("config", "user.name").stdout.strip():
        run(["git", "config", "user.name", "LTC1890"])
    if not git("config", "user.email").stdout.strip():
        run(["git", "config", "user.email", "LTC1890@users.noreply.github.com"])

    if args.repo:
        r = git("remote", "get-url", "origin")
        if r.returncode != 0:
            run(["git", "remote", "add", "origin", args.repo])
        elif r.stdout.strip() != args.repo:
            run(["git", "remote", "set-url", "origin", args.repo])

    print("\n=== 1. Removendo comentarios ===")
    if run([sys.executable, STRIP, GAME_DIR]).returncode != 0:
        print("Falha no strip_comments - abortando")
        sys.exit(1)

    if not args.version:
        args.version = bump(current_version())
        print(f"Bump automatico: v{args.version}")
    else:
        print(f"Versao: v{args.version}")

    if not args.changelog:
        args.changelog = ""
        print("Changelog: (vazio)")

    print("\n=== 2. Gerando manifest.json + version.json ===")
    if run(
        [sys.executable, BUILD, "-v", args.version, "-c", args.changelog]
    ).returncode != 0:
        print("Falha no build_manifest - abortando")
        sys.exit(1)

    print("\n=== 3. Commit + tag ===")
    run(["git", "add", "-A"])
    message = f"v{args.version}"
    if args.changelog:
        message += f" - {args.changelog}"
    run(["git", "commit", "-m", message])
    run(["git", "tag", f"v{args.version}"])

    if args.no_push:
        print("\n--no-push: tudo pronto localmente. Para publicar:")
        print("  git push -u origin main --tags")
        return

    print("\n=== 4. Push ===")
    branch = "main"
    r = git("rev-parse", "--abbrev-ref", "HEAD")
    if r.returncode == 0 and r.stdout.strip():
        branch = r.stdout.strip()
    if run(["git", "push", "-u", "origin", branch, "--tags"]).returncode != 0:
        print("Falha no push. Verifique: git remote -v e credenciais.")
        sys.exit(1)

    print(f"\nPublicado v{args.version} com sucesso!")

if __name__ == "__main__":
    main()
