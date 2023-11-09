@echo off
setlocal enabledelayedexpansion

:: Customize the appearance of the command line
color 0B

:: Attempt to resize the command prompt window to 80 columns and 25 lines
mode con: cols=120 lines=25

:: Retrieve the local and GitHub versions
call :getPythonVersion
call :getAppVersion
call :getGitHubVersion

:menu
cls
call :printLine
call :printCentered "APP MANAGEMENT CONSOLE"
call :printLine
call :printCentered "Python version: !python_version!"
call :printCentered "Local App version: !app_version!"
call :printCentered "Latest GitHub version: !github_version!"
call :printLine
call :printCentered "1. Run App"
call :printCentered "2. Install App"
call :printCentered "3. Retrieve Templates/DiceWords from Discord"
call :printCentered "4. Check GitHub for Updates"
call :printCentered "5. Exit"
call :printLine
echo.

:: Get user choice
set /p choice="Enter your choice (1/2/3/4/5): "
if not "%choice%"=="" (
    if "%choice%"=="1" goto run
    if "%choice%"=="2" goto install
    if "%choice%"=="3" goto joinDiscord
    if "%choice%"=="4" goto goToGitHub
    if "%choice%"=="5" goto confirmExit
)

call :printCentered "Invalid choice. Please enter a valid number (1, 2, 3, 4, or 5)."
pause
goto menu

:run
if not exist .venv\ (
    call :printCentered "The virtual environment is not set up. Please install the application first."
    pause
    goto menu
)

if not exist DiceWords_App.py (
    call :printCentered "The Python script 'DiceWords_App.py' does not exist."
    pause
    goto menu
)

call :printCentered "Running the application..."
pushd .venv\Scripts
call activate
popd
python DiceWords_App.py
call deactivate
call :printCentered "Application has stopped."
pause
goto menu

:install
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    call :printCentered "Python is not installed or not in the PATH."
    pause
    goto menu
)

if not exist .venv\ (
    call :printCentered "Creating a virtual environment..."
    python -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        call :printCentered "Failed to create a virtual environment."
        pause
        goto menu
    )
    call :printCentered "Virtual environment created."
)

call :printCentered "Activating the virtual environment..."
pushd .venv\Scripts
call activate
popd

call :printCentered "Installing requirements..."
pip install -r requirements.txt > assets\other\install_log.txt 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :printCentered "Failed to install requirements. Check 'assets\other\install_log.txt' for details."
    pause
    goto menu
)
call :printCentered "Dependencies installed successfully. See 'assets\other\install_log.txt' for details."

call :printCentered "Please enter your username:"
set /p username=

:: Save the username into username.txt
echo username="{%username%}" > assets/other/username.txt

call :printCentered "Username registered. Username, templates and dicewords can be edited via text files from the relevant directories."
timeout /t 7 /nobreak 1>nul
call :printCentered "Give us just a few more seconds, the flux capacitors are warming."
timeout /t 5 /nobreak 1>nul
call :printCentered "WARNING: The available DiceWords and templates are not the sole intended use of this application. 
timeout /t 5 /nobreak 1>nul
call :printCentered "They are only intended to spark creativity and lend random ideas in specific forms the user *may* desire - 
timeout /t 5 /nobreak 1>nul
call :printCentered "as well as to provide an example of what is possible."
timeout /t 3 /nobreak 1>nul
call :printCentered "In the area of alterations and form fitting the mechanations to produce wildly unique and differing results,"
timeout /t 2 /nobreak 1>nul
call :printCentered "we here at Mythamnis intended for this application (and such had constructed it so) to be as visible, simple"
timeout /t 1 /nobreak 1>nul
call :printCentered " and as easy an experience as it could possibly be;"
timeout /t 9 /nobreak 1>nul
call :printCentered "so any application of the vast array of ideas the program could possibly serve are in easy reach." 
timeout /t 8 /nobreak 1>nul
call :printCentered "All variable data, input, output, and parametrical affects are editable in the enclosed .txt files."
timeout /t 9 /nobreak 1>nul
call :printCentered "CONSOLE: FLUX CAPACITORS PRIMED, VELOCITY ACHEIVED"
timeout /t 3 /nobreak 1>nul
call :printCentered "That's our cue!"
timeout /t 2 /nobreak 1>nul
call :printCentered "CONSOLE: FLUX CAPACITORS PRIMED, VELOCITY ACHEIVED"
timeout /t 1 /nobreak 1>nul
call :printCentered "CONSOLE: FLUX CAPACITORS PRIMED, VELOCITY ACHEIVED"
timeout /t 1 /nobreak 1>nul
call :printCentered "CONSOLE: FLUX CAPACITORS PRIMED, VELOCITY ACHEIVED"
timeout /t 1 /nobreak 1>nul
call :printCentered "Give us a second!"
timeout /t 2 /nobreak 1>nul
call :printCentered "The .txt files are few, and they're self-evident in name."
timeout /t 2 /nobreak 1>nul
call :printCentered "Visit us on discord, we can be pretty neat at times.
timeout /t 5 /nobreak 1>nul
call :printCentered "If you have, or decide to make a library, or even a few .txts, post it for the rest of us, please."
timeout /t 2 /nobreak 1>nul
call :printCentered "Happy rolling."

echo.
pause
goto menu



:joinDiscord
start https://discord.gg/HE5CVrYm
goto menu

:goToGitHub
start https://github.com/MackNcD/DiceWords_App
goto menu

:confirmExit
goto end

:end
call :printCentered "Exiting..."
endlocal
exit /b 0

:: Function to retrieve Python version
:getPythonVersion
for /f "delims=" %%i in ('python --version 2^>^&1') do set python_version=%%i
goto :eof

:: Function to retrieve App version
:getAppVersion
if exist assets\other\version.txt (
    set /p app_version=<assets\other\Version.txt
) else (
    set app_version=1.4.4
)
goto :eof

:: Function to check the latest GitHub version
:getGitHubVersion
for /f "delims=" %%i in ('curl -s "https://api.github.com/repos/MackNcD/DiceWords_App/releases/latest"') do (
    echo %%i | findstr "tag_name" > nul
    if not errorlevel 1 (
        for /f "tokens=2 delims=:, "" " %%a in ("%%i") do (
            set github_version=%%a
            goto version_found
        )
    )
)
:version_found
if not defined github_version (
    echo Unable to check GitHub version.
    set github_version=Unknown
)
goto :eof

:: Function to print a line
:printLine
echo +------------------------------------------------------------------------------+
goto :eof

:: Function to print centered text
:printCentered
set "text=%~1"
:: Get the length of the text
set "len=0"
for /l %%A in (12, -1, 0) do (
    set /a "len|=1<<%%A"
    for %%B in (!len!) do if "!text:~%%B,1!"=="" set /a "len&=~1<<%%A"
)
:: Calculate the padding
set /a "pad=(80 - len) / 2"
set "line="
for /l %%i in (1, 1, !pad!) do set "line= !line!"
:: Print the padded line
echo !line!!text!
goto :eof
