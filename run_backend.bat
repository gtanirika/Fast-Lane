@echo off
REM --- Fast Lane backend launcher ---
cd /d "%~dp0"

:: create virtual environment if missing
if not exist venv\Scripts\activate.bat (
    python -m venv venv
)

call venv\Scripts\activate

:: install requirements if not already installed
pip install -r requirements.txt

:: start the server
python backend\main.py
