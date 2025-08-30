#!/bin/bash
# DataForgePDF - Скрипт запуска для Linux/macOS

echo "🚀 DataForgePDF - Запуск для Linux/macOS"
echo "=================================================="

# Проверяем существование виртуального окружения
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено!"
    echo "Запустите сначала: python scripts/setup_venv.py"
    exit 1
fi

# Активируем виртуальное окружение
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Проверяем зависимости
echo "📦 Проверка зависимостей..."
python -c "import openpyxl, docx, weasyprint, jinja2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Отсутствуют зависимости!"
    echo "Установите зависимости: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Все зависимости установлены"
echo "🚀 Запуск основного скрипта..."
echo ""

# Запускаем основной скрипт
python src/main.py

# Деактивируем виртуальное окружение
deactivate
