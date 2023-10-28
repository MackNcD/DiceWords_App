@echo off

REM Check Python version
python --version | findstr /R "3.10.*" > nul
if errorlevel 1 (
    echo Ensure you have Python 3.10 or higher installed.
    pause
    exit
)


REM Navigate to the main DiceWords folder
cd /D %~dp0


REM Create a python virtual environment
python -m venv .venv


REM Activate the virtual environment
.venv\Scripts\activate


REM Install the dependencies
pip install -r requirements.txt


REM Inform the user to open main.py in Windows Studio Code
echo Dependencies installed. Now, you can open main.py and run it in Windows Studio Code.
pause
