import shutil
import subprocess
import sys
import tomllib  # Python 3.11+
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
SRC_ENTRY = PROJECT_ROOT / "src" / "treefy" / "__main__.py"
HOOKS_DIR = PROJECT_ROOT / "hooks"
ICON_PATH = PROJECT_ROOT / "assets" / "treefy.ico"
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
BUILD_DIR = PROJECT_ROOT / "build"
DIST_DIR = PROJECT_ROOT / "dist"
SPEC_DIR = BUILD_DIR / "specs"

ONEFILE = True  # Set to False for easier debugging [--onedir]


def read_version() -> str:
    try:
        with PYPROJECT_PATH.open("rb") as f:
            data = tomllib.load(f)
        return data["project"]["version"]
    except Exception as e:
        print(f"❌ Failed to read version from pyproject.toml: {e}")
        sys.exit(1)


def clean_previous_builds():
    for folder in [BUILD_DIR, DIST_DIR]:
        if folder.exists():
            print(f"Removing {folder}")
            shutil.rmtree(folder)


def build():
    cmd = [
        "pyinstaller",
        "--name",
        BUILD_NAME,
        "--additional-hooks-dir",
        str(HOOKS_DIR),
        "--icon",
        str(ICON_PATH),
        "--noconsole",
        f"--specpath={SPEC_DIR}",
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR / 'work'}",
        str(SRC_ENTRY),
    ]

    cmd.append("--onefile" if ONEFILE else "--onedir")

    print("Building with:")
    print("   " + " ".join(cmd))
    subprocess.run(cmd, check=True)

    print(f"\n✅ Build completed: dist/{BUILD_NAME}/")


if __name__ == "__main__":
    version = read_version()
    BUILD_NAME = f"treefy_v{version}"

    if not HOOKS_DIR.exists() or not (HOOKS_DIR / "hook-customtkinter.py").exists():
        print("❌ Missing hook for customtkinter in ./hooks/.")
        sys.exit(1)

    if not ICON_PATH.exists():
        print("❌ Missing icon file: ./assets/treefy.ico")
        sys.exit(1)

    clean_previous_builds()
    build()
