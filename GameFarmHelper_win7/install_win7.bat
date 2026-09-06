@echo off
title Установка Game Farm Helper для Windows 7
color 0A

echo ============================================
echo    УСТАНОВКА ДЛЯ WINDOWS 7
echo ============================================
echo.

:: Проверка версии Windows
ver | find "6.1" >nul
if %errorLevel% neq 0 (
    echo [!] Это не Windows 7!
    echo [!] Для Windows 10/11 используйте другую версию
    pause
    exit /b 1
)

echo [1/4] Проверка Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [X] Python не установлен!
    echo [i] Для Windows 7 нужен Python 3.8
    echo [i] Скачайте: https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe
    echo.
    start https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe
    pause
    exit /b 1
) else (
    echo [OK] Python найден
    python --version
)
echo.

echo [2/4] Установка библиотек...
echo.
echo Установка pywin32...
pip install pywin32 --quiet
if %errorLevel%==0 (echo [OK] pywin32 установлен) else (echo [FAILED] pywin32)

echo Установка wmi...
pip install wmi --quiet
if %errorLevel%==0 (echo [OK] wmi установлен) else (echo [FAILED] wmi)
echo.

echo [3/4] Загрузка NirCmd...
echo NirCmd нужен для надежного выключения монитора
echo.
echo Скачать NirCmd? (Y/N)
set /p choice="Ваш выбор: "
if /i "%choice%"=="Y" (
    echo Загрузка NirCmd...
    powershell -Command "Invoke-WebRequest -Uri 'http://www.nirsoft.net/utils/nircmd.zip' -OutFile 'nircmd.zip'"
    powershell -Command "Expand-Archive -Path 'nircmd.zip' -DestinationPath 'nircmd' -Force"
    copy "nircmd\nircmd.exe" "nircmd.exe" >nul 2>&1
    echo [OK] NirCmd загружен
) else (
    echo [i] NirCmd не загружен (программа будет работать без него)
)
echo.

echo [4/4] Проверка установки...
python -c "import win32gui; print('[OK] pywin32 работает')" 2>nul || echo "[X] Ошибка pywin32"
python -c "import wmi; print('[OK] wmi работает')" 2>nul || echo "[X] Ошибка wmi"

echo.
echo ============================================
echo    УСТАНОВКА ЗАВЕРШЕНА!
echo ============================================
echo.
echo Файлы:
echo - game_farm_helper_win7.py (основная программа)
echo - start_win7.bat (для запуска)
echo - nircmd.exe (если скачали)
echo.
pause