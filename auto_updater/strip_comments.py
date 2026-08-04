import ast
import io
import sys
import tokenize
from pathlib import Path

TARGET_EXTENSIONS = {".py"}

def strip_hash_comments(source):
    lines = source.splitlines(keepends=True)
    comment_rows = {}

    tokgen = tokenize.generate_tokens(io.StringIO(source).readline)
    for tok in tokgen:
        if tok.type == tokenize.COMMENT:
            row, col = tok.start
            if row not in comment_rows or col < comment_rows[row]:
                comment_rows[row] = col

    for row, col in comment_rows.items():
        idx = row - 1
        line = lines[idx]
        newline = ""
        if line.endswith("\r\n"):
            newline = "\r\n"
        elif line.endswith("\n"):
            newline = "\n"
        truncated = line[:col].rstrip()
        lines[idx] = (truncated + newline) if truncated else newline

    return "".join(lines)

def strip_docstrings(source):
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source

    lines = source.splitlines(keepends=True)
    doc_nodes = []

    def check_body(node):
        body = getattr(node, "body", None)
        if not body:
            return
        first = body[0]
        if (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        ):
            doc_nodes.append(first)

    check_body(tree)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            check_body(node)

    for node in doc_nodes:
        start = node.lineno - 1
        end = node.end_lineno
        for i in range(start, end):
            line = lines[i]
            newline = ""
            if line.endswith("\r\n"):
                newline = "\r\n"
            elif line.endswith("\n"):
                newline = "\n"
            lines[i] = newline

    return "".join(lines)

def collapse_blank_lines(source, max_consecutive=1):
    lines = source.splitlines(keepends=True)
    result = []
    blank_run = 0
    for line in lines:
        if line.strip() == "":
            blank_run += 1
            if blank_run <= max_consecutive:
                result.append(line if line else "\n")
        else:
            blank_run = 0
            result.append(line)
    return "".join(result)

def process_source(source):
    no_comments = strip_hash_comments(source)
    no_docstrings = strip_docstrings(no_comments)
    cleaned = collapse_blank_lines(no_docstrings, max_consecutive=1)
    return cleaned

def verify_equivalent(original, cleaned, path):
    try:
        ast.parse(cleaned)
    except SyntaxError as e:
        raise RuntimeError(f"{path}: resulting file has a syntax error: {e}")

    def strip_doc(dump_tree_source):
        tree = ast.parse(dump_tree_source)
        targets = [tree] + [
            n for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        ]
        for node in targets:
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(
                body[0].value, ast.Constant
            ) and isinstance(body[0].value.value, str):
                body.pop(0)
        return ast.dump(tree)

    orig_norm = strip_doc(original)
    clean_norm = ast.dump(ast.parse(cleaned))
    if orig_norm != clean_norm:
        raise RuntimeError(f"{path}: AST changed beyond comments/docstrings removal")

def process_file(path: Path, in_place=True, backup_dir=None):
    original = path.read_text(encoding="utf-8")
    cleaned = process_source(original)
    verify_equivalent(original, cleaned, path)

    if backup_dir is not None:
        rel = path
        backup_path = backup_dir / rel.name
        backup_path.write_text(original, encoding="utf-8")

    if in_place:
        path.write_text(cleaned, encoding="utf-8")
    return cleaned

def main():
    if len(sys.argv) < 2:
        print("Uso: python strip_comments.py <pasta_do_projeto> [--backup]")
        sys.exit(1)

    target_dir = Path(sys.argv[1]).resolve()
    make_backup = "--backup" in sys.argv[2:]

    if not target_dir.is_dir():
        print(f"Pasta nao encontrada: {target_dir}")
        sys.exit(1)

    backup_dir = None
    if make_backup:
        backup_dir = target_dir.parent / (target_dir.name + "_backup_pre_strip")
        backup_dir.mkdir(exist_ok=True)

    py_files = sorted(p for p in target_dir.rglob("*.py"))
    print(f"Encontrados {len(py_files)} arquivos .py em {target_dir}")

    changed = 0
    errors = 0
    for path in py_files:
        try:
            before = path.read_text(encoding="utf-8")
            after = process_file(path, in_place=True, backup_dir=backup_dir)
            if after != before:
                changed += 1
                print(f"  limpo: {path.relative_to(target_dir)}")
        except Exception as e:
            errors += 1
            print(f"  ERRO em {path.relative_to(target_dir)}: {e}")

    print(f"\nConcluido. {changed} arquivo(s) alterado(s). {errors} erro(s).")
    if errors:
        sys.exit(2)

if __name__ == "__main__":
    main()
