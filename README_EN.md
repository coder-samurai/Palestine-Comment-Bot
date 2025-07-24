# 📣 Instagram Comment Bot for Palestine 🇵🇸

A fully automated, feature-rich Instagram commenting bot built with Python and Selenium.  
**Educational purposes only** - Restructured with clean code practices, user-friendly configuration, and advanced automation features.

> ⚠️ This tool is developed **to support awareness for the people of Gaza and Palestine** by amplifying powerful messages through Instagram comments.

---

## ✊ Purpose

This project was created with a clear purpose:  
To **support digital resistance** and **spread awareness** for Palestine during times of censorship and silence.

Through hashtags like `#FreePalestine`, `#GazaUnderAttack`, and `#SavePalestine`, this bot ensures **your message continues** to be seen and heard, even when manual effort is not enough.

> 🛑 This tool was not made to spread hate or spam. It is a **peaceful form of digital activism**.

---

## 🚀 **NEW Features - Fully Refactored**

### 🎮 **Interactive Control**
- **Console Commands**: `status`, `stats`, `pause`, `resume`, `stop`, `quit`
- **Telegram Remote Control**: Control bot from anywhere via `/status`, `/pause`, `/resume` commands
- **Real-time Statistics**: View daily comment counts per account
- **Graceful Shutdown**: Proper exit handling with signal management

### ⚙️ **User-Friendly Configuration**
- **Interactive Setup**: `python main.py --setup` for guided configuration
- **JSON Configuration**: All settings stored in `bot_config.json`
- **No Code Editing**: Configure everything through prompts or config file

### 🌐 **Advanced Proxy Management**
- **Speed Testing**: Automatically skip slow proxies (configurable latency threshold)
- **Smart Rotation**: Only use verified fast proxies
- **On-demand Testing**: Proxies tested only when needed
- **Fallback System**: Retry failed proxies in case of temporary issues

### 📱 **Telegram Integration**
- **Notifications**: Real-time logging to Telegram
- **Remote Commands**: Control bot via Telegram messages
- **Status Reports**: Get detailed bot status remotely
- **Statistics**: View comment stats via Telegram

### 🔒 **Enhanced Security & Reliability**
- **Cookie Persistence**: Smart session management
- **Daily Limits**: Per-account comment limits (configurable)
- **Duplicate Prevention**: Never comment twice on same post
- **Error Recovery**: Robust error handling and retry mechanisms

---

## 📁 **Required Files**

### `accounts.txt`
```
username1:password1  
username2:password2  
username3:password3
```

### `comments.txt`
```
🇵🇸 Free Palestine  
Justice for Gaza.  
أنقذوا أطفال فلسطين  
اللهم انصر أهل غزة
#FreePalestine ❤️
Stand with Palestine 🇵🇸
```

### `proxyscrape_premium_http_proxies.txt` (Optional)
```
192.168.1.1:8080
10.0.0.1:3128
proxy.example.com:3128
```

### `chromedriver.exe`
Download from [ChromeDriver](https://chromedriver.chromium.org/) and place in project folder.

---

## 🛠️ **Setup & Installation**

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Initial Setup**
```bash
python main.py --setup
```
This will guide you through:
- Daily limits and timing settings
- File paths configuration  
- Proxy settings (timeout, speed limits)
- Browser settings (headless mode)
- Telegram bot setup (optional)
- Target hashtags

### 3. **Alternative Setup Methods**
```bash
# Create sample config file to edit manually
python main.py --create-config

# Show help and all options
python main.py --help

# Run with existing configuration
python main.py
```

---

## ⚙️ **Configuration Options**

All settings are customizable via `bot_config.json`:

### 📊 **Limits & Timing**
- `daily_limit_per_account`: Max comments per account per day (default: 200)
- `min_delay_between_comments`: Minimum wait between comments (420s = 7min)
- `max_delay_between_comments`: Maximum wait between comments (480s = 8min)
- `min_comments_per_session`: Minimum comments per session (2)
- `max_comments_per_session`: Maximum comments per session (5)

### 🌐 **Proxy Settings**
- `use_proxy`: Enable/disable proxy rotation
- `proxy_timeout`: Connection timeout in seconds (5s)
- `max_proxy_latency`: Skip proxies slower than this (3000ms)
- `proxy_file`: Path to proxy file

### 📱 **Telegram Integration**
- `telegram_token`: Bot token from @BotFather
- `telegram_chat_id`: Your chat ID for notifications
- `enable_telegram_logging`: Auto-enabled when token + chat ID provided
- `enable_telegram_commands`: Remote control via Telegram

### 🎯 **Targeting**
- `hashtags`: List of hashtags to target
- `max_posts_per_hashtag`: Posts to check per hashtag (50)
- `max_scroll_attempts`: Scroll attempts to load posts (3)

---

## 🎮 **Interactive Commands**

### 🖥️ **Console Commands**
While bot is running, type:
- `status` - Show current bot status and configuration
- `stats` - Display today's comment statistics per account
- `pause` - Pause bot operation (can be resumed)
- `resume` - Resume paused bot operation
- `stop` - Stop bot gracefully (completes current session)
- `quit` - Force quit immediately
- `help` - Show available commands

### 📱 **Telegram Commands** (if enabled)
Send to your Telegram bot:
- `/status` - Show current bot status and configuration
- `/stats` - Display today's comment statistics per account
- `/pause` - Pause bot operation (can be resumed)
- `/resume` - Resume paused bot operation
- `/stop` - Stop bot gracefully (completes current session)
- `/help` - Show available Telegram commands

---

## 🧠 **How It Works**

1. **Account Rotation**: Cycles through multiple Instagram accounts
2. **Smart Login**: Uses saved cookies to skip login when possible
3. **Daily Limits**: Respects per-account daily comment limits
4. **Hashtag Processing**: Randomly processes configured hashtags
5. **Post Discovery**: Scrolls and finds posts for each hashtag
6. **Duplicate Prevention**: Skips posts already commented on
7. **Comment Posting**: Posts random comments from your list
8. **Statistics Tracking**: Records all activity in JSON format
9. **Proxy Rotation**: Uses fast, verified proxies for each session
10. **Real-time Control**: Respond to console/Telegram commands

---

## 📊 **Statistics & Monitoring**

The bot automatically tracks:
- Daily comment counts per account
- URLs commented on (prevents duplicates)
- Comment text used for each post
- Success/failure rates
- All data stored in `comment_stats.json`

Example stats output:
```
📈 Today's Statistics (2025-07-24):
   account1: 15 comments
   account2: 23 comments
   account3: 8 comments
📊 Total: 46 comments today
```

---

## 🚀 **Usage Examples**

### **Basic Usage**
```bash
# First time setup
python main.py --setup

# Run the bot
python main.py
```

### **Advanced Usage**
```bash
# Create custom config
python main.py --create-config
# Edit bot_config_sample.json and rename to bot_config.json

# Run with existing config
python main.py
```

### **Telegram Setup**
1. Message @BotFather on Telegram
2. Create bot with `/newbot`
3. Get your bot token
4. Message your bot, then visit `https://api.telegram.org/bot<TOKEN>/getUpdates`
5. Find your chat ID in the response
6. Add both to bot configuration

---

## 🔧 **Advanced Features**

### **Proxy Speed Testing**
- Automatically tests proxy latency
- Skips proxies slower than configured threshold
- Maintains list of working fast proxies
- Falls back gracefully when proxies fail

### **Session Management**
- Saves browser cookies for each account
- Automatically detects login status
- Handles 2FA and challenge detection
- Graceful error recovery

### **Smart Timing**
- Configurable delays between comments
- Respects daily limits automatically
- Random session sizes to appear natural
- Interruptible delays for immediate stop/pause

---

## 📱 **Telegram Bot Setup Guide**

1. **Create Bot**:
   - Message @BotFather on Telegram
   - Send `/newbot`
   - Choose name and username
   - Save the bot token

2. **Get Chat ID**:
   - Message your new bot
   - Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   - Find your chat ID in the JSON response

3. **Configure**:
   - Add token and chat ID during setup
   - Bot will automatically enable remote control

---

## 📜 **Disclaimer**

This tool interacts with Instagram and may violate their [Terms of Service](https://help.instagram.com/581066165581870).  
**Use at your own risk.** Your accounts may be blocked or flagged if overused or misused.

- ✅ **DO**: Use for peaceful awareness and education
- ❌ **DON'T**: Use for spam, harassment, or commercial promotion
- 🎓 **Purpose**: This project is for **educational purposes** and humanitarian awareness
- 🔒 **Responsibility**: Use lies entirely with **you**

---

## 🛡️ **Safety Features**

- **Rate Limiting**: Automatic delays between actions
- **Daily Limits**: Prevents overuse of accounts
- **Error Handling**: Graceful failure recovery
- **Session Management**: Proper cookie handling
- **Duplicate Prevention**: Never double-comment
- **Graceful Shutdown**: Clean exit on stop commands

---

## 🆘 **Troubleshooting**

### Common Issues:
- **ChromeDriver Error**: Download correct version from [ChromeDriver](https://chromedriver.chromium.org/)
- **Login Failed**: Check account credentials in `accounts.txt`
- **No Proxies**: Disable proxy usage or add working proxies
- **Telegram Not Working**: Verify token and chat ID

### Getting Help:
```bash
python main.py --help
```

---

## ❤️ **Final Word**

> "When injustice becomes law, resistance becomes duty."  
> Speak up. Even online. Even with code.  
> Especially when they try to silence the voices of the oppressed.

🇵🇸 **Free Palestine. Long live resistance.**

---

**Made with 💚 for digital activism and Palestinian awareness**