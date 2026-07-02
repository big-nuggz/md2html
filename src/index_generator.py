"""Generates the index.html page from the Welcome markdown content."""

import re
import json
from pathlib import Path

from .builder import OUT_ROOT, MD_ROOT
from .converter import convert_md_to_html


# Load the index template from file
TEMPLATES_DIR = Path(__file__).resolve().parent / 'templates'
INDEX_TEMPLATE = (TEMPLATES_DIR / 'index.html').read_text(encoding='utf-8')

# Load preferences
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PREFERENCES_PATH = PROJECT_ROOT / 'preferences.json'
if PREFERENCES_PATH.exists():
    with open(PREFERENCES_PATH, encoding='utf-8') as f:
        _prefs = json.load(f)
else:
    _prefs = {}
SITE_NAME = _prefs.get('site_name', 'md2html')
SITE_TITLE = _prefs.get('site_title', 'Home')


def _rewrite_index_links(html_body: str) -> str:
    """Rewrite image/src paths to point to the files/ directory.

    The index page is at out/index.html, but assets (images, PDFs, etc.)
    are copied to out/files/. This function prefixes img src paths
    with 'files/' so they resolve correctly.
    """
    def replace_src(match):
        attr = match.group(1)  # 'src' or 'href'
        quote = match.group(2)
        url = match.group(3)
        # Don't rewrite external URLs or already-prefixed paths
        if url.startswith(('http://', 'https://', '#', 'files/', '../', './', 'mailto:')):
            return f'{attr}={quote}{url}{quote}'
        return f'{attr}={quote}files/{url}{quote}'

    # Rewrite img src="..." and src='...'
    html_body = re.sub(
        r'(src)=(["\'])((?!http://|https://|#|files/|\.\./|\./|mailto:)[^\s"\']+)\2',
        replace_src,
        html_body,
    )
    return html_body


def generate_index() -> None:
    """Generate or update the index.html page at out/index.html.

    Uses md/index.md as the body content. Falls back to a simple message
    if the file doesn't exist.
    """
    welcome_path = MD_ROOT / 'index.md'
    if welcome_path.exists():
        md_content = welcome_path.read_text(encoding='utf-8')
        body_html = convert_md_to_html(md_content)
        body_html = _rewrite_index_links(body_html)
    else:
        body_html = '<p>Welcome to md2html. Add content to <code>md/index.md</code> to customize this page.</p>'

    index_html = INDEX_TEMPLATE.format(
        body=body_html,
        site_name=SITE_NAME,
        site_title=SITE_TITLE,
    )

    index_path = OUT_ROOT / 'index.html'
    index_path.write_text(index_html, encoding='utf-8')
    print(f"  Generated: index.html")
