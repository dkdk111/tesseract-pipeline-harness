"""Entry point for ``python -m tesseract_pipeline``."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
