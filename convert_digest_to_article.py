#!/usr/bin/env python3
"""
Конвертация Telegram дайджеста в статью для Яндекс Дзен
"""

import json
import re
from datetime import datetime
from pathlib import Path

def digest_to_article(digest_text, date=None):
    """
    Конвертировать дайджест в формат статьи для Дзен
    """
    if date is None:
        date = datetime.now()
    
    # Парсим дайджест
    lines = digest_text.strip().split('\n')
    
    # Генерируем заголовок
    date_ru = date.strftime("%d %B %Y")
    months = {
        "January": "января", "February": "февраля", "March": "марта",
        "April": "апреля", "May": "мая", "June": "июня",
        "July": "июля", "August": "августа", "September": "сентября",
        "October": "октября", "November": "ноября", "December": "декабря"
    }
    for en, ru in months.items():
        date_ru = date_ru.replace(en, ru)
    
    title = f"Криптовалютный дайджест за {date_ru}"
    
    # Генерируем описание (первые 150 символов контента)
    description = "Главные события крипторынка: биткоин, альткоины, сигналы трейдеров и on-chain аналитика"
    
    # Форматируем контент для Дзен
    article_content = f"""# {title}

{digest_text}

---

## 📌 О дайджесте

Ежедневная сводка главных событий криптовалютного рынка. Материал основан на агрегации данных из ведущих крипто-каналов с общим охватом более 270 тысяч участников.

### Категории:
- **🔴 Рынок** — движение цен, анализ трендов
- **📈 Сигналы** — торговые идеи и уровни
- **⛓️ On-Chain** — анализ блокчейн-данных
- **⚡️ Новости** — важные события индустрии
- **💡 Анализ** — экспертные мнения и прогнозы

### Подпишитесь
Чтобы получать ежедневные обновления, подпишитесь на наш канал!

---

*Дисклеймер: данный материал носит информационный характер и не является инвестиционной рекомендацией. Всегда проводите собственное исследование перед принятием финансовых решений.*
"""
    
    # Создаем метаданные
    article = {
        "title": title,
        "description": description,
        "content": article_content,
        "date": date.isoformat(),
        "slug": f"crypto-digest-{date.strftime('%Y-%m-%d')}",
        "tags": ["криптовалюта", "биткоин", "блокчейн", "трейдинг", "крипторынок"],
        "image": f"/images/crypto-{date.strftime('%Y%m%d')}.jpg",
        "author": "Crypto Digest",
        "category": "Криптовалюты"
    }
    
    return article

def save_article(article, output_dir="public/articles"):
    """
    Сохранить статью в JSON и Markdown
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    slug = article['slug']
    
    # JSON
    json_path = f"{output_dir}/{slug}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    
    # Markdown (для Next.js)
    md_path = f"{output_dir}/{slug}.md"
    frontmatter = f"""---
title: "{article['title']}"
description: "{article['description']}"
date: "{article['date']}"
image: "{article['image']}"
tags: {json.dumps(article['tags'])}
author: "{article['author']}"
category: "{article['category']}"
---

{article['content']}
"""
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
    
    print(f"✅ Статья сохранена:")
    print(f"   JSON: {json_path}")
    print(f"   MD: {md_path}")
    
    return article

def main():
    """
    Конвертировать последний дайджест
    """
    # Ищем последний дайджест
    workspace = Path("/root/.openclaw/workspace")
    digest_files = sorted(workspace.glob("digest_*.txt"), reverse=True)
    
    if not digest_files:
        print("❌ Нет дайджестов для конвертации")
        return
    
    latest_digest = digest_files[0]
    print(f"📄 Используем дайджест: {latest_digest.name}")
    
    # Читаем
    with open(latest_digest, 'r', encoding='utf-8') as f:
        digest_text = f.read()
    
    # Извлекаем дату из имени файла
    match = re.search(r'digest_(\d{8})_', latest_digest.name)
    if match:
        date_str = match.group(1)
        date = datetime.strptime(date_str, '%Y%m%d')
    else:
        date = datetime.now()
    
    # Конвертируем
    print("\n🔄 Конвертация в статью для Дзен...")
    article = digest_to_article(digest_text, date)
    
    # Сохраняем
    output_dir = workspace / "dzen-auto" / "public" / "articles"
    save_article(article, str(output_dir))
    
    print(f"\n✅ Готово! Статья готова к публикации")
    print(f"📝 Заголовок: {article['title']}")
    print(f"🔗 Slug: {article['slug']}")

if __name__ == "__main__":
    main()
