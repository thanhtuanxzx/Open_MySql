@echo off
title Build MySQL Manager EXE
cd /d "%~dp0"
echo ============================================
echo Dang dong goi Open MySQL sang file .exe...
echo ============================================
python -m PyInstaller ^
    --noconsole ^
    --onefile ^
    --name=MySQL_Manager ^
    --icon="%~dp0logo.ico" ^
    --collect-all ttkbootstrap ^
    --distpath . ^
    --workpath build ^
    --clean ^
    -y ^
    app.py

if errorlevel 1 (
    echo.
    echo [ERROR] Dong goi that bai!
    pause
    exit /b 1
)

echo.
echo ============================================
echo Dong goi thanh cong: MySQL_Manager.exe
echo ============================================
pause
