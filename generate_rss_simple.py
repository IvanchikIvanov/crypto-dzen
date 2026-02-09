#!/usr/bin/env python3
"""
Простой генератор RSS для Яндекс Дзен
"""

import json
from datetime import datetime
from pathlib import Path

def escape_xml(text):
    """Экранировать спецсимволы XML"""
    if not text:
        return ""
    return (text
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&apos;'))

def generate_rss(articles_dir="public/articles", output_file="public/rss.xml", site_url="https://crypto-dzen.vercel.app"):
    """
    Генерировать RSS ленту
    """
    
    # Читаем статьи
    articles = []
    for json_file in Path(articles_dir).glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            articles.append(json.load(f))
    
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # Генерируем RSS вручную (без XML библиотек)
    rss_items = []
    
    for article in articles[:20]:
        date = datetime.fromisoformat(article['date'])
        pub_date = date.strftime('%a, %d %b %Y %H:%M:%S +0000')
        
        item = f"""
    <item>
      <title>{escape_xml(article['title'])}</title>
      <link>{site_url}/{article['slug']}</link>
      <description>{escape_xml(article['description'])}</description>
      <pubDate>{pub_date}</pubDate>
      <guid>{site_url}/{article['slug']}</guid>
      <category>{escape_xml(article.get('category', 'Криптовалюты'))}</category>
      <content:encoded><![CDATA[{article['content']}]]></content:encoded>
    </item>"""
        
        rss_items.append(item)
    
    # Собираем полный RSS
    last_build_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    
    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>Crypto Digest - Ежедневные крипто-дайджесты</title>
    <link>{site_url}</link>
    <description>Ежедневная сводка главных событий криптовалютного рынка. Агрегация данных из ведущих крипто-каналов.</description>
    <language>ru</language>
    <lastBuildDate>{last_build_date}</lastBuildDate>
{''.join(rss_items)}
  </channel>
</rss>"""
    
    # Сохраняем
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rss_xml)
    
    print(f"✅ RSS лента создана: {output_file}")
    print(f"📊 Статей: {len(articles)}")
    print(f"🔗 URL: {site_url}/rss.xml")
    
    return rss_xml

def main():
    workspace = Path("/root/.openclaw/workspace/dzen-auto")
    
    articles_dir = workspace / "public" / "articles"
    output_file = workspace / "public" / "rss.xml"
    
    generate_rss(
        articles_dir=str(articles_dir),
        output_file=str(output_file),
        site_url="https://ivanchikivanov.github.io/crypto-dzen"
    )

if __name__ == "__main__":
    main()
