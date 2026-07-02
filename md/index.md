# Welcome to dividendos

This is a **static site** generated from Markdown files.

## Features

- Convert Markdown to beautiful HTML
- Automatic index page generation
- Dark mode support
- Syntax highlighting for code blocks
- Responsive design

## Quick Start

1. Add `.md` files to the `md/` directory
2. Run `python src/cli.py`
3. Open `out/index.html` in your browser

### Code Example

```python
def hello(name: str) -> str:
    return f"Hello, {name}!"

print(hello("dividendos"))
```

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `md/` | Your Markdown source files |
| `out/` | Generated HTML/CSS/JS output |
| `src/` | Python conversion scripts |

> **Tip:** You can organize files into subdirectories inside `md/` and they'll be mirrored in the output.