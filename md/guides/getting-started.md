# Getting Started Guide

This guide will help you get up and running with md2html.

## Installation

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Creating Content

Create Markdown files in the `md/` directory. You can use any text editor.

### Basic Markdown

Here's a simple example:

```markdown
# My Page Title

Some **bold** and *italic* text.

- List item 1
- List item 2
- List item 3
```

## Building the Site

Run the converter:

```bash
python src/cli.py
```

This will:
1. Convert all `.md` files to `.html`
2. Copy any images or other assets
3. Generate the `index.html` page

## Viewing the Result

Open `out/index.html` in your web browser. All links use relative paths, so everything works offline without a server.

### Links Between Pages

You can link to other pages using standard Markdown link syntax:

```markdown
See the [main page](../index.md) for an overview.
```

These `.md` links are automatically rewritten to `.html` links during conversion.