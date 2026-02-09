#!/usr/bin/env python3
"""
Генератор RSS ленты для Яндекс Дзен
"""

import json
import os
from datetime import datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def generate_rss(articles_dir="public/articles", output_file="public/rss.xml", site_url="https://crypto-dzen.vercel.app"):
    """
    Генерировать RSS ленту из статей
    """
    
    # Читаем все статьи
    articles = []
    articles_path = Path(articles_dir)
    
    for json_file in articles_path.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            article = json.load(f)
            articles.append(article)
    
    # Сортируем по дате (новые первыми)
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # Создаем RSS
    rss = Element('rss')
    rss.set('version', '2.0')
    rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
    rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    
    channel = SubElement(rss, 'channel')
    
    # Метаданные канала
    SubElement(channel, 'title').text = 'Crypto Digest - Ежедневные крипто-дайджесты'
    SubElement(channel, 'link').text = site_url
    SubElement(channel, 'description').text = 'Ежедневная сводка главных событий криптовалютного рынка. Агрегация данных из ведущих крипто-каналов.'
    SubElement(channel, 'language').text = 'ru'
    SubElement(channel, 'lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    
    # Self link (skip for now to avoid namespace issues)
    
    # Добавляем статьи
    for article in articles[:20]:  # Последние 20 статей
        item = SubElement(channel, 'item')
        
        SubElement(item, 'title').text = article['title']
        SubElement(item, 'link').text = f"{site_url}/{article['slug']}"
        SubElement(item, 'description').text = article['description']
        SubElement(item, 'pubDate').text = datetime.fromisoformat(article['date']).strftime('%a, %d %b %Y %H:%M:%S +0000')
        SubElement(item, 'guid').text = f"{site_url}/{article['slug']}"
        SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = article.get('author', 'Crypto Digest')
        
        # Категории (теги)
        for tag in article.get('tags', []):
            SubElement(item, 'category').text = tag
        
        # Полный контент
        content = SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded')
        content.text = f"<![CDATA[{article['content']}]]>"
        
        # Изображение (enclosure)
        if article.get('image'):
            enclosure = SubElement(item, 'enclosure')
            enclosure.set('url', f"{site_url}{article['image']}")
            enclosure.set('type', 'image/jpeg')
    
    # Форматируем XML
    xml_str = minidom.parseString(tostring(rss, encoding='utf-8')).toprettyxml(indent="  ", encoding='utf-8')
    
    # Сохраняем
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'wb') as f:
        f.write(xml_str)
    
    print(f"✅ RSS лента создана: {output_file}")
    print(f"📊 Статей в ленте: {len(articles)}")
    print(f"🔗 URL: {site_url}/rss.xml")

def main():
    workspace = Path("/root/.openclaw/workspace/dzen-auto")
    
    articles_dir = workspace / "public" / "articles"
    output_file = workspace / "public" / "rss.xml"
    
    # URL можно изменить после деплоя на Vercel
    site_url = "https://crypto-dzen.vercel.app"
    
    generate_rss(
        articles_dir=str(articles_dir),
        output_file=str(output_file),
        site_url=site_url
    )

if __name__ == "__main__":
    main()
