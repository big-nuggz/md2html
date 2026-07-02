# md2html

A **zero-dependency** (beyond `markdown` + `pygments`) static site generator that converts Markdown files to clean, responsive HTML pages. No server needed — just open the generated files in your browser.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Convert all markdown files
python -m src.cli

# Open the generated site
open out/index.html
```

### Convenience Rebuild Scripts

For even easier rebuilding, use the provided scripts:

| Platform | Command |
|----------|---------|
| **Windows** | Double-click `rebuild.bat` or run `.\rebuild.bat` |
| **macOS / Linux** | Run `./rebuild.sh` |

## Usage

```bash
# Full rebuild (convert everything in md/)
python -m src.cli

# Convert specific files
python -m src.cli md/guide.md

# Convert a directory
python -m src.cli md/notes/

# Convert multiple targets
python -m src.cli md/a.md md/b.md
```

## Project Structure

```
md2html/
├── src/                # Python scripts
│   ├── cli.py          # CLI entry point (argparse)
│   ├── builder.py      # Build orchestrator
│   ├── converter.py    # Markdown → HTML conversion
│   └── index_generator.py  # Index page generation
├── md/                 # Your Markdown source files
│   └── (any structure)
├── out/                # Generated output
│   ├── index.html      # Main navigation page
│   ├── css/style.css   # Stylesheet
│   ├── js/script.js    # JavaScript
│   └── files/          # Mirrors md/ structure as .html
├── requirements.txt
└── README.md
```

## Features

- **Zero server required** — all links use relative paths, works offline
- **Mirrors your directory structure** — `md/subdir/doc.md` → `out/files/subdir/doc.html`
- **Automatic index page** — navigable file tree with collapsible folders
- **Syntax highlighting** — via highlight.js (loaded from CDN)
- **Dark mode** — automatically matches your OS preference
- **Responsive design** — works on mobile and desktop
- **Smart link rewriting** — `[link](other.md)` → `<a href="other.html">` automatically
- **Asset passthrough** — images, PDFs, etc. are copied verbatim
- **Orphan cleanup** — removed `.html` files are cleaned on full rebuild

## How It Works

1. Place `.md` files in the `md/` directory, organized however you like
2. Run the converter — it walks the entire tree, converts every `.md` to `.html`, copies non-markdown assets, and generates `out/index.html`
3. Open `out/index.html` in any browser — everything works with relative paths

## Requirements

- Python 3.9+
- `markdown` library
- `pygments` (for syntax highlighting)

## AI

The entire md2html project was developed using AI assistance, specifically the **DeepSeek-V4-Flash** model.

## License

MIT
