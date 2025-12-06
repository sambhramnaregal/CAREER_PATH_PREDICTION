@echo off
echo Starting Backend Server...
REM Ensure we are in the correct directory
cd /d "%~dp0"
REM Run using the virtual environment python
.\venv\Scripts\python.exe app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Application exited with error code %ERRORLEVEL%.
    pause
)
