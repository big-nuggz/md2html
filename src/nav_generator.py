"""Generates nav.json and nav tree HTML for the navigation menu."""

import json
from pathlib import Path
from html import escape

from .builder import FILES_ROOT, OUT_ROOT


def generate_nav_json() -> None:
    """Generate nav.json at out/nav.json with the page tree structure."""
    tree = _build_tree(FILES_ROOT, FILES_ROOT)
    nav_path = OUT_ROOT / 'nav.json'
    nav_path.write_text(json.dumps(tree, indent=2), encoding='utf-8')
    print(f"  Generated: nav.json")


def generate_nav_tree_html() -> str:
    """Build the HTML string for the sidebar navigation tree."""
    tree = _build_tree(FILES_ROOT, FILES_ROOT)
    return _tree_to_html(tree)


def inject_nav_into_pages() -> None:
    """Inject the nav tree HTML into all generated .html files."""
    if not FILES_ROOT.exists():
        return

    base_nav_html = generate_nav_tree_html()
    placeholder = '<div class="flex-1 overflow-y-auto py-1" id="sideNavTree">'

    # Update files under out/files/
    for html_path in list(FILES_ROOT.rglob('*.html')):
        # Calculate depth from out/ root
        rel = html_path.relative_to(OUT_ROOT)
        depth = len(rel.parents) - 1  # e.g. files/guides/page.html -> 2 levels up
        prefix = '../' * depth
        nav_html = _prefix_nav_links(base_nav_html, prefix)
        _inject_nav(html_path, nav_html, placeholder)

    # Update root index.html
    index_path = OUT_ROOT / 'index.html'
    if index_path.exists():
        _inject_nav(index_path, base_nav_html, placeholder)


def _prefix_nav_links(html: str, prefix: str) -> str:
    """Add a prefix to all href values in nav links (e.g. files/... -> ../../files/...)."""
    if not prefix:
        return html
    # Replace href="files/ with href="<prefix>files/
    return html.replace('href="files/', 'href="' + prefix + 'files/')


def _build_tree(directory: Path, rel_root: Path) -> list:
    """Recursively build a list of dicts representing the file tree.

    Each entry is either:
      {"type": "file", "name": "...", "path": "..."}
      {"type": "dir",  "name": "...", "children": [...]}
    """
    items = []
    entries = sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))

    for entry in entries:
        rel = entry.relative_to(rel_root)
        name = entry.stem.replace('-', ' ').replace('_', ' ').title()

        if entry.is_dir():
            children = _build_tree(entry, rel_root)
            # Only include directories that have .html files somewhere inside
            has_html = any(f.suffix == '.html' for f in entry.rglob('*'))
            if has_html or children:
                items.append({
                    "type": "dir",
                    "name": entry.name,
                    "children": children,
                })
        elif entry.suffix == '.html':
            items.append({
                "type": "file",
                "name": name,
                "path": "files/" + rel.as_posix(),
            })

    return items


def _tree_to_html(items: list) -> str:
    """Convert nav tree items to nested HTML."""
    html = '<ul class="nav-list">'
    for item in items:
        if item['type'] == 'file':
            html += (
                f'<li class="nav-item">'
                f'<a class="nav-link" href="{escape(item["path"])}">{escape(item["name"])}</a>'
                f'</li>'
            )
        elif item['type'] == 'dir':
            html += (
                f'<li class="nav-item nav-folder">'
                f'<details class="nav-details" open>'
                f'<summary class="nav-folder-summary">'
                f'<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 inline mr-1 -mt-0.5">'
                f'<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />'
                f'</svg>'
                f'{escape(item["name"])}</summary>'
                f'<div class="nav-folder-contents">'
            )
            if item.get('children'):
                html += _tree_to_html(item['children'])
            html += '</div></details></li>'
    html += '</ul>'
    return html


def _inject_nav(html_path: Path, nav_html: str, placeholder: str) -> None:
    """Replace the nav tree placeholder in a single HTML file."""
    content = html_path.read_text(encoding='utf-8')
    old_marker = placeholder + '</div>'
    new_marker = placeholder + nav_html + '</div>'
    if old_marker in content:
        content = content.replace(old_marker, new_marker, 1)
        html_path.write_text(content, encoding='utf-8')