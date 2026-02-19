#!/usr/bin/env python3
"""
Генератор RSS для Яндекс Дзен - соответствует официальным требованиям
https://dzen.ru/help/ru/website/rss-modify.html
"""

import json
import re
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

def markdown_to_html(text, site_url, cover_url):
    """
    Конвертация Markdown в HTML для Дзена
    Только разрешённые теги: h1-h4, p, br, strong, em, a, img, figure, ul, li
    """
    if not text:
        return ""
    
    lines = text.split('\n')
    html_lines = []
    in_ul = False
    
    for line in lines:
        line = line.rstrip()
        
        # Заголовки
        if line.startswith('# '):
            if in_ul:
                html_lines.append('</ul>')
                in_ul = False
            html_lines.append(f'<h1>{escape_xml(line[2:])}</h1>')
        elif line.startswith('## '):
            if in_ul:
                html_lines.append('</ul>')
                in_ul = False
            html_lines.append(f'<h2>{escape_xml(line[3:])}</h2>')
        elif line.startswith('### '):
            if in_ul:
                html_lines.append('</ul>')
                in_ul = False
            html_lines.append(f'<h3>{escape_xml(line[4:])}</h3>')
        # Списки
        elif line.startswith('• ') or line.startswith('- ') or line.startswith('* '):
            if not in_ul:
                html_lines.append('<ul>')
                in_ul = True
            content = line[2:].strip()
            # bold внутри
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', escape_xml(content))
            html_lines.append(f'<li>{content}</li>')
        # Разделители
        elif line.startswith('---') or line.startswith('━━━'):
            if in_ul:
                html_lines.append('</ul>')
                in_ul = False
            html_lines.append('<br/>')
        # Пустая строка
        elif line == '':
            if in_ul:
                html_lines.append('</ul>')
                in_ul = False
        # Обычный текст
        else:
            if in_ul:
                html_lines.append('</ul>')
                in_ul = False
            content = escape_xml(line)
            # Bold
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            # Italic
            content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
            html_lines.append(f'<p>{content}</p>')
    
    if in_ul:
        html_lines.append('</ul>')
    
    return '\n'.join(html_lines)

def generate_rss(articles_dir="public/articles", output_file="public/rss.xml", site_url="https://dzen-auto.vercel.app"):
    """
    Генерировать RSS ленту под требования Яндекс.Дзен
    """
    
    # Читаем статьи
    articles = []
    for json_file in Path(articles_dir).glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            articles.append(json.load(f))
    
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    print(f"📚 Найдено статей: {len(articles)}")
    
    rss_items = []
    
    for article in articles[:20]:
        date = datetime.fromisoformat(article['date'])
        pub_date = date.strftime('%a, %d %b %Y %H:%M:%S +0000')
        
        # URL материала (ЧПУ без UTM-меток)
        article_url = f"{site_url}/articles/{article['slug']}"
        
        # Обложка (enclosure обязателен, минимум 700px)
        cover_url = f"{site_url}/cover.jpg"
        
        # Конвертируем контент в HTML (Дзен не принимает Markdown)
        html_content = markdown_to_html(article['content'], site_url, cover_url)
        
        # Формируем полный HTML с заголовком (обязательно!)
        full_html = f"""<h1>{escape_xml(article['title'])}</h1>

<figure>
<img src="{cover_url}" alt="{escape_xml(article['title'])}" width="1200" height="800"/>
</figure>

{html_content}"""
        
        # Категории для Дзена (обязательные!)
        item = f"""
    <item>
      <title>{escape_xml(article['title'])}</title>
      <link>{article_url}</link>
      <description>{escape_xml(article['description'])}</description>
      <pubDate>{pub_date}</pubDate>
      <guid isPermaLink="true">{article_url}</guid>

      <!-- Тип публикации -->
      <category>format-article</category>
      <!-- Индексация -->
      <category>index</category>
      <!-- Комментарии -->
      <category>comment-all</category>

      <!-- Обложка (минимум 700px) -->
      <enclosure url="{cover_url}" type="image/jpeg" length="150000"/>

      <!-- Полный HTML-контент -->
      <content:encoded><![CDATA[{full_html}]]></content:encoded>
    </item>"""
        
        rss_items.append(item)
    
    # Итоговый RSS
    last_build_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    
    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>Crypto Digest — Ежедневные крипто-дайджесты</title>
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
    
    print(f"✅ RSS создан: {output_file}")
    print(f"📊 Статей в ленте: {len(articles)}")
    print(f"🔗 RSS URL: {site_url}/rss.xml")

def main():
    workspace = Path("/root/.openclaw/workspace/dzen-auto")
    
    generate_rss(
        articles_dir=str(workspace / "public" / "articles"),
        output_file=str(workspace / "public" / "rss.xml"),
        site_url="https://dzen-auto.vercel.app"
    )

if __name__ == "__main__":
    main()
