"""Generates the index.html page from the Welcome markdown content."""

from pathlib import Path

from .builder import OUT_ROOT, MD_ROOT
from .converter import convert_md_to_html


# Load the index template from file
TEMPLATES_DIR = Path(__file__).resolve().parent / 'templates'
INDEX_TEMPLATE = (TEMPLATES_DIR / 'index.html').read_text(encoding='utf-8')


def generate_index() -> None:
    """Generate or update the index.html page at out/index.html.

    Uses md/index.md as the body content. Falls back to a simple message
    if the file doesn't exist.
    """
    welcome_path = MD_ROOT / 'index.md'
    if welcome_path.exists():
        md_content = welcome_path.read_text(encoding='utf-8')
        body_html = convert_md_to_html(md_content)
    else:
        body_html = '<p>Welcome to dividendos. Add content to <code>md/index.md</code> to customize this page.</p>'

    index_html = INDEX_TEMPLATE.format(
        body=body_html,
    )

    index_path = OUT_ROOT / 'index.html'
    index_path.write_text(index_html, encoding='utf-8')
    print(f"  Generated: index.html")