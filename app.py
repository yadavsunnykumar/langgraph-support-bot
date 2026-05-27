"""
Streamlit Cloud entry point.
Adds the project root to sys.path so `from src...` imports work,
then delegates to the actual app.
"""
import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import and run the actual app
from src.ui.streamlit_app import *  # noqa: F401, F403