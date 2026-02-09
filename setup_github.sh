#!/bin/bash
# Быстрая настройка GitHub Pages

set -e

echo "🚀 Настройка GitHub Pages для Яндекс.Дзен"
echo "=========================================="
echo ""

# Проверка GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "⚠️ GitHub CLI не установлен"
    echo ""
    echo "Варианты:"
    echo "1. Установить: apt install gh"
    echo "2. Или следуйте инструкциям в GITHUB_PAGES_SETUP.md"
    exit 1
fi

# Проверка авторизации
if ! gh auth status &> /dev/null; then
    echo "🔑 Требуется авторизация в GitHub"
    gh auth login
fi

echo ""
read -p "📝 Введите название репозитория (например: crypto-dzen): " REPO_NAME

if [ -z "$REPO_NAME" ]; then
    echo "❌ Название репозитория не может быть пустым"
    exit 1
fi

echo ""
echo "📦 Создание репозитория $REPO_NAME..."

cd /root/.openclaw/workspace/dzen-auto

# Инициализация git
if [ ! -d .git ]; then
    git init
    git config user.email "bot@openclaw.ai"
    git config user.name "OpenClaw Bot"
fi

# Добавить все файлы
git add -A
git commit -m "Initial commit for GitHub Pages" || true

# Создать репозиторий и запушить
gh repo create "$REPO_NAME" --public --source=. --push --description="Crypto digest RSS for Yandex.Zen"

if [ $? -ne 0 ]; then
    echo "❌ Ошибка создания репозитория"
    exit 1
fi

echo ""
echo "✅ Репозиторий создан!"

# Получить username
USERNAME=$(gh api user -q .login)

echo ""
echo "🌐 Ваш сайт будет доступен на:"
echo "   https://$USERNAME.github.io/$REPO_NAME/"
echo ""
echo "📡 RSS лента:"
echo "   https://$USERNAME.github.io/$REPO_NAME/rss.xml"
echo ""

# Обновить URL в скриптах
echo "🔧 Обновление URL в скриптах..."

SITE_URL="https://$USERNAME.github.io/$REPO_NAME"

# Обновить generate_rss_simple.py
sed -i "s|site_url=\".*\"|site_url=\"$SITE_URL\"|g" generate_rss_simple.py

# Обновить index.html
sed -i "s|https://.*\.vercel\.app|$SITE_URL|g" public/index.html

# Перегенерировать RSS
python3 generate_rss_simple.py

# Закоммитить изменения
git add -A
git commit -m "Update URLs to GitHub Pages"
git push

echo ""
echo "=========================================="
echo "✅ НАСТРОЙКА ЗАВЕРШЕНА!"
echo "=========================================="
echo ""
echo "📋 Следующие шаги:"
echo ""
echo "1. Включить GitHub Pages:"
echo "   - Зайдите в Settings → Pages"
echo "   - Source: GitHub Actions"
echo "   - Сохраните"
echo ""
echo "2. Дождитесь деплоя (~2 минуты)"
echo "   - Вкладка Actions покажет прогресс"
echo ""
echo "3. Добавьте RSS в Яндекс.Дзен:"
echo "   $SITE_URL/rss.xml"
echo ""
echo "🎉 Готово!"
