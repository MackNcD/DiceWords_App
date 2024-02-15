@echo off

if not defined PYTHON (set PYTHON=python)
if not defined VENV_DIR (set "VENV_DIR=%~dp0%.venv")
set ERROR_REPORTING=FALSE
mkdir tmp 2>NUL

:start_venv

:activate_venv
set PYTHON="%VENV_DIR%\Scripts\Python.exe"
echo Using VENV: %VENV_DIR%

:launch
%PYTHON% DiceWords_App.py %*
pause
exit /b