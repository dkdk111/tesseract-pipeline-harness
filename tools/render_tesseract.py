#!/usr/bin/env python3
"""Back-compatible shim for the trace renderer.

The renderer now lives in the package. This wrapper lets you keep running:

    python tools/render_tesseract.py examples/01_market_brief/tesseract.json

The equivalent, once the package is importable, is:

    python -m tesseract_pipeline render examples/01_market_brief/tesseract.json
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tesseract_pipeline.render import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(sys.argv))
