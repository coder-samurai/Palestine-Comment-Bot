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

## ⚠️ **IMPORTANT: ChromeDriver Version Compatibility**

### 🇳🇱 **Nederlands**
De ChromeDriver versie moet **exact hetzelfde** zijn als je Chrome browser versie. Bijvoorbeeld: als je Chrome 120.0.6099.109 hebt, gebruik dan ChromeDriver 120.0.6099.109. Een verkeerde versie zorgt voor crashes en "session not created" errors.

### 🇺🇸 **English**
The ChromeDriver version must be **exactly the same** as your Chrome browser version. For example: if you have Chrome 120.0.6099.109, use ChromeDriver 120.0.6099.109. A mismatched version causes crashes and "session not created" errors.

### 🇸🇦 **العربية**
يجب أن تكون نسخة ChromeDriver **مطابقة تماماً** لنسخة متصفح Chrome. مثال: إذا كان لديك Chrome 120.0.6099.109، استخدم ChromeDriver 120.0.6099.109. النسخة الخاطئة تسبب أخطاء وتعطل البرنامج.

**Quick Version Check:**
```bash
# Check Chrome version
google-chrome --version
# or
chromium --version

# Download matching ChromeDriver from:
# https://chromedriver.chromium.org/downloads
```

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

## 🚀 Key Features

### 🎮 **Interactive Control**
- Console Commands: `status`, `stats`, `pause`, `resume`, `stop`
- Telegram Remote Control: Control from anywhere
- Real-time Statistics and Monitoring

### ⚙️ **User-Friendly Configuration**
- Interactive Setup: `python main.py --setup`
- JSON Configuration: All settings in `bot_config.json`
- No Code Editing Required

### 🌐 **Advanced Proxy Management**
- Speed Testing: Skip slow proxies automatically
- Smart Rotation: Only verified fast proxies
- Fallback System: Retry failed proxies

### 📱 **Telegram Integration**
- Real-time Notifications
- Remote Commands: `/status`, `/pause`, `/resume`
- Statistics via Telegram

### 🔒 **Enhanced Security**
- Cookie Persistence
- Daily Limits per Account
- Duplicate Prevention
- Error Recovery

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