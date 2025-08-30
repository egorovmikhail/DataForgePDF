#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для настройки виртуального окружения DataForgePDF
"""

import os
import sys
import subprocess
import platform
import venv
from pathlib import Path


def run_command(command, shell=True):
    """Выполняет команду и возвращает результат"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def check_python_version():
    """Проверяет версию Python"""
    if sys.version_info < (3, 7):
        print("❌ Требуется Python 3.7 или выше")
        print(f"Текущая версия: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} обнаружен")
    return True


def create_virtual_environment():
    """Создает виртуальное окружение"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Виртуальное окружение уже существует")
        return True
    
    print("🔧 Создание виртуального окружения...")
    
    try:
        venv.create(venv_path, with_pip=True)
        print("✅ Виртуальное окружение создано")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания виртуального окружения: {e}")
        return False


def get_venv_python():
    """Возвращает путь к Python в виртуальном окружении"""
    system = platform.system().lower()
    
    if system == "windows":
        return "venv\\Scripts\\python.exe"
    else:
        return "venv/bin/python"


def get_venv_pip():
    """Возвращает путь к pip в виртуальном окружении"""
    system = platform.system().lower()
    
    if system == "windows":
        return "venv\\Scripts\\pip.exe"
    else:
        return "venv/bin/pip"


def install_dependencies():
    """Устанавливает зависимости"""
    pip_path = get_venv_pip()
    
    print("📦 Установка зависимостей...")
    
    # Обновляем pip
    success, stdout, stderr = run_command(f'"{pip_path}" install --upgrade pip')
    if not success:
        print(f"⚠️  Предупреждение: не удалось обновить pip: {stderr}")
    
    # Устанавливаем зависимости
    success, stdout, stderr = run_command(f'"{pip_path}" install -r requirements.txt')
    if success:
        print("✅ Зависимости установлены")
        return True
    else:
        print(f"❌ Ошибка установки зависимостей: {stderr}")
        return False


def install_system_dependencies():
    """Информирует о системных зависимостях"""
    system = platform.system().lower()
    
    print("\n📋 Системные зависимости:")
    
    if system == "darwin":  # macOS
        print("""
Для macOS установите следующие зависимости:
1. Homebrew (если не установлен):
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2. Системные библиотеки:
   brew install pango gdk-pixbuf libffi

3. Для WeasyPrint:
   brew install cairo pango gdk-pixbuf libffi
        """)
    
    elif system == "linux":
        print("""
Для Linux (Ubuntu/Debian) установите:
   sudo apt-get update
   sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

Для Linux (CentOS/RHEL/Fedora):
   sudo yum install redhat-rpm-config python3-devel python3-pip python3-setuptools python3-wheel python3-cffi libffi-devel cairo pango gdk-pixbuf2
        """)
    
    elif system == "windows":
        print("""
Для Windows:
1. Установите Microsoft Visual C++ Build Tools
2. Установите GTK+ для Windows (для WeasyPrint)
3. Или используйте WSL (Windows Subsystem for Linux)
        """)
    
    else:
        print(f"Система {system} не поддерживается")


def create_directories():
    """Создает необходимые директории"""
    directories = ["data", "output", "templates", "fonts"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Директория {directory} создана")


def download_fonts():
    """Скачивает шрифты Roboto"""
    fonts_dir = Path("fonts")
    fonts_dir.mkdir(exist_ok=True)
    
    print("🔤 Скачивание шрифтов Roboto...")
    
    # URL для шрифтов Roboto
    font_urls = {
        "Roboto-Regular.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Regular.ttf",
        "Roboto-Bold.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Bold.ttf"
    }
    
    for font_name, url in font_urls.items():
        font_path = fonts_dir / font_name
        if not font_path.exists():
            try:
                import urllib.request
                print(f"📥 Скачивание {font_name}...")
                urllib.request.urlretrieve(url, font_path)
                print(f"✅ {font_name} скачан")
            except Exception as e:
                print(f"⚠️  Не удалось скачать {font_name}: {e}")
                print(f"   Скачайте вручную с: {url}")
        else:
            print(f"✅ {font_name} уже существует")


def create_example_files():
    """Создает примеры файлов данных"""
    data_dir = Path("data")
    
    # Пример CSV файла
    csv_file = data_dir / "example.csv"
    if not csv_file.exists():
        csv_content = """Имя,Возраст,Город,Профессия
Иван Петров,25,Москва,Программист
Мария Сидорова,30,Санкт-Петербург,Дизайнер
Алексей Козлов,28,Казань,Менеджер
Анна Волкова,35,Новосибирск,Аналитик"""
        
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        print("✅ Пример CSV файла создан")
    
    # Пример JSON файла
    json_file = data_dir / "example.json"
    if not json_file.exists():
        json_content = """[
  {"имя": "Иван Петров", "возраст": 25, "город": "Москва", "профессия": "Программист"},
  {"имя": "Мария Сидорова", "возраст": 30, "город": "Санкт-Петербург", "профессия": "Дизайнер"},
  {"имя": "Алексей Козлов", "возраст": 28, "город": "Казань", "профессия": "Менеджер"}
]"""
        
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write(json_content)
        print("✅ Пример JSON файла создан")
    
    # Пример TXT файла
    txt_file = data_dir / "example.txt"
    if not txt_file.exists():
        txt_content = """Иван Петров\t25\tМосква\tПрограммист
Мария Сидорова\t30\tСанкт-Петербург\tДизайнер
Алексей Козлов\t28\tКазань\tМенеджер
Анна Волкова\t35\tНовосибирск\tАналитик"""
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        print("✅ Пример TXT файла создан")


def main():
    """Основная функция настройки"""
    print("🚀 Настройка DataForgePDF")
    print("=" * 50)
    
    # Проверяем версию Python
    if not check_python_version():
        sys.exit(1)
    
    # Создаем директории
    create_directories()
    
    # Создаем виртуальное окружение
    if not create_virtual_environment():
        sys.exit(1)
    
    # Устанавливаем зависимости
    if not install_dependencies():
        print("\n⚠️  Попробуйте установить зависимости вручную:")
        print("   source venv/bin/activate  # для Linux/macOS")
        print("   venv\\Scripts\\activate     # для Windows")
        print("   pip install -r requirements.txt")
    
    # Скачиваем шрифты
    download_fonts()
    
    # Создаем примеры файлов
    create_example_files()
    
    # Информируем о системных зависимостях
    install_system_dependencies()
    
    print("\n🎉 Настройка завершена!")
    print("\n📖 Для запуска:")
    print("   source venv/bin/activate  # для Linux/macOS")
    print("   venv\\Scripts\\activate     # для Windows")
    print("   python src/main.py")
    
    print("\n📁 Структура проекта:")
    print("   data/          - файлы данных")
    print("   output/        - сгенерированные PDF")
    print("   templates/     - HTML шаблоны")
    print("   fonts/         - шрифты")
    print("   src/main.py    - основной скрипт")


if __name__ == "__main__":
    main()
