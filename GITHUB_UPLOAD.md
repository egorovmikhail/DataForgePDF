# 🚀 Загрузка DataForgePDF на GitHub

## 📋 Пошаговая инструкция

### 1. Создание репозитория на GitHub

1. **Перейдите на [github.com](https://github.com)**
2. **Нажмите кнопку "New repository"** (зеленый плюс в правом верхнем углу)
3. **Заполните форму:**
   - **Repository name**: `DataForgePDF`
   - **Description**: `Генератор PDF документов с полной поддержкой кириллицы для Windows, macOS и Linux`
   - **Visibility**: `Public` ✅
   - **НЕ ставьте галочки** на:
     - [ ] Add a README file
     - [ ] Add .gitignore  
     - [ ] Choose a license
4. **Нажмите "Create repository"**

### 2. Копирование URL репозитория

После создания репозитория GitHub покажет страницу с командами. **Скопируйте URL репозитория** - он будет выглядеть как:
```
https://github.com/ваш-username/DataForgePDF.git
```

### 3. Выполнение команд в терминале

**Замените `YOUR_USERNAME` на ваше имя пользователя GitHub** и выполните команды:

```bash
# Добавляем remote origin
git remote add origin https://github.com/YOUR_USERNAME/DataForgePDF.git

# Переименовываем основную ветку в main (современный стандарт)
git branch -M main

# Отправляем код на GitHub
git push -u origin main
```

### 4. Проверка результата

После успешной загрузки:
- Перейдите на страницу вашего репозитория
- Убедитесь, что все файлы загружены
- Проверьте, что README.md отображается корректно

## 🔧 Альтернативные команды

Если у вас настроен SSH ключ:

```bash
git remote add origin git@github.com:YOUR_USERNAME/DataForgePDF.git
git branch -M main
git push -u origin main
```

## 📁 Что будет загружено

- ✅ **Основной код**: `src/main.py`
- ✅ **Документация**: `README.md`, `CHANGELOG.md`, `USAGE_EXAMPLES.md`
- ✅ **Шрифты**: DejaVu Sans, Arial Unicode MS, Roboto
- ✅ **Шаблоны**: HTML шаблон для PDF
- ✅ **Примеры данных**: CSV, JSON, TXT файлы
- ✅ **Скрипты**: настройка, запуск для разных ОС
- ✅ **Конфигурация**: requirements.txt, setup.py

## 🎯 После загрузки

1. **Добавьте описание** в About секцию репозитория
2. **Настройте теги** (Topics): `pdf`, `cyrillic`, `russian`, `python`, `weasyprint`, `reportlab`
3. **Создайте Issues** для планирования будущих улучшений
4. **Настройте GitHub Pages** если планируете документацию

## 🆘 Если возникли проблемы

- **Ошибка аутентификации**: настройте Personal Access Token или SSH ключ
- **Файлы не загружаются**: проверьте размер файлов (шрифты могут быть большими)
- **Конфликт веток**: используйте `git pull origin main --allow-unrelated-histories`

---

**Удачи с загрузкой! 🚀✨**
