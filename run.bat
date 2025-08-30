@echo off
REM DataForgePDF - Скрипт запуска для Windows

echo 🚀 DataForgePDF - Запуск для Windows
echo ==================================================

REM Проверяем существование виртуального окружения
if not exist "venv" (
    echo ❌ Виртуальное окружение не найдено!
    echo Запустите сначала: python scripts/setup_venv.py
    pause
    exit /b 1
)

REM Активируем виртуальное окружение
echo 🔧 Активация виртуального окружения...
call venv\Scripts\activate.bat

REM Проверяем зависимости
echo 📦 Проверка зависимостей...
python -c "import openpyxl, docx, weasyprint, jinja2" 2>nul
if errorlevel 1 (
    echo ❌ Отсутствуют зависимости!
    echo Установите зависимости: pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ Все зависимости установлены
echo 🚀 Запуск основного скрипта...
echo.

REM Запускаем основной скрипт
python src\main.py

REM Деактивируем виртуальное окружение
deactivate

pause
