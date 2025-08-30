# 🚀 Быстрый старт DataForgePDF

## ⚡ За 5 минут

### 1. Настройка (одноразово)
```bash
# Запустите скрипт настройки
python scripts/setup_venv.py
```

### 2. Запуск
```bash
# Linux/macOS
./run.sh

# Windows
run.bat

# Или универсально
python run.py
```

### 3. Выберите файл данных
- CSV, JSON, Excel, Word или TXT
- Следуйте инструкциям в консоли
- PDF автоматически откроется

## 📁 Структура проекта

```
DataForgePDF/
├── data/           # 📊 Ваши файлы данных
├── output/         # 📄 Сгенерированные PDF
├── templates/      # 🎨 HTML шаблоны
├── fonts/          # 🔤 Шрифты Roboto
├── src/main.py     # 🐍 Основной скрипт
└── run.sh/run.bat  # 🚀 Скрипты запуска
```

## 📊 Поддерживаемые форматы

| Формат | Расширение | Описание |
|--------|------------|----------|
| CSV    | .csv       | Разделитель: запятая |
| JSON   | .json      | Массив объектов/массивов |
| Excel  | .xlsx/.xls | Первый лист, заголовки в первой строке |
| Word   | .docx/.doc | Абзацы = строки, табуляция = колонки |
| TXT    | .txt       | Настраиваемый разделитель |

## 🎯 Примеры использования

### CSV файл
```csv
Имя,Возраст,Город
Иван,25,Москва
Мария,30,СПб
```

### JSON файл
```json
[
  {"имя": "Иван", "возраст": 25, "город": "Москва"},
  {"имя": "Мария", "возраст": 30, "город": "СПб"}
]
```

## 🔧 Устранение проблем

### Ошибка "ModuleNotFoundError"
```bash
# Активируйте виртуальное окружение
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Установите зависимости
pip install -r requirements.txt
```

### Проблемы с WeasyPrint
**macOS:**
```bash
brew install cairo pango gdk-pixbuf libffi
```

**Linux:**
```bash
sudo apt-get install libcairo2 libpango-1.0-0
```

## 📖 Подробная документация

См. [README.md](README.md) для полной документации.

---

**🎉 Готово! Теперь вы можете создавать красивые PDF из ваших данных!**
