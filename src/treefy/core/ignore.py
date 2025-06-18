# src/treefy/core/ignore.py

from pathlib import Path

import pathspec


def load_ignore_file(file: Path) -> list[str]:
    if file.exists():
        lines = file.read_text().splitlines()
        # ignore comments and empty lines
        return [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
    return []


def build_ignore_matcher(root: Path, use_gitignore: bool = True):

    patterns = []

    if use_gitignore:
        patterns += load_ignore_file(root / ".gitignore")

    patterns += load_ignore_file(root / ".treefy" / ".treefyignore")

    spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)

    def should_ignore(path: Path) -> bool:
        rel = path.relative_to(root)
        rel_str = str(rel)
        rel_str_dir = rel_str + "/" if path.is_dir() else rel_str

        # Match normal ET slashée
        return spec.match_file(rel_str) or spec.match_file(rel_str_dir)

    return should_ignore
