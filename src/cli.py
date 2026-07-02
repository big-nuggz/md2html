"""Command-line interface for the dividendos markdown-to-HTML converter."""

import sys
import argparse
from pathlib import Path

from .builder import build


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to static HTML pages.',
        epilog=(
            'Examples:\n'
            '  python src/cli.py                    # Rebuild everything\n'
            '  python src/cli.py md/guide.md        # Convert a single file\n'
            '  python src/cli.py md/notes/          # Convert a directory\n'
            '  python src/cli.py md/a.md md/b.md    # Convert multiple files'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        'targets',
        nargs='*',
        metavar='path',
        help='One or more .md files or directories to convert (default: rebuild all)',
    )
    parser.add_argument(
        '--version',
        action='version',
        version='dividendos 0.1.0',
    )

    args = parser.parse_args()

    # Resolve relative paths to absolute
    if args.targets:
        resolved = []
        for t in args.targets:
            p = Path(t)
            if not p.is_absolute():
                p = Path.cwd() / p
            resolved.append(str(p))
        build(resolved)
    else:
        build(None)


if __name__ == '__main__':
    main()