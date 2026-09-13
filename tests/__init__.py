import sys
from pathlib import Path

# Ensure repository and parent directories are on sys.path
_repo_dir = Path(__file__).resolve().parent.parent
_parent_dir = _repo_dir.parent

if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))
if str(_repo_dir) not in sys.path:
    sys.path.insert(0, str(_repo_dir))
