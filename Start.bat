@echo off
setlocal enabledelayedexpansion

:: Customize the appearance of the command line
color 0B

:: Attempt to resize the command prompt window to 80 columns and 25 lines
mode con: cols=80 lines=25

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
call :printCentered "3. Join Discord"
call :printCentered "4. Go to GitHub"
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
pip install -r requirements.txt > assets\logs\install_log.txt 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :printCentered "Failed to install requirements. Check 'assets\logs\install_log.txt' for details."
    pause
    goto menu
)
call :printCentered "Dependencies installed successfully. See 'assets\logs\install_log.txt' for details."
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
call :printCentered "Are you sure you want to exit? (Y/N)"
set /p confirm=
if /i "!confirm!"=="Y" goto end
call :printCentered "Returning to menu..."
goto menu

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
if exist assets\logs\Version.txt (
    set /p app_version=<assets\logs\Version.txt
) else (
    set app_version=Unknown
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
