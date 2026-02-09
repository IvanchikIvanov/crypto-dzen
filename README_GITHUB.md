# 📊 Crypto Digest - RSS Feed for Yandex.Zen

Automated daily crypto digest aggregated from 9+ Telegram channels with 270K+ total subscribers.

## 🔗 RSS Feed

```
https://YOUR_USERNAME.github.io/REPO_NAME/rss.xml
```

## 📝 Content Categories

- 🔴 **Market** — Price movements, trends, positions
- 📈 **Signals** — Trading ideas, levels, entries/exits
- ⛓️ **On-Chain** — Blockchain data, whale movements
- ⚡️ **News** — Industry updates, announcements
- 💡 **Analysis** — Expert opinions, forecasts

## 🤖 Automation

Content is automatically:
1. Aggregated from Telegram channels daily at 12:00 MSK
2. Converted into article format
3. Added to RSS feed
4. Published to Yandex.Zen via RSS subscription

## 🛠️ Tech Stack

- **Content Collection:** Python + Pyrogram (Telegram API)
- **RSS Generation:** Python (native XML generation)
- **Hosting:** GitHub Pages
- **Automation:** GitHub Actions + OpenClaw Cron

## 📂 Structure

```
public/
├── index.html          # Landing page
├── rss.xml            # RSS feed (main)
└── articles/          # Article data
    ├── *.json         # Article metadata
    └── *.md           # Article content

Scripts:
├── convert_digest_to_article.py   # Telegram → Article
├── generate_rss_simple.py         # Article → RSS
└── update_content.py              # Full update workflow
```

## 🚀 Setup

See [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md) for detailed setup instructions.

## 📜 License

MIT

## 🤝 Contributing

This is an automated content aggregation project. For issues or suggestions, please open an issue.

---

**Powered by OpenClaw** 🤖
