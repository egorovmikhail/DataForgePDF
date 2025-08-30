@echo off
REM Скрипт для пуша в оба репозитория: GitHub и GitVerse

echo 🚀 Отправка изменений в оба репозитория...

REM Проверяем статус
echo 📊 Статус Git:
git status --short

REM Добавляем все изменения
echo 📦 Добавление изменений...
git add .

REM Коммитим изменения (если есть)
git diff --cached --quiet
if %errorlevel% neq 0 (
    echo 💾 Создание коммита...
    for /f "tokens=1-6 delims=/: " %%a in ('date /t') do set mydate=%%c-%%b-%%a
    for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a%%b
    git commit -m "Обновления: %mydate% %mytime%"
) else (
    echo ✅ Нет изменений для коммита
)

REM Пушим в GitHub (origin)
echo 🌐 Отправка в GitHub...
git push origin main
if %errorlevel% equ 0 (
    echo ✅ GitHub: успешно отправлено
) else (
    echo ❌ GitHub: ошибка отправки
)

REM Пушим в GitVerse
echo 🌐 Отправка в GitVerse...
git push gitverse main
if %errorlevel% equ 0 (
    echo ✅ GitVerse: успешно отправлено
) else (
    echo ❌ GitVerse: ошибка отправки
)

echo 🎉 Отправка завершена!
echo.
echo 📊 Статус веток:
git branch -vv

pause
