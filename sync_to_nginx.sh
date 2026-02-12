#!/bin/bash
# Синхронизация обновлённых статей на nginx

rsync -av --delete /root/.openclaw/workspace/dzen-auto/public/ /var/www/crypto-dzen/

echo "✅ Статика синхронизирована с nginx"
