@echo off
chcp 65001 >nul
title Установка Game Farm Helper
color 0A

echo ============================================
echo    УСТАНОВКА GAME FARM HELPER
echo ============================================
echo.

:: Проверка прав администратора
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Требуются права администратора!
    echo [!] Перезапустите файл от имени администратора
    echo.
    pause
    exit /b 1
)

echo [1/4] Проверка Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [X] Python не установлен!
    echo [i] Скачайте Python с https://www.python.org/downloads/
    echo [i] При установке отметьте "Add Python to PATH"
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    echo [OK] Python найден
    python --version
)
echo.

echo [2/4] Обновление pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip обновлен
echo.

echo [3/4] Установка Python библиотек...
echo Это может занять несколько минут...
echo.

echo Установка pywin32...
pip install pywin32 --quiet
if %errorLevel%==0 (echo [OK] pywin32 установлен) else (echo [FAILED] pywin32)

echo Установка psutil...
pip install psutil --quiet
if %errorLevel%==0 (echo [OK] psutil установлен) else (echo [FAILED] psutil)

echo Установка wmi...
pip install wmi --quiet
if %errorLevel%==0 (echo [OK] wmi установлен) else (echo [FAILED] wmi)

echo Установка pyautogui...
pip install pyautogui --quiet
if %errorLevel%==0 (echo [OK] pyautogui установлен) else (echo [FAILED] pyautogui)

echo Установка keyboard...
pip install keyboard --quiet
if %errorLevel%==0 (echo [OK] keyboard установлен) else (echo [FAILED] keyboard)

echo Установка mouse...
pip install mouse --quiet
if %errorLevel%==0 (echo [OK] mouse установлен) else (echo [FAILED] mouse)

echo.
echo [4/4] Проверка установки...
python -c "import win32gui; print('[OK] pywin32 работает')" 2>nul || echo "[X] Ошибка pywin32"
python -c "import psutil; print('[OK] psutil работает')" 2>nul || echo "[X] Ошибка psutil"
python -c "import wmi; print('[OK] wmi работает')" 2>nul || echo "[X] Ошибка wmi"

echo.
echo ============================================
echo    УСТАНОВКА ЗАВЕРШЕНА!
echo ============================================
echo.
echo Дополнительно установите вручную:
echo.
echo 1. MSI Afterburner (для вентиляторов):
echo    https://www.msi.com/Landing/afterburner/graphics-cards
echo.
echo 2. ПО для вашей клавиатуры:
echo    - Logitech: https://www.logitechg.com/en-us/innovation/g-hub.html
echo    - Razer: https://www.razer.com/synapse-3
echo    - Corsair: https://www.corsair.com/us/en/icue
echo    - OpenRGB (универсальное): https://openrgb.org/
echo.
echo Хотите открыть страницы загрузки? (Y/N)
set /p choice="Ваш выбор: "
if /i "%choice%"=="Y" (
    start https://www.msi.com/Landing/afterburner/graphics-cards
    timeout /t 2 >nul
    start https://openrgb.org/
)

echo.
echo Нажмите любую клавишу для выхода...
pause >nul