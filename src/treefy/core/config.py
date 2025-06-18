# src/treefy/core/config.py

import json
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


def get_config_path(project_root: Path) -> Path:
    return project_root / ".treefy" / "config.json"


def load_config(project_root: Path) -> dict:
    config_path = get_config_path(project_root)
    if config_path.exists():
        try:
            return json.loads(config_path.read_text())
        except Exception as e:
            print(f"[WARN] Failed to load config: {e}")
    return {"depth": 5, "deselected": []}  # fallback


def save_config(project_root: Path, config: dict):
    config_path = get_config_path(project_root)
    try:
        config_path.write_text(json.dumps(config, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to save config: {e}")


def init_treefy_folder(project_root: Path) -> Path:

    treefy_dir = project_root / ".treefy"
    treefy_dir.mkdir(exist_ok=True)

    ignore_file = treefy_dir / ".treefyignore"
    if not ignore_file.exists():
        ignore_file.write_text(DEFAULT_TREEFYIGNORE + "\n")

    # handle .gitignore (root & .treefy/)
    ensure_line_in_gitignore(project_root)
    (treefy_dir / ".gitignore").write_text("# Automatically created by treefy\n*\n")

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
