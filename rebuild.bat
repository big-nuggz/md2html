@echo off
REM md2html - Rebuild the entire static site
cd /d "%~dp0"
call .\venv\Scripts\activate
python -m src.cli
pause