#!/usr/bin/env python3
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name("verify_1_0_5_optional_lock_overlay.py")), run_name="__main__")
