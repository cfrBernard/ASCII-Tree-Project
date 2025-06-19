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

DEFAULT_CONFIG = {"depth": 5, "excluded": []}


def get_treefy_dir(project_root: Path) -> Path:
    return project_root / ".treefy"


def get_config_path(project_root: Path) -> Path:
    return get_treefy_dir(project_root) / "config.json"


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


def init_treefy_folder(project_root: Path) -> None:
    treefy_dir = get_treefy_dir(project_root)
    treefy_dir.mkdir(exist_ok=True)

    # .treefyignore (fallback)
    ignore_file = treefy_dir / ".treefyignore"
    if not ignore_file.exists():
        ignore_file.write_text(DEFAULT_TREEFYIGNORE + "\n")

    # .gitignore
    ensure_line_in_gitignore(project_root)
    (treefy_dir / ".gitignore").write_text("# Automatically created by treefy\n*\n")

    # config.json
    config_path = get_config_path(project_root)
    if not config_path.exists():
        save_config(project_root, DEFAULT_CONFIG)


def load_config(project_root: Path) -> dict:
    config_path = get_config_path(project_root)
    if config_path.exists():
        try:
            return json.loads(config_path.read_text())
        except Exception as e:
            print(f"[WARN] Failed to load config: {e}")
    return DEFAULT_CONFIG.copy()


def save_config(project_root: Path, config: dict):
    config_path = get_config_path(project_root)
    try:
        config_path.write_text(json.dumps(config, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to save config: {e}")
