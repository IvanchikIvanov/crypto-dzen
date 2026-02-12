#!/usr/bin/env python3
"""
Обновление контента для Дзен
Конвертирует дайджест + генерирует RSS
"""

import subprocess
import sys
from pathlib import Path

def main():
    workspace = Path("/root/.openclaw/workspace/dzen-auto")
    
    print("="*60)
    print("🤖 ОБНОВЛЕНИЕ КОНТЕНТА ДЛЯ ДЗЕН")
    print("="*60 + "\n")
    
    # 1. Конвертация дайджеста
    print("📝 Шаг 1: Конвертация дайджеста в статью...")
    result = subprocess.run(
        ["python3", "convert_digest_to_article.py"],
        cwd=workspace,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Ошибка конвертации:\n{result.stderr}")
        sys.exit(1)
    
    print(result.stdout)
    
    # 2. Генерация RSS
    print("\n📡 Шаг 2: Генерация RSS ленты...")
    result = subprocess.run(
        ["python3", "generate_rss_simple.py"],
        cwd=workspace,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Ошибка генерации RSS:\n{result.stderr}")
        sys.exit(1)
    
    print(result.stdout)
    
    # 3. Синхронизация с nginx
    print("\n🔄 Шаг 3: Синхронизация с nginx...")
    result = subprocess.run(
        ["bash", "sync_to_nginx.sh"],
        cwd=workspace,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Ошибка синхронизации:\n{result.stderr}")
    else:
        print(result.stdout)
    
    # 4. Информация о результате
    print("\n" + "="*60)
    print("✅ КОНТЕНТ ОБНОВЛЁН!")
    print("="*60)
    print("\n📋 Доступно:")
    print("- 🌐 Сайт: http://134.199.228.121/")
    print("- 📡 RSS: http://134.199.228.121/rss.xml")
    print("\n💡 Следующие шаги:")
    print("1. Подключи домен (DuckDNS или купи)")
    print("2. Обнови RSS URL в Яндекс.Дзен")

if __name__ == "__main__":
    main()
