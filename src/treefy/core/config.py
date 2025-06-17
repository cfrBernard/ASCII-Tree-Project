from pathlib import Path

DEFAULT_TREEFYIGNORE = """
.git/
.gitignore
.treefy/
__pycache__/
*.pyc
.venv/
env/
venv/
node_modules/
*.log
""".strip()


def init_treefy_folder(project_root: Path) -> Path:

    treefy_dir = project_root / ".treefy"
    treefy_dir.mkdir(exist_ok=True)

    ignore_file = treefy_dir / ".treefyignore"
    if not ignore_file.exists():
        ignore_file.write_text(DEFAULT_TREEFYIGNORE + "\n")

    ensure_line_in_gitignore(project_root)

    return ignore_file


def ensure_line_in_gitignore(root: Path, line: str = ".treefy/"):
    comment = "# Treefy stuff"
    gitignore = root / ".gitignore"

    if gitignore.exists():
        content = gitignore.read_text().splitlines()

        if line not in content:
            with gitignore.open("a") as f:
                f.write(f"\n{comment}\n{line}\n")
    else:
        gitignore.write_text(f"{comment}\n{line}\n")
