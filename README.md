# 📣 Instagram Comment Bot for Palestine 🇵🇸

[![Palestine](https://img.shields.io/badge/Support-Palestine-green?style=for-the-badge&logo=heart)](https://www.palestine.org)
[![Educational](https://img.shields.io/badge/Purpose-Educational-blue?style=for-the-badge)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://python.org)

**A fully automated, feature-rich Instagram commenting bot for digital activism and awareness.**

---

## 🌍 Choose Your Language / Kies je taal / اختر لغتك

| Language | File | Description |
|----------|------|-------------|
| 🇺🇸 **English** | [README_EN.md](README_EN.md) | Complete documentation in English |
| 🇳🇱 **Nederlands** | [README_NL.md](README_NL.md) | Volledige documentatie in het Nederlands |
| 🇸🇦 **العربية** | [README_AR.md](README_AR.md) | التوثيق الكامل باللغة العربية |

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Interactive setup
python main.py --setup

# Run the bot
python main.py
```

---

## ✊ Purpose

This project was created to **support digital resistance** and **spread awareness** for Palestine during times of censorship and silence.

Through hashtags like `#FreePalestine`, `#GazaUnderAttack`, and `#SavePalestine`, this bot ensures **your message continues** to be seen and heard.

> 🛑 This tool was not made to spread hate or spam. It is a **peaceful form of digital activism**.

---

## 🔧 Features

✅ Randomized account rotation  
✅ Auto-login with cookies (skip login if already signed in)  
✅ Per-account daily limit (default: 200)  
✅ Retry system with backoff for errors  
✅ Avoid reposting same comment on same link  
✅ Link + comment archiving per account and day  
✅ Headless mode supported

---

## 📁 Files & Setup

### `accounts.txt`

```
username1:password1  
username2:password2  
username3:password3
```

### `comments.txt`

A list of supportive, respectful comments to be posted (1 per line).  
You can write them in Arabic, English, Dutch, etc.

Example:
```
🇵🇸 Free Palestine  
Justice for Gaza.  
أنقذوا أطفال فلسطين  
اللهم انصر أهل غزة  
```

> ✍️ For best impact: Avoid emojis or all-caps. Keep it meaningful.

---

## 🧠 How It Works

- The bot loads all available accounts.
- For each account:
  - It checks if cookies exist and uses them to skip login.
  - If no cookies or invalid session, it logs in manually.
  - It checks how many comments were already posted today (per account).
  - It opens random posts for selected hashtags and comments, skipping duplicates.
  - It rotates between accounts every few comments.
  - It waits between 7-8 minutes after each comment to stay under radar (24h / 200 max = ±7 min).
- It keeps track of posted links + comments in `comment_stats.json`.

---

## 🚀 Running the Script

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

> For headless mode (no Chrome window): Set `HEADLESS_MODE = True` in the config.

---

## 📜 Disclaimer

This tool is for **educational purposes only**. Use responsibly and at your own risk.

- ✅ **DO**: Use for peaceful awareness and education
- ❌ **DON'T**: Use for spam, harassment, or commercial promotion
- 🎓 **Purpose**: Educational and humanitarian awareness
- 🔒 **Responsibility**: Lies entirely with the user

---

## ❤️ Support Palestine

> "When injustice becomes law, resistance becomes duty."

🇵🇸 **Free Palestine. Long live resistance.**

**Made with 💚 for digital activism and Palestinian awareness**

---

## 📞 Support

- 📖 **Documentation**: Choose your language above
- 🐛 **Issues**: Open an issue on GitHub
- 💬 **Questions**: Check the language-specific README files

---

### Project Structure

```
├── README.md           # This file (language selection)
├── README_EN.md        # English documentation
├── README_NL.md        # Dutch documentation  
├── README_AR.md        # Arabic documentation
├── main.py            # Main bot script
├── requirements.txt   # Dependencies
└── .gitignore        # Git ignore rules
```