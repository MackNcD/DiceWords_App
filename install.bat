@echo off

REM Check Python version
python --version | findstr /R "3.10.*" > nul
if errorlevel 1 (
    echo Ensure you have Python 3.10 or higher installed.
    pause
    exit
)

REM Store the original directory (location of the batch file)
set original_dir=%~dp0

REM Navigate to the original directory (DiceWords_App-main)
cd /D %original_dir%

REM Create a python virtual environment
python -m venv .venv
if not exist ".venv" (
    echo Failed to create the virtual environment.
    pause
    exit
)

REM Activate the virtual environment using the call command
call .venv\Scripts\activate

REM Install the dependencies
pip install -r requirements.txt

REM Inform the user to open main.py in Windows Studio Code
echo Dependencies installed. Now, you can open main.py and run it in Windows Studio Code.
pause

REM Navigate to the dicewords directory inside DiceWords_App-main
cd /D "%original_dir%dicewords"

REM Check if the path exists before creating the folder
if not exist "%original_dir%dicewords" (
    echo The system cannot find the path specified.
    pause
    exit
)

REM Create the 'freshly created' folder
mkdir "freshly created"

REM Check if the folder was created successfully
if exist "%original_dir%dicewords\freshly created" (
    echo Folder 'freshly created' has been created.
) else (
    echo Failed to create the 'freshly created' folder.
)
pause
