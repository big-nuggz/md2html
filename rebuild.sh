#!/bin/bash
# md2html - Rebuild the entire static site
cd "$(dirname "$0")"
source ./venv/bin/activate
python -m src.cli