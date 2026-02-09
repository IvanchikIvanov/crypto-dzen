#!/bin/bash
# Автоматическое обновление контента и деплой на Vercel

set -e

WORKSPACE="/root/.openclaw/workspace/dzen-auto"
LOG_FILE="$WORKSPACE/auto_deploy.log"

echo "========================================" >> "$LOG_FILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') - Запуск автообновления" >> "$LOG_FILE"

cd "$WORKSPACE"

# 1. Конвертировать последний дайджест в статью
echo "📝 Конвертация дайджеста..." >> "$LOG_FILE"
python3 convert_digest_to_article.py >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Ошибка конвертации" >> "$LOG_FILE"
    exit 1
fi

# 2. Сгенерировать RSS
echo "📡 Генерация RSS..." >> "$LOG_FILE"
python3 generate_rss_simple.py >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Ошибка генерации RSS" >> "$LOG_FILE"
    exit 1
fi

# 3. Деплой на Vercel
echo "🚀 Деплой на Vercel..." >> "$LOG_FILE"

# Используем Vercel CLI для деплоя
# Предполагается, что vercel уже залогинен
cd "$WORKSPACE"
vercel --prod --yes >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Успешно задеплоено на Vercel" >> "$LOG_FILE"
else
    echo "⚠️ Vercel CLI недоступен или ошибка деплоя" >> "$LOG_FILE"
    echo "💡 Файлы обновлены локально, запустите 'vercel --prod' вручную" >> "$LOG_FILE"
fi

echo "✅ Готово!" >> "$LOG_FILE"
echo "📊 RSS обновлен: https://dzen-auto-a4jrr0g9m-ivanchikivanovs-projects.vercel.app/rss.xml" >> "$LOG_FILE"
