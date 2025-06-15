from pathlib import Path

import pathspec


def load_ignore_patterns(project_path: Path):
    gitignore_path = project_path / ".gitignore"
    if not gitignore_path.exists():
        return None
    patterns = gitignore_path.read_text().splitlines()
    spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    return lambda path: spec.match_file(str(path.relative_to(project_path)))
