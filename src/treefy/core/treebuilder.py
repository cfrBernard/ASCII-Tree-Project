from pathlib import Path

from rich.console import Console
from rich.tree import Tree

from treefy.core.ignore import load_ignore_patterns

console = Console()


def build_tree(path: Path, ignore=None, max_depth=5):
    tree = Tree(f"[bold blue]{path.name}")
    _build_tree_rec(path, tree, ignore, max_depth)
    return tree


def _build_tree_rec(path, tree_node, ignore, depth):
    if depth == 0:
        return

    for child in sorted(path.iterdir()):
        if ignore and ignore(child):
            continue
        if child.is_dir():
            subtree = tree_node.add(f"[bold magenta]{child.name}/")
            _build_tree_rec(child, subtree, ignore, depth - 1)
        else:
            tree_node.add(child.name)


def run_cli():
    import argparse

    parser = argparse.ArgumentParser(description="Generate ASCII tree structure.")
    parser.add_argument("path", nargs="?", default=".", help="Target folder")
    parser.add_argument("--depth", type=int, default=5, help="Max tree depth")
    parser.add_argument("--use-gitignore", action="store_true", help="Respect .gitignore")
    args = parser.parse_args()

    path = Path(args.path).resolve()
    ignore = load_ignore_patterns(path) if args.use_gitignore else None
    tree = build_tree(path, ignore=ignore, max_depth=args.depth)
    console.print(tree)
