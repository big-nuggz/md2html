"""Core markdown to HTML conversion logic."""

import markdown
import re
from pathlib import Path


# Load the page template from file
TEMPLATES_DIR = Path(__file__).resolve().parent / 'templates'
PAGE_TEMPLATE = (TEMPLATES_DIR / 'page.html').read_text(encoding='utf-8')


def convert_md_to_html(md_content: str) -> str:
    """Convert Markdown string to HTML body content."""
    extensions = [
        'fenced_code',
        'codehilite',
        'tables',
        'toc',
        'sane_lists',
        'smarty',
    ]
    extension_configs = {
        'codehilite': {
            'css_class': 'highlight',
            'guess_lang': True,
        },
    }
    html = markdown.markdown(
        md_content,
        extensions=extensions,
        extension_configs=extension_configs,
    )
    return html


def rewrite_md_links(html_body: str, source_rel_dir: Path) -> str:
    """Rewrite .md links to .html links within the HTML body.

    Handles:
      - [text](somefile.md)
      - [text](path/to/somefile.md#anchor)
      - [text](somefile.md?query=param)
    """
    def replace_link(match):
        full = match.group(0)
        # Extract just the URL part between ( and )
        paren_start = full.index('(')
        inner = full[paren_start + 1:-1]
        # Match .md links
        md_link_pattern = re.compile(r'^([^)]*?)\.md([#?].*)?$', re.IGNORECASE)
        m = md_link_pattern.match(inner)
        if m:
            new_url = m.group(1) + '.html' + (m.group(2) or '')
            return full[:paren_start + 1] + new_url + ')'
        return full

    # Match markdown links and images [text](url) or ![alt](url)
    pattern = re.compile(r'(!?\[[^\]]*\]\([^)]+\))')
    return pattern.sub(replace_link, html_body)


def extract_title(md_content: str) -> str:
    """Extract the first H1 heading from markdown content as the page title."""
    for line in md_content.splitlines():
        stripped = line.strip()
        if stripped.startswith('# ') and not stripped.startswith('## '):
            return stripped[2:].strip()
    return 'Untitled'


def wrap_in_template(html_body: str, title: str, rel_depth: int) -> str:
    """Wrap HTML body in the full page template.

    Args:
        html_body: The converted markdown HTML body.
        title: Page title.
        rel_depth: How many directory levels deep from out/files/ root.
                   0 = root, 1 = one subdir deep, etc.
    """
    # Files are in out/files/..., CSS is in out/css/, index is in out/index.html
    # So we always need at least one ../ to go from out/files/ up to out/
    parent_prefix = '../' * (rel_depth + 1)
    css_path = parent_prefix + 'css/style.css'
    index_path = parent_prefix + 'index.html'
    js_path = parent_prefix + 'js/script.js'

    return PAGE_TEMPLATE.format(
        title=title,
        css_path=css_path,
        index_path=index_path,
        js_path=js_path,
        body=html_body,
    )


def convert_file(md_path: Path, out_path: Path, md_root: Path, out_root: Path) -> None:
    """Convert a single markdown file to HTML and write it.

    Args:
        md_path: Path to the .md file.
        out_path: Path where .html should be written.
        md_root: Root of the markdown directory.
        out_root: Root of the output files directory.
    """
    md_content = md_path.read_text(encoding='utf-8')

    # Calculate relative depth of this file from out/files/ root
    rel_path = out_path.relative_to(out_root)
    rel_depth = len(rel_path.parents) - 1  # -1 because the file itself counts as a parent

    title = extract_title(md_content)
    html_body = convert_md_to_html(md_content)
    html_body = rewrite_md_links(html_body, md_path.parent)
    full_html = wrap_in_template(html_body, title, rel_depth)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(full_html, encoding='utf-8')