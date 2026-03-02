# PowerShell script to launch Fast Lane backend
Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Definition -Parent)

if (-Not (Test-Path venv\Scripts\Activate.ps1)) {
    python -m venv venv
}

& .\venv\Scripts\Activate.ps1

pip install -r requirements.txt

python backend\main.py
