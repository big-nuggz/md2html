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

## Configuration

Site-wide preferences are stored in `preferences.json` at the project root:

```json
{
    "site_name": "md2html",
    "site_title": "Home"
}
```

| Key | Purpose |
|-----|---------|
| `site_name` | Used in page titles (`Page Title - site_name`), the header logo, and the footer |
| `site_title` | The title shown on the homepage's `<title>` tag |

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
│   ├── index.html      # Main page (from md/index.md)
│   ├── nav.json        # Navigation tree data
│   ├── css/style.css   # Stylesheet
│   ├── js/script.js    # JavaScript
│   └── files/          # Mirrors md/ structure as .html
├── preferences.json    # Site configuration
├── requirements.txt
├── rebuild.bat         # Windows rebuild script
├── rebuild.sh          # macOS/Linux rebuild script
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

## Writing Content

All your content lives in the `md/` directory. The structure you create there is mirrored exactly in the output.

### Markdown Files

- Create `.md` files anywhere inside `md/` — they become `.html` pages in `out/files/`
- Organize with subdirectories: `md/guides/topic.md` → `out/files/guides/topic.html`
- Link between pages using standard Markdown links: `[see guide](../guides/topic.md)` — these are automatically rewritten to `.html` links
- The `md/index.md` file is **special** — its content is rendered as the homepage at `out/index.html` (it is *not* copied to `out/files/`)

### Images & Assets

- Place images, PDFs, or any other files next to your `.md` files
- Reference them with relative paths: `![photo](cat.jpg)`
- Non-markdown files are copied verbatim to `out/files/` alongside the converted HTML pages

### Example Structure

```
md/
├── index.md                 ← Homepage content (Welcome text, images, etc.)
├── cat.jpg                  ← Image referenced by index.md
├── guides/
│   ├── getting-started.md   ← A regular page
│   └── guide-image.png      ← Image referenced by getting-started.md
└── notes/
    └── setup-notes.md
```

## How It Works

1. Place `.md` files and assets in the `md/` directory, organized however you like
2. Run the converter — it walks the entire tree, converts every `.md` to `.html`, copies non-markdown assets, generates the homepage from `md/index.md`, and builds a navigation sidebar
3. Open `out/index.html` in any browser — everything works with relative paths

## Requirements

- Python 3.9+
- `markdown` library
- `pygments` (for syntax highlighting)

## AI

The entire md2html project was developed using AI assistance, specifically the **DeepSeek-V4-Flash** model.

## License

MIT
