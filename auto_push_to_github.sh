#!/bin/bash
# Автоматический push в GitHub после генерации контента

set -e

cd /root/.openclaw/workspace/dzen-auto

echo "📝 Добавление изменений..."
git add public/articles/ public/rss.xml public/index.html

echo "💾 Коммит..."
git commit -m "Auto update: $(date '+%Y-%m-%d %H:%M')" || echo "Нет изменений"

echo "📤 Push в GitHub..."
git push origin main

echo "✅ Готово! GitHub Pages автоматически обновится."
