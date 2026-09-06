@echo off
title Game Farm Helper Win7
color 0B

echo Запуск Game Farm Helper для Windows 7...
echo.

:: Переход в папку со скриптом
cd /d "%~dp0"

:: Проверка наличия файла
if not exist "game_farm_helper_win7.py" (
    echo [X] Файл game_farm_helper_win7.py не найден!
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
    echo [i] Установите Python 3.8 для Windows 7
    echo [i] https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe
    pause
    exit /b 1
)

:: Запуск программы
echo [OK] Запуск Python...
echo.

python "%~dp0game_farm_helper_win7.py"

:: Если программа завершилась с ошибкой
if %errorLevel% neq 0 (
    echo.
    echo [!] Программа завершилась с ошибкой!
    echo.
    pause
)