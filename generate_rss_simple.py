#!/usr/bin/env python3
"""
Генератор RSS для Яндекс Дзен - строго по официальным требованиям
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
        .replace('"', '&quot;'))

def markdown_to_html(text):
    """
    Конвертация Markdown в HTML.
    Только разрешённые Дзеном теги:
    p, a, b, i, u, s, h1-h4, blockquote, ul/li, ol/li, figure, img
    """
    if not text:
        return ""

    lines = text.split('\n')
    html_lines = []
    in_ul = False
    skip_first_h1 = True  # Пропускаем первый h1 — он уже добавлен в enclosure/заголовок

    for line in lines:
        line = line.rstrip()

        # Заголовки
        if line.startswith('# '):
            if in_ul:
                html_lines.append('</ul>')
                in_ul = False
            if skip_first_h1:
                skip_first_h1 = False
                continue  # Пропускаем первый h1 (он уже есть выше)
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

        # Маркированные списки (внутри списка форматирование не поддерживается по Дзену)
        elif line.startswith('• ') or line.startswith('- ') or line.startswith('* '):
            if not in_ul:
                html_lines.append('<ul>')
                in_ul = True
            # Убираем markdown-разметку, оставляем чистый текст
            content = line[2:].strip()
            content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)  # убираем bold
            content = re.sub(r'\*(.+?)\*', r'\1', content)        # убираем italic
            content = escape_xml(content)
            html_lines.append(f'<li>{content}</li>')

        # Разделители
        elif line.startswith('---') or line.startswith('━━━'):
            if in_ul:
                html_lines.append('</ul>')
                in_ul = False

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
            # Bold **text**
            content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', content)
            # Italic *text*
            content = re.sub(r'\*(.+?)\*', r'<i>\1</i>', content)
            html_lines.append(f'<p>{content}</p>')

    if in_ul:
        html_lines.append('</ul>')

    return '\n'.join(html_lines)


def generate_rss(articles_dir="public/articles", output_file="public/rss.xml", site_url="https://dzen-auto.vercel.app"):
    """
    Генерировать RSS ленту по официальным требованиям Яндекс.Дзен
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
        pub_date = date.strftime('%a, %d %b %Y %H:%M:%S +0300')

        # ЧПУ URL без UTM-меток
        article_url = f"{site_url}/articles/{article['slug']}"

        # Обложка — минимум 700px, без length (не обязателен)
        cover_url = f"{site_url}/cover.jpg"

        # HTML контент (не Markdown!)
        html_body = markdown_to_html(article['content'])

        # Полный content:encoded строго по примеру из документации
        full_content = f"""<p>{escape_xml(article['description'])}</p>

<figure>
<img src="{cover_url}">
<figcaption>Криптовалютный дайджест</figcaption>
</figure>

{html_body}"""

        item = f"""
    <item>
      <title>{escape_xml(article['title'])}</title>
      <link>{article_url}</link>
      <description>{escape_xml(article['description'])}</description>
      <pubDate>{pub_date}</pubDate>
      <guid>{article_url}</guid>
      <category>format-article</category>
      <category>index</category>
      <category>comment-all</category>
      <enclosure url="{cover_url}" type="image/jpeg"/>
      <content:encoded><![CDATA[{full_content}]]></content:encoded>
    </item>"""

        rss_items.append(item)

    last_build_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0300')

    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:media="http://search.yahoo.com/mrss/"
  xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:georss="http://www.georss.org/georss">
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
