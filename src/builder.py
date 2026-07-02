"""Orchestrates the build process: walks md/, converts files, copies assets, cleans orphans."""

import shutil
from pathlib import Path
from typing import Optional

from .converter import convert_file


# Project root paths (relative to this file's location)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MD_ROOT = PROJECT_ROOT / 'md'
OUT_ROOT = PROJECT_ROOT / 'out'
FILES_ROOT = OUT_ROOT / 'files'
CSS_SRC = PROJECT_ROOT / 'out' / 'css'
JS_SRC = PROJECT_ROOT / 'out' / 'js'

# File extensions to copy verbatim (images, PDFs, etc.)
BINARY_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico', '.pdf', '.zip', '.mp4', '.webm'}


def _copy_assets() -> None:
    """Ensure CSS and JS directories exist in out/."""
    (OUT_ROOT / 'css').mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / 'js').mkdir(parents=True, exist_ok=True)


def _clean_orphans() -> None:
    """Remove .html files in out/files/ that have no corresponding .md in md/.

    Only runs on a full build (no specific targets).
    """
    if not FILES_ROOT.exists():
        return

    for html_path in FILES_ROOT.rglob('*.html'):
        # Compute the relative path from FILES_ROOT
        rel = html_path.relative_to(FILES_ROOT)
        # Corresponding .md path in md/
        md_path = MD_ROOT / rel.with_suffix('.md')
        # Special case: md/index.md is used for the homepage, not a regular page
        if md_path.parent == MD_ROOT and md_path.stem == 'index':
            html_path.unlink()
            print(f"  Removed orphan: {html_path.relative_to(OUT_ROOT)} (index.md is reserved)")
            continue
        if not md_path.exists():
            html_path.unlink()
            print(f"  Removed orphan: {html_path.relative_to(OUT_ROOT)}")

    # Remove empty directories
    for dirpath in sorted(FILES_ROOT.rglob('*'), reverse=True):
        if dirpath.is_dir() and not any(dirpath.iterdir()):
            dirpath.rmdir()


def _copy_non_md(source_dir: Path, dest_dir: Path) -> None:
    """Copy non-markdown files from source_dir to dest_dir, preserving structure."""
    for item in source_dir.rglob('*'):
        if item.is_file() and item.suffix.lower() not in {'.md', '.markdown'}:
            rel = item.relative_to(source_dir)
            dest = dest_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)


def _process_file(md_path: Path) -> None:
    """Convert a single .md file to .html in the output directory."""
    rel = md_path.relative_to(MD_ROOT)
    out_path = FILES_ROOT / rel.with_suffix('.html')
    convert_file(md_path, out_path, MD_ROOT, FILES_ROOT)
    print(f"  Converted: {rel} -> out/files/{rel.with_suffix('.html')}")


def build(targets: Optional[list[str]] = None) -> None:
    """Main build entry point.

    Args:
        targets: List of file/directory paths to process.
                 If None, rebuilds everything from md/.
    """
    _copy_assets()

    if targets is None:
        # Full rebuild
        print("Building all files from md/...")
        _clean_orphans()

        if not MD_ROOT.exists():
            print("  No md/ directory found. Nothing to build.")
            return

        # Convert all .md files (except index.md which is used for the homepage)
        md_files = list(MD_ROOT.rglob('*.md')) + list(MD_ROOT.rglob('*.markdown'))
        for md_path in sorted(md_files):
            # Skip root index.md — it's used for the homepage, not a regular page
            if md_path.parent == MD_ROOT and md_path.stem == 'index':
                continue
            _process_file(md_path)

        # Copy non-markdown assets
        _copy_non_md(MD_ROOT, FILES_ROOT)

    else:
        # Process specific targets
        for target_str in targets:
            target_path = Path(target_str).resolve()

            if not target_path.exists():
                print(f"  Warning: '{target_str}' does not exist. Skipping.")
                continue

            if target_path.is_file():
                if target_path.suffix.lower() in {'.md', '.markdown'}:
                    _process_file(target_path)
                else:
                    # Copy non-md file
                    try:
                        rel = target_path.relative_to(MD_ROOT)
                        dest = FILES_ROOT / rel
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(target_path, dest)
                        print(f"  Copied: {rel}")
                    except ValueError:
                        print(f"  Warning: '{target_str}' is outside md/. Skipping.")
            elif target_path.is_dir():
                # Process all .md files in the directory
                for md_path in sorted(target_path.rglob('*.md')):
                    _process_file(md_path)
                for md_path in sorted(target_path.rglob('*.markdown')):
                    _process_file(md_path)
                # Copy non-md assets
                _copy_non_md(target_path, FILES_ROOT / target_path.relative_to(MD_ROOT)
                             if target_path != MD_ROOT else FILES_ROOT)

    # Generate index
    from .index_generator import generate_index
    generate_index()

    # Generate navigation JSON and inject nav tree into pages
    from .nav_generator import generate_nav_json, inject_nav_into_pages
    generate_nav_json()
    inject_nav_into_pages()

    print("Done.")
