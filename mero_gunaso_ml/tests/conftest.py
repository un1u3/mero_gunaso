from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
VENV_LIB = ROOT / ".venv" / "lib"


if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if VENV_LIB.exists():
    for site_packages in sorted(VENV_LIB.glob("python*/site-packages")):
        if str(site_packages) not in sys.path:
            sys.path.insert(0, str(site_packages))
