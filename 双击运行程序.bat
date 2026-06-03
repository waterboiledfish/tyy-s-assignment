@echo off
title Media Insight Platform

echo Starting Media Insight Platform...
echo.

set PY_CMD=

python --version >nul 2>nul
if not errorlevel 1 (
    set PY_CMD=python
) else (
    py --version >nul 2>nul
    if not errorlevel 1 (
        set PY_CMD=py
    )
)

if "%PY_CMD%"=="" (
    echo Python was not found.
    echo Please install Python 3.10 or later first.
    echo Download: https://www.python.org/downloads/
    echo Important: check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Using Python command: %PY_CMD%
echo Checking required packages...

%PY_CMD% -c "import matplotlib, openpyxl" >nul 2>nul
if errorlevel 1 (
    echo Installing required packages. Please wait...
    %PY_CMD% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo Package installation failed.
        echo Try this manually:
        echo %PY_CMD% -m pip install matplotlib openpyxl
        echo.
        pause
        exit /b 1
    )
)

echo Opening program...
echo.
%PY_CMD% media_insight_platform.py

echo.
echo Program closed.
pause
