@echo off
title Open MySQL Manager
cd /d "%~dp0"
python app.py
if errorlevel 1 (
    echo.
    echo [ERROR] Khong the khoi chay app.py
    pause
)

