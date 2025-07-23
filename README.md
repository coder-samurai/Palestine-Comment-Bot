# 📣 Instagram Comment Bot for Palestine 🇵🇸

This is a fully automated Instagram commenting bot built using Python and Selenium.  
It rotates between multiple accounts, avoids duplicates, respects daily limits, and uses cookies to skip login where possible.

> ⚠️ This tool is developed **to support awareness for the people of Gaza and Palestine** by amplifying powerful messages through Instagram comments.

---

## ✊ Purpose

This project was created with a clear purpose:  
To **support digital resistance** and **spread awareness** for Palestine during times of censorship and silence.

Through hashtags like `#FreePalestine`, `#GazaUnderAttack`, and `#SavePalestine`, this bot ensures **your message continues** to be seen and heard, even when manual effort is not enough.

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

This tool interacts with Instagram and may violate their [Terms of Service](https://help.instagram.com/581066165581870).  
Use at your own risk. Your accounts may be blocked or flagged if overused or misused.

- Do **not** use this for spam, bots, or commercial promotion.
- This project was made **only to support humanitarian awareness**, especially for the oppressed in Gaza.
- Responsibility for use lies with **you**.

---

## ❤️ Final Word

> “When injustice becomes law, resistance becomes duty.”  
> Speak up. Even online. Even with code.  
> Especially when they try to silence the voices of the oppressed.

🇵🇸 **Free Palestine. Long live resistance.**
