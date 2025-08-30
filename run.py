#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Универсальный скрипт запуска DataForgePDF
Автоматически определяет ОС и активирует виртуальное окружение
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


def get_venv_python():
    """Возвращает путь к Python в виртуальном окружении"""
    system = platform.system().lower()
    
    if system == "windows":
        return "venv\\Scripts\\python.exe"
    else:
        return "venv/bin/python"


def check_venv():
    """Проверяет существование виртуального окружения"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Виртуальное окружение не найдено!")
        print("Запустите сначала: python scripts/setup_venv.py")
        return False
    return True


def check_dependencies():
    """Проверяет установленные зависимости"""
    try:
        import openpyxl
        import docx
        import weasyprint
        import jinja2
        return True
    except ImportError as e:
        print(f"❌ Отсутствуют зависимости: {e}")
        print("Установите зависимости: pip install -r requirements.txt")
        return False


def run_main():
    """Запускает основной скрипт"""
    main_script = Path("src/main.py")
    if not main_script.exists():
        print("❌ Основной скрипт не найден: src/main.py")
        return False
    
    try:
        # Запускаем основной скрипт
        subprocess.run([sys.executable, str(main_script)], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
        return True


def main():
    """Основная функция"""
    print("🚀 DataForgePDF - Универсальный запуск")
    print("=" * 50)
    
    # Проверяем виртуальное окружение
    if not check_venv():
        return 1
    
    # Проверяем зависимости
    if not check_dependencies():
        return 1
    
    # Запускаем основной скрипт
    if run_main():
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
