@echo off
REM md2html - Rebuild the entire static site
cd /d "%~dp0"
".\venv\Scripts\python" -m src.cli
pause