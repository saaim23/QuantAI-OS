#!/usr/bin/env python3
"""
QuantAI-OS - Entry Point
Run: python main.py analyze AAPL
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from quantai.cli import main

if __name__ == "__main__":
    main()
