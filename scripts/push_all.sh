#!/bin/bash
# Скрипт для пуша в оба репозитория: GitHub и GitVerse

echo "🚀 Отправка изменений в оба репозитория..."

# Проверяем статус
echo "📊 Статус Git:"
git status --short

# Добавляем все изменения
echo "📦 Добавление изменений..."
git add .

# Коммитим изменения (если есть)
if ! git diff --cached --quiet; then
    echo "💾 Создание коммита..."
    git commit -m "Обновления: $(date '+%Y-%m-%d %H:%M:%S')"
else
    echo "✅ Нет изменений для коммита"
fi

# Пушим в GitHub (origin)
echo "🌐 Отправка в GitHub..."
if git push origin main; then
    echo "✅ GitHub: успешно отправлено"
else
    echo "❌ GitHub: ошибка отправки"
fi

# Пушим в GitVerse
echo "🌐 Отправка в GitVerse..."
if git push gitverse main; then
    echo "✅ GitVerse: успешно отправлено"
else
    echo "❌ GitVerse: ошибка отправки"
fi

echo "🎉 Отправка завершена!"
echo ""
echo "📊 Статус веток:"
git branch -vv
