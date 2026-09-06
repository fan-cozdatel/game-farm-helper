@echo off
chcp 65001 >nul
title Game Farm Helper
color 0B

echo Запуск Game Farm Helper...
echo.

:: Переход в папку со скриптом
cd /d "%~dp0"

:: Проверка прав администратора
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Требуются права администратора!
    echo [!] Перезапуск от имени администратора...
    timeout /t 2 >nul
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Проверка наличия файла
if not exist "game_farm_helper.py" (
    echo [X] Файл game_farm_helper.py не найден!
    echo [i] Убедитесь, что файл находится в папке:
    echo     %~dp0
    echo.
    pause
    exit /b 1
)

:: Проверка Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [X] Python не найден!
    echo [i] Запустите install.bat для установки
    pause
    exit /b 1
)

:: Запуск программы
echo [OK] Файл найден: %~dp0game_farm_helper.py
echo [OK] Запуск Python...
echo.

python "%~dp0game_farm_helper.py"

:: Если программа завершилась с ошибкой
if %errorLevel% neq 0 (
    echo.
    echo [!] Программа завершилась с ошибкой!
    echo [!] Код ошибки: %errorLevel%
    echo.
    echo Проверьте:
    echo 1. Установлен ли Python: python --version
    echo 2. Установлены ли библиотеки: pip list
    echo 3. Запустите install.bat если библиотеки не установлены
    echo.
    pause
)