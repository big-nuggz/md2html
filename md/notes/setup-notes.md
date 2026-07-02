# Setup Notes

Personal notes about setting up the md2html project.

## Requirements

- Python 3.9+
- pip

## Virtual Environment

It's a good idea to use a virtual environment:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

## Troubleshooting

### Permission Issues

If you get permission errors on Windows, try:

1. Running your terminal as Administrator
2. Or using `--user` flag: `pip install --user -r requirements.txt`

### File Not Found

Make sure you're running the script from the project root directory:

```
md2html/
├── src/
├── md/
└── out/
```

> **Note:** The script must be run from the project root so it can find the `md/` and `out/` directories.