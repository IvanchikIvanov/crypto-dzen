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
    
    # 3. Информация о деплое
    print("\n" + "="*60)
    print("✅ КОНТЕНТ ОБНОВЛЁН!")
    print("="*60)
    print("\n📋 Следующие шаги:")
    print("1. Запустите: cd /root/.openclaw/workspace/dzen-auto")
    print("2. Деплой: vercel --prod")
    print("\nИли настройте автоматический деплой через GitHub + Vercel.")
    print("\n🔗 RSS URL: https://dzen-auto-a4jrr0g9m-ivanchikivanovs-projects.vercel.app/rss.xml")

if __name__ == "__main__":
    main()
