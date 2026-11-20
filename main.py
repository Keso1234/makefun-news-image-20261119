#!/usr/bin/env python3
"""Copy the pre-rendered entry.png to the output directory.

Self-contained: stdlib only, no local module imports.
Works under `python3 -P -s` from any working directory.
"""

import os
import shutil
from pathlib import Path


def main():
    source = Path(__file__).resolve().parent / "entry.png"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"
    shutil.copyfile(source, destination)
    size = destination.stat().st_size
    print(f"Output: {destination}")
    print(f"Size: {size} bytes")


if __name__ == "__main__":
    main()
