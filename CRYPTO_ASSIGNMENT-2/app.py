from pathlib import Path
import runpy
import sys

PROJECT_DIR = Path(__file__).resolve().parent / "DKIM_Virtual_Lab_Phase_2"
TARGET = PROJECT_DIR / "app.py"

if not TARGET.exists():
    raise FileNotFoundError(f"Expected Flask app at {TARGET}")

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

sys.argv[0] = str(TARGET)
runpy.run_path(str(TARGET), run_name="__main__")
