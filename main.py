# Instagram Bot - Educational Refactored Version with User Configuration
# Restructured for clean code practices and maintainability

import os
import time
import json
import random
import signal
import sys
import threading
from datetime import datetime
from itertools import cycle
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
from abc import ABC, abstractmethod
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@dataclass
class BotConfig:
    """Configuration class for bot settings - All user-customizable options"""
    
    # Daily limits and timing
    daily_limit_per_account: int = 200
    min_delay_between_comments: int = 420  # seconds (7 minutes)
    max_delay_between_comments: int = 480  # seconds (8 minutes)
    min_comments_per_session: int = 2
    max_comments_per_session: int = 5
    
    # File paths
    comments_file: str = 'comments.txt'
    accounts_file: str = 'accounts.txt'
    chromedriver_path: str = 'chromedriver.exe'
    log_file: str = 'log.txt'
    stats_file: str = 'comment_stats.json'
    cookies_dir: str = 'cookies'
    
    # Proxy settings
    proxy_file: str = 'proxyscrape_premium_http_proxies.txt'
    use_proxy: bool = True
    proxy_timeout: int = 5  # seconds
    max_proxy_latency: int = 3000  # milliseconds - skip proxies slower than this
    
    # Browser settings
    headless_mode: bool = False
    
    # Telegram notifications
    telegram_token: str = ""  # Leave empty to disable Telegram notifications
    telegram_chat_id: str = ""  # Leave empty to disable Telegram notifications
    enable_telegram_logging: bool = False
    enable_telegram_commands: bool = False  # Enable remote control via Telegram
    
    # Target hashtags
    hashtags: List[str] = None
    
    # Advanced settings
    max_posts_per_hashtag: int = 50
    max_scroll_attempts: int = 3
    login_wait_time: int = 8
    post_load_wait_time: int = 5
    
    def __post_init__(self):
        if self.hashtags is None:
            self.hashtags = ['#freepalestine', '#gazaunderattack', '#savepalestine']
        
        # Validate telegram settings
        if self.telegram_token and self.telegram_chat_id:
            self.enable_telegram_logging = True
            self.enable_telegram_commands = True
        else:
            self.enable_telegram_logging = False
            self.enable_telegram_commands = False
    
    @classmethod
    def load_from_file(cls, config_file: str = 'bot_config.json'):
        """Load configuration from JSON file"""
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return cls(**data)
            except Exception as e:
                print(f"Error loading config file: {e}")
                print("Using default configuration...")
        return cls()
    
    def save_to_file(self, config_file: str = 'bot_config.json'):
        """Save current configuration to JSON file"""
        try:
            # Convert to dict, excluding methods
            config_dict = {}
            for key, value in self.__dict__.items():
                if not key.startswith('_') and not callable(value):
                    config_dict[key] = value
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=4, ensure_ascii=False)
            print(f"Configuration saved to {config_file}")
        except Exception as e:
            print(f"Error saving config file: {e}")
    
    def interactive_setup(self):
        """Interactive setup for first-time users"""
        print("=== Instagram Bot Configuration Setup ===\n")
        
        # Daily limits
        print("📊 DAILY LIMITS & TIMING")
        try:
            self.daily_limit_per_account = int(input(f"Daily comment limit per account [{self.daily_limit_per_account}]: ") or self.daily_limit_per_account)
            self.min_comments_per_session = int(input(f"Minimum comments per session [{self.min_comments_per_session}]: ") or self.min_comments_per_session)
            self.max_comments_per_session = int(input(f"Maximum comments per session [{self.max_comments_per_session}]: ") or self.max_comments_per_session)
            
            print("\n⏱️ TIMING BETWEEN COMMENTS")
            self.min_delay_between_comments = int(input(f"Minimum delay between comments (seconds) [{self.min_delay_between_comments}]: ") or self.min_delay_between_comments)
            self.max_delay_between_comments = int(input(f"Maximum delay between comments (seconds) [{self.max_delay_between_comments}]: ") or self.max_delay_between_comments)
        except ValueError:
            print("Invalid input, using default values")
        
        # File paths
        print("\n📁 FILE PATHS")
        self.comments_file = input(f"Comments file path [{self.comments_file}]: ") or self.comments_file
        self.accounts_file = input(f"Accounts file path [{self.accounts_file}]: ") or self.accounts_file
        self.chromedriver_path = input(f"ChromeDriver path [{self.chromedriver_path}]: ") or self.chromedriver_path
        self.proxy_file = input(f"Proxy file path [{self.proxy_file}]: ") or self.proxy_file
        
        # Proxy settings
        print("\n🌐 PROXY SETTINGS")
        use_proxy_input = input(f"Use proxy rotation? (y/n) [{'y' if self.use_proxy else 'n'}]: ").lower()
        self.use_proxy = use_proxy_input == 'y' if use_proxy_input else self.use_proxy
        
        if self.use_proxy:
            try:
                self.proxy_timeout = int(input(f"Proxy timeout (seconds) [{self.proxy_timeout}]: ") or self.proxy_timeout)
                self.max_proxy_latency = int(input(f"Max proxy latency (ms) [{self.max_proxy_latency}]: ") or self.max_proxy_latency)
            except ValueError:
                print("Invalid input for proxy settings, using defaults")
        
        # Browser settings
        print("\n🌊 BROWSER SETTINGS")
        headless_input = input(f"Run in headless mode? (y/n) [{'y' if self.headless_mode else 'n'}]: ").lower()
        self.headless_mode = headless_input == 'y' if headless_input else self.headless_mode
        
        # Telegram settings
        print("\n📱 TELEGRAM NOTIFICATIONS (Optional - leave empty to disable)")
        telegram_token = input(f"Telegram bot token [{self.telegram_token}]: ")
        if telegram_token:
            self.telegram_token = telegram_token
        
        telegram_chat_id = input(f"Telegram chat ID [{self.telegram_chat_id}]: ")
        if telegram_chat_id:
            self.telegram_chat_id = telegram_chat_id
        
        # Update telegram logging based on inputs
        if self.telegram_token and self.telegram_chat_id:
            self.enable_telegram_logging = True
            self.enable_telegram_commands = True
            print("✅ Telegram notifications and remote commands enabled")
        else:
            self.enable_telegram_logging = False
            self.enable_telegram_commands = False
            print("❌ Telegram notifications and remote commands disabled")
        
        # Hashtags
        print("\n🏷️ TARGET HASHTAGS")
        hashtags_input = input(f"Enter hashtags (comma-separated) [{','.join(self.hashtags)}]: ")
        if hashtags_input:
            self.hashtags = [tag.strip() for tag in hashtags_input.split(',')]
        
        print(f"\n✅ Configuration complete!")
        
        # Ask to save
        save_config = input("Save this configuration to file? (y/n) [y]: ").lower()
        if save_config != 'n':
            self.save_to_file()


class Logger:
    """Centralized logging system"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.log_file = config.log_file
        
    def log(self, message: str, username: str = None) -> None:
        """Log message to file and optionally send to Telegram"""
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        user_prefix = f"[{username}] " if username else ""
        formatted_message = f"{timestamp} {user_prefix}{message}"
        
        # Print to console
        print(formatted_message)
        
        # Write to file
        self._write_to_file(formatted_message)
        
        # Send to Telegram if enabled
        if self.config.enable_telegram_logging:
            self._send_telegram_message(formatted_message)
    
    def _write_to_file(self, message: str) -> None:
        """Write message to log file"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(message + '\n')
        except Exception as e:
            print(f"Failed to write to log file: {e}")
    
    def _send_telegram_message(self, message: str) -> None:
        """Send message to Telegram bot"""
        if not self.config.enable_telegram_logging:
            return
            
        try:
            requests.get(
                f"https://api.telegram.org/bot{self.config.telegram_token}/sendMessage",
                params={"chat_id": self.config.telegram_chat_id, "text": message},
                timeout=5
            )
        except Exception as e:
            print(f"Telegram logging failed: {e}")
    
    def send_telegram_message_direct(self, message: str) -> None:
        """Send message directly to Telegram (for responses)"""
        if not self.config.enable_telegram_commands:
            return
            
        try:
            requests.get(
                f"https://api.telegram.org/bot{self.config.telegram_token}/sendMessage",
                params={"chat_id": self.config.telegram_chat_id, "text": message},
                timeout=5
            )
        except Exception as e:
            print(f"Telegram message failed: {e}")
    
    def log_error(self, message: str, username: str = None) -> None:
        """Log error to separate error file"""
        error_message = f"[{datetime.now()}] {message}"
        try:
            with open('errors.log', 'a', encoding='utf-8') as f:
                f.write(error_message + '\n')
        except Exception as e:
            print(f"Failed to write error log: {e}")
        
        self.log(f"ERROR: {message}", username)


class TelegramCommandHandler:
    """Handles Telegram bot commands for remote control"""
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.config = orchestrator.config
        self.logger = orchestrator.logger
        self.running = False
        self.telegram_thread = None
        self.last_update_id = 0
    
    def start(self):
        """Start Telegram command polling"""
        if not self.config.enable_telegram_commands:
            return
            
        self.running = True
        self.telegram_thread = threading.Thread(target=self._polling_loop, daemon=True)
        self.telegram_thread.start()
        
        # Send startup message
        self.logger.send_telegram_message_direct(
            "🤖 Bot started! Remote control enabled.\n\n"
            "Available commands:\n"
            "/status - Show bot status\n"
            "/stats - Show statistics\n" 
            "/pause - Pause bot\n"
            "/resume - Resume bot\n"
            "/stop - Stop bot gracefully\n"
            "/help - Show this help"
        )
        print("📱 Telegram remote control enabled")
    
    def stop(self):
        """Stop Telegram command polling"""
        self.running = False
        if self.config.enable_telegram_commands:
            self.logger.send_telegram_message_direct("🛑 Bot stopped")
    
    def _polling_loop(self):
        """Main polling loop for Telegram updates"""
        while self.running:
            try:
                self._check_for_updates()
                time.sleep(2)  # Poll every 2 seconds
            except Exception as e:
                print(f"Telegram polling error: {e}")
                time.sleep(5)
    
    def _check_for_updates(self):
        """Check for new Telegram messages"""
        try:
            response = requests.get(
                f"https://api.telegram.org/bot{self.config.telegram_token}/getUpdates",
                params={"offset": self.last_update_id + 1, "timeout": 1},
                timeout=3
            )
            
            if response.status_code == 200:
                data = response.json()
                if data["ok"] and data["result"]:
                    for update in data["result"]:
                        self._process_update(update)
                        self.last_update_id = update["update_id"]
        except Exception as e:
            # Silently ignore polling errors to avoid spam
            pass
    
    def _process_update(self, update):
        """Process a single Telegram update"""
        if "message" not in update:
            return
            
        message = update["message"]
        
        # Verify it's from the correct chat
        if str(message["chat"]["id"]) != self.config.telegram_chat_id:
            return
            
        # Get the command text
        text = message.get("text", "").strip()
        if not text.startswith("/"):
            return
            
        command = text.lower().split()[0]
        self._handle_telegram_command(command)
    
    def _handle_telegram_command(self, command: str):
        """Handle Telegram commands"""
        if command == "/status":
            self._send_status()
        elif command == "/stats":
            self._send_stats()
        elif command == "/pause":
            self.orchestrator.pause()
            self.logger.send_telegram_message_direct("⏸️ Bot paused")
        elif command == "/resume":
            self.orchestrator.resume()
            self.logger.send_telegram_message_direct("▶️ Bot resumed")
        elif command == "/stop":
            self.logger.send_telegram_message_direct("🛑 Stopping bot gracefully...")
            self.orchestrator.stop()
        elif command == "/help":
            self._send_help()
        else:
            self.logger.send_telegram_message_direct(f"❓ Unknown command: {command}\nSend /help for available commands")
    
    def _send_status(self):
        """Send bot status via Telegram"""
        status = "RUNNING" if not self.orchestrator.paused else "PAUSED"
        current_account = getattr(self.orchestrator, 'current_account', 'None')
        
        message = f"""📊 Bot Status Report
        
🔄 Status: {status}
👥 Accounts: {len(self.orchestrator.accounts)}
👤 Current: {current_account}
🏷️ Hashtags: {', '.join(self.config.hashtags)}
⏱️ Delay: {self.config.min_delay_between_comments}-{self.config.max_delay_between_comments}s
🌐 Proxy: {'✅' if self.config.use_proxy else '❌'}
👁️ Headless: {'✅' if self.config.headless_mode else '❌'}"""
        
        self.logger.send_telegram_message_direct(message)
    
    def _send_stats(self):
        """Send statistics via Telegram"""
        stats = self.orchestrator.stats_manager.stats
        today = datetime.now().strftime("%Y-%m-%d")
        
        message = f"📈 Today's Statistics ({today}):\n\n"
        total_comments = 0
        
        for username, user_stats in stats.items():
            if today in user_stats:
                count = user_stats[today].get("count", 0)
                total_comments += count
                message += f"👤 {username}: {count} comments\n"
        
        message += f"\n📊 Total: {total_comments} comments today"
        
        if total_comments == 0:
            message = "📈 No comments posted today yet"
        
        self.logger.send_telegram_message_direct(message)
    
    def _send_help(self):
        """Send help message via Telegram"""
        help_text = """🤖 Instagram Bot Remote Control

Available Commands:
/status - Show current bot status and configuration
/stats - Display today's comment statistics
/pause - Pause bot operation (can be resumed)
/resume - Resume paused bot operation
/stop - Stop bot gracefully
/help - Show this help message

💡 Bot will continue running in background and send status updates automatically."""
        
        self.logger.send_telegram_message_direct(help_text)


class InputHandler:
    """Handles user input during bot operation"""
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.running = False
        self.input_thread = None
    
    def start(self):
        """Start input handling thread"""
        self.running = True
        self.input_thread = threading.Thread(target=self._input_loop, daemon=True)
        self.input_thread.start()
        print("\n🎮 Interactive commands available:")
        print("   'status' - Show current bot status")
        print("   'stats' - Show comment statistics")
        print("   'pause' - Pause bot operation")
        print("   'resume' - Resume bot operation")
        print("   'stop' - Stop bot gracefully")
        print("   'quit' - Force quit immediately")
        if self.orchestrator.config.enable_telegram_commands:
            print("   📱 Telegram remote control is also enabled!")
        print()
    
    def stop(self):
        """Stop input handling"""
        self.running = False
    
    def _input_loop(self):
        """Main input handling loop"""
        while self.running:
            try:
                user_input = input().strip().lower()
                self._handle_command(user_input)
            except (EOFError, KeyboardInterrupt):
                break
            except Exception as e:
                print(f"Input error: {e}")
    
    def _handle_command(self, command: str):
        """Handle user commands"""
        if command == 'status':
            self._show_status()
        elif command == 'stats':
            self._show_stats()
        elif command == 'pause':
            self.orchestrator.pause()
        elif command == 'resume':
            self.orchestrator.resume()
        elif command == 'stop':
            self.orchestrator.stop()
        elif command == 'quit':
            self.orchestrator.force_quit()
        elif command == 'help':
            self._show_help()
        else:
            print(f"Unknown command: {command}. Type 'help' for available commands.")
    
    def _show_status(self):
        """Show current bot status"""
        status = "RUNNING" if not self.orchestrator.paused else "PAUSED"
        print(f"\n📊 Bot Status: {status}")
        print(f"🔄 Accounts loaded: {len(self.orchestrator.accounts)}")
        print(f"🏷️ Target hashtags: {', '.join(self.orchestrator.config.hashtags)}")
        print(f"⏱️ Comment delay: {self.orchestrator.config.min_delay_between_comments}-{self.orchestrator.config.max_delay_between_comments}s")
        if hasattr(self.orchestrator, 'current_account'):
            print(f"👤 Current account: {self.orchestrator.current_account}")
        print()
    
    def _show_stats(self):
        """Show comment statistics"""
        stats = self.orchestrator.stats_manager.stats
        today = datetime.now().strftime("%Y-%m-%d")
        
        print(f"\n📈 Today's Statistics ({today}):")
        total_comments = 0
        
        for username, user_stats in stats.items():
            if today in user_stats:
                count = user_stats[today].get("count", 0)
                total_comments += count
                print(f"   {username}: {count} comments")
        
        print(f"📊 Total comments today: {total_comments}")
        print()
    
    def _show_help(self):
        """Show available commands"""
        print("""
🎮 Available Commands:
   status - Show current bot status
   stats  - Show comment statistics
   pause  - Pause bot operation
   resume - Resume bot operation  
   stop   - Stop bot gracefully
   quit   - Force quit immediately
   help   - Show this help message
""")


class ExitHandler:
    """Handles graceful shutdown of the bot"""
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        if hasattr(signal, 'SIGBREAK'):  # Windows
            signal.signal(signal.SIGBREAK, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n⚠️ Received shutdown signal ({signum})")
        self.orchestrator.stop()


class ProxyManager:
    """Manages proxy rotation and testing with speed filtering"""
    
    def __init__(self, config: BotConfig, logger: Logger):
        self.config = config
        self.proxy_file = config.proxy_file
        self.logger = logger
        self.all_proxies = self._load_proxies()
        self.working_proxies = []
        self.failed_proxies = set()
        self.slow_proxies = set()  # Track proxies that are too slow
        self.current_proxy_index = 0
    
    def _load_proxies(self) -> List[str]:
        """Load proxies from file without testing"""
        if not self.config.use_proxy:
            self.logger.log("Proxy usage disabled in configuration")
            return []
            
        if not os.path.exists(self.proxy_file):
            self.logger.log(f"Proxy file not found: {self.proxy_file}")
            return []
        
        with open(self.proxy_file, 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f if line.strip()]
        
        self.logger.log(f"Loaded {len(proxies)} proxies from file")
        return proxies
    
    def _test_proxy(self, proxy: str) -> bool:
        """Test if proxy is working and fast enough"""
        if proxy in self.failed_proxies or proxy in self.slow_proxies:
            return False
            
        try:
            start_time = time.time()
            response = requests.get(
                "https://httpbin.org/ip",
                proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                timeout=self.config.proxy_timeout
            )
            latency = round((time.time() - start_time) * 1000)
            
            if response.status_code == 200:
                # Check if proxy is fast enough
                if latency > self.config.max_proxy_latency:
                    self.logger.log(f"🐌 Proxy too slow ({latency}ms > {self.config.max_proxy_latency}ms): {proxy}")
                    self.slow_proxies.add(proxy)
                    return False
                
                self.logger.log(f"✅ Proxy works ({latency}ms): {proxy}")
                return True
            else:
                self.logger.log(f"❌ Proxy returned status {response.status_code}: {proxy}")
        except requests.exceptions.Timeout:
            self.logger.log(f"⏱️ Proxy timeout ({self.config.proxy_timeout}s): {proxy}")
            self.slow_proxies.add(proxy)
        except Exception as e:
            self.logger.log(f"❌ Proxy failed {proxy}: {e}")
        
        # Mark as failed to avoid retesting
        self.failed_proxies.add(proxy)
        return False
    
    def get_next_proxy(self) -> Optional[str]:
        """Get next working proxy, testing on-demand"""
        if not self.config.use_proxy:
            return None
            
        # First, try to use already verified working proxies
        if self.working_proxies:
            proxy = self.working_proxies[self.current_proxy_index % len(self.working_proxies)]
            self.current_proxy_index += 1
            return proxy
        
        # If no working proxies yet, test new ones until we find one
        untested_proxies = [p for p in self.all_proxies 
                           if p not in self.failed_proxies and p not in self.slow_proxies]
        
        for proxy in untested_proxies:
            if self._test_proxy(proxy):
                self.working_proxies.append(proxy)
                return proxy
        
        # If all proxies failed, clear failed list and try again (in case of temporary issues)
        if not untested_proxies and (self.failed_proxies or self.slow_proxies):
            self.logger.log("All proxies failed or too slow, clearing lists and retrying...")
            self.failed_proxies.clear()
            self.slow_proxies.clear()
            # Try first proxy again
            if self.all_proxies and self._test_proxy(self.all_proxies[0]):
                self.working_proxies.append(self.all_proxies[0])
                return self.all_proxies[0]
        
        self.logger.log("No working proxies available")
        return None


class CookieManager:
    """Manages browser cookies for session persistence"""
    
    def __init__(self, cookies_dir: str):
        self.cookies_dir = cookies_dir
        os.makedirs(cookies_dir, exist_ok=True)
    
    def save_cookies(self, driver, username: str) -> None:
        """Save browser cookies for user"""
        cookie_path = os.path.join(self.cookies_dir, f"{username}.json")
        try:
            with open(cookie_path, 'w', encoding='utf-8') as f:
                json.dump(driver.get_cookies(), f)
        except Exception as e:
            print(f"Failed to save cookies for {username}: {e}")
    
    def load_cookies(self, driver, username: str) -> bool:
        """Load saved cookies for user"""
        cookie_path = os.path.join(self.cookies_dir, f"{username}.json")
        
        if not os.path.exists(cookie_path):
            return False
        
        try:
            driver.get("https://www.instagram.com")
            with open(cookie_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            
            for cookie in cookies:
                driver.add_cookie(cookie)
            
            driver.get("https://www.instagram.com")
            return True
        except Exception as e:
            print(f"Failed to load cookies for {username}: {e}")
            return False


class StatsManager:
    """Manages comment statistics and tracking"""
    
    def __init__(self, stats_file: str):
        self.stats_file = stats_file
        self.stats = self._load_stats()
    
    def _load_stats(self) -> Dict:
        """Load statistics from file"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load stats: {e}")
        return {}
    
    def save_stats(self) -> None:
        """Save statistics to file"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"Failed to save stats: {e}")
    
    def get_daily_count(self, username: str) -> int:
        """Get today's comment count for user"""
        today_str = datetime.now().strftime("%Y-%m-%d")
        return self.stats.get(username, {}).get(today_str, {}).get("count", 0)
    
    def is_duplicate_link(self, username: str, url: str) -> bool:
        """Check if URL was already commented on today"""
        today_str = datetime.now().strftime("%Y-%m-%d")
        account_stats = self.stats.get(username, {}).get(today_str, {}).get("hashtags", {})
        
        for links in account_stats.values():
            for item in links:
                if item["url"] == url:
                    return True
        return False
    
    def record_comment(self, username: str, hashtag: str, url: str, comment: str) -> None:
        """Record a successful comment"""
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        # Initialize nested structure if needed
        if username not in self.stats:
            self.stats[username] = {}
        if today_str not in self.stats[username]:
            self.stats[username][today_str] = {"count": 0, "hashtags": {}}
        if hashtag not in self.stats[username][today_str]["hashtags"]:
            self.stats[username][today_str]["hashtags"][hashtag] = []
        
        # Record the comment
        self.stats[username][today_str]["hashtags"][hashtag].append({
            "url": url,
            "comment": comment
        })
        self.stats[username][today_str]["count"] += 1
        
        # Save immediately
        self.save_stats()


class BrowserManager:
    """Manages browser setup and configuration"""
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36"
    ]
    
    def __init__(self, config: BotConfig, proxy_manager: ProxyManager, logger: Logger):
        self.config = config
        self.proxy_manager = proxy_manager
        self.logger = logger
    
    def create_driver(self):
        """Create and configure Chrome driver"""
        options = uc.ChromeOptions()
        
        if self.config.headless_mode:
            options.add_argument("--headless=new")
            self.logger.log("Running in headless mode")
        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f"--user-agent={random.choice(self.USER_AGENTS)}")
        
        # Add proxy if enabled
        if self.config.use_proxy:
            proxy = self.proxy_manager.get_next_proxy()
            if proxy:
                options.add_argument(f"--proxy-server=http://{proxy}")
                self.logger.log(f"Using proxy: {proxy}")
        
        try:
            driver = uc.Chrome(
                service=Service(self.config.chromedriver_path),
                options=options
            )
            
            # Anti-detection script
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                    window.navigator.chrome = { runtime: {} };
                """
            })
            
            return driver
            
        except WebDriverException as e:
            self.logger.log_error(f"Failed to start browser: {e}")
            raise


class InstagramBot:
    """Main Instagram automation bot"""
    
    def __init__(self, username: str, password: str, config: BotConfig, 
                 logger: Logger, cookie_manager: CookieManager, browser_manager: BrowserManager):
        self.username = username
        self.password = password
        self.config = config
        self.logger = logger
        self.cookie_manager = cookie_manager
        self.browser_manager = browser_manager
        self.visited_urls: Set[str] = set()
        self.comments = self._load_comments()
        self.driver = None
    
    def _load_comments(self) -> List[str]:
        """Load comments from file"""
        if not os.path.exists(self.config.comments_file):
            self.logger.log_error(f"Comments file not found: {self.config.comments_file}")
            raise FileNotFoundError(f"Comments file not found: {self.config.comments_file}")
        
        with open(self.config.comments_file, 'r', encoding='utf-8') as f:
            comments = [self._strip_non_bmp(line.strip()) for line in f if line.strip()]
        
        if not comments:
            raise ValueError("No comments found in comments file")
        
        return comments
    
    @staticmethod
    def _strip_non_bmp(text: str) -> str:
        """Remove non-BMP characters from text"""
        return ''.join(c for c in text if ord(c) <= 0xFFFF)
    
    def start_session(self) -> None:
        """Start browser session"""
        self.driver = self.browser_manager.create_driver()
        self.logger.log("Browser started", self.username)
    
    def login(self) -> bool:
        """Login to Instagram"""
        if not self.driver:
            raise RuntimeError("Browser session not started")
        
        # Try loading cookies first
        if self.cookie_manager.load_cookies(self.driver, self.username):
            time.sleep(3)
            if "login" not in self.driver.current_url:
                self.logger.log("✅ Session active, logged in via cookies", self.username)
                return True
        
        # Manual login
        self.logger.log("🔐 Logging in manually", self.username)
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(self.config.login_wait_time)
        
        try:
            username_field = self.driver.find_element(By.NAME, 'username')
            password_field = self.driver.find_element(By.NAME, 'password')
            
            username_field.send_keys(self.username)
            password_field.send_keys(self.password + Keys.RETURN)
            time.sleep(self.config.login_wait_time)
            
            current_url = self.driver.current_url
            
            if "challenge" in current_url:
                self.logger.log("⚠️ Challenge or 2FA detected", self.username)
                return False
            
            if "accounts/login" in current_url:
                self.logger.log("❌ Login failed. Check credentials", self.username)
                return False
            
            # Save cookies on successful login
            self.cookie_manager.save_cookies(self.driver, self.username)
            self.logger.log("✅ Logged in successfully", self.username)
            return True
            
        except Exception as e:
            self.logger.log_error(f"Login exception: {e}", self.username)
            return False
    
    def get_post_links(self, hashtag: str) -> List[str]:
        """Get post links for a hashtag"""
        try:
            # Clean hashtag (remove # if present)
            clean_hashtag = hashtag.replace('#', '')
            url = f'https://www.instagram.com/explore/tags/{clean_hashtag}/'
            
            self.logger.log(f"🔍 Searching posts for {hashtag}...", self.username)
            self.driver.get(url)
            time.sleep(self.config.post_load_wait_time + 3)  # Extra wait for hashtag pages
            
            # Check if page loaded properly
            if "Sorry, this page isn't available" in self.driver.page_source:
                self.logger.log(f"❌ Hashtag page not available: {hashtag}", self.username)
                return []
            
            # Multiple scroll attempts to load more posts
            for scroll in range(self.config.max_scroll_attempts):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)
                self.logger.log(f"📜 Scrolling... ({scroll+1}/{self.config.max_scroll_attempts})", self.username)
            
            # Try multiple selectors for post links
            post_links = []
            
            # Method 1: Standard post links
            links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/']")
            for link in links:
                href = link.get_attribute('href')
                if href and '/p/' in href and href not in post_links:
                    post_links.append(href)
            
            # Method 2: Alternative selector
            if not post_links:
                links = self.driver.find_elements(By.TAG_NAME, 'a')
                for link in links:
                    href = link.get_attribute('href')
                    if href and '/p/' in href and 'instagram.com/p/' in href:
                        post_links.append(href)
            
            # Remove duplicates and limit results
            unique_links = list(set(post_links))[:self.config.max_posts_per_hashtag]
            
            if unique_links:
                self.logger.log(f"✅ Found {len(unique_links)} posts for {hashtag}", self.username)
            else:
                self.logger.log(f"⚠️ No posts found for {hashtag}", self.username)
                # Log page source snippet for debugging
                page_text = self.driver.page_source[:500]
                self.logger.log(f"📄 Page preview: {page_text[:100]}...", self.username)
            
            return unique_links
            
        except Exception as e:
            self.logger.log_error(f"Failed to get post links for {hashtag}: {e}", self.username)
            return []
    
    def comment_on_post(self, url: str) -> Optional[Tuple[str, str]]:
        """Comment on a single post"""
        if url in self.visited_urls:
            return None
        
        try:
            self.logger.log(f"🌐 Opening post: {url[:50]}...", self.username)
            self.driver.get(url)
            time.sleep(self.config.post_load_wait_time)
            
            # Check if post is accessible
            if "Sorry, this post isn't available" in self.driver.page_source:
                self.logger.log("❌ Post not available or deleted", self.username)
                return None
            
            # Try to click comment icon
            try:
                comment_icon = self.driver.find_element(By.XPATH, "//svg[@aria-label='Comment']")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", comment_icon)
                comment_icon.click()
                time.sleep(2)
                self.logger.log("👆 Comment icon clicked", self.username)
            except NoSuchElementException:
                self.logger.log("ℹ️ Comment icon not found, may already be open", self.username)
            
            # Find and focus comment box
            comment_box = None
            for attempt in range(5):
                try:
                    comment_box = self.driver.find_element(By.XPATH, "//textarea[@aria-label='Add a comment…']")
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", comment_box)
                    self.driver.execute_script("arguments[0].focus();", comment_box)
                    comment_box.click()
                    time.sleep(1)
                    
                    # Re-find element to avoid stale reference
                    comment_box = self.driver.find_element(By.XPATH, "//textarea[@aria-label='Add a comment…']")
                    if comment_box.is_displayed() and comment_box.is_enabled():
                        self.logger.log("✍️ Comment box ready", self.username)
                        break
                        
                except StaleElementReferenceException:
                    self.logger.log(f"🔄 Stale element, retrying... ({attempt+1}/5)", self.username)
                    time.sleep(1)
                except Exception as e:
                    self.logger.log(f"⚠️ Failed to locate comment box ({attempt+1}/5): {e}", self.username)
                    time.sleep(1)
            
            if not comment_box:
                self.logger.log("❌ Unable to locate comment box after retries", self.username)
                return None
            
            # Select and type comment
            comment_text = self._strip_non_bmp(random.choice(self.comments))
            self.logger.log(f"📝 Typing comment: {comment_text[:30]}...", self.username)
            
            comment_box.clear()
            comment_box.send_keys(comment_text)
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", 
                comment_box
            )
            time.sleep(2)
            
            # Click post button with retries
            post_clicked = False
            for attempt in range(10):
                try:
                    post_button = self.driver.find_element(By.XPATH, "//div[@role='button' and text()='Post']")
                    if post_button.is_enabled():
                        post_button.click()
                        post_clicked = True
                        self.logger.log("📤 Post button clicked", self.username)
                        break
                except Exception:
                    time.sleep(0.5)
            
            if not post_clicked:
                self.logger.log("❌ Failed to click post button", self.username)
                return None
            
            time.sleep(3)
            self.visited_urls.add(url)
            self.logger.log(f"✅ Comment posted successfully!", self.username)
            return url, comment_text
            
        except Exception as e:
            self.logger.log_error(f"💥 Failed to comment on post: {e}", self.username)
            return None
    
    def close_session(self) -> None:
        """Close browser session"""
        if self.driver:
            self.driver.quit()
            self.logger.log("Browser session closed", self.username)


class BotOrchestrator:
    """Main orchestrator for the bot system"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.logger = Logger(config)
        self.proxy_manager = ProxyManager(config, self.logger)
        self.cookie_manager = CookieManager(config.cookies_dir)
        self.browser_manager = BrowserManager(config, self.proxy_manager, self.logger)
        self.stats_manager = StatsManager(config.stats_file)
        self.accounts = self._load_accounts()
        
        # Control variables
        self.running = True
        self.paused = False
        self.current_account = None
        
        # Setup handlers
        self.input_handler = InputHandler(self)
        self.exit_handler = ExitHandler(self)
        self.telegram_handler = TelegramCommandHandler(self)
    
    def pause(self):
        """Pause bot operation"""
        self.paused = True
        self.logger.log("⏸️ Bot paused by user")
    
    def resume(self):
        """Resume bot operation"""
        self.paused = False
        self.logger.log("▶️ Bot resumed by user")
    
    def stop(self):
        """Stop bot gracefully"""
        self.running = False
        self.logger.log("🛑 Bot stopping gracefully...")
    
    def force_quit(self):
        """Force quit immediately"""
        self.logger.log("🚨 Force quit requested - exiting immediately")
        os._exit(0)
    
    def _load_accounts(self) -> List[Tuple[str, str]]:
        """Load account credentials from file"""
        if not os.path.exists(self.config.accounts_file):
            self.logger.log_error(f"Accounts file not found: {self.config.accounts_file}")
            raise FileNotFoundError(f"Accounts file not found: {self.config.accounts_file}")
        
        accounts = []
        with open(self.config.accounts_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if ':' in line:
                    username, password = line.split(':', 1)
                    accounts.append((username, password))
        
        if not accounts:
            raise ValueError("No valid accounts found in accounts file")
        
        random.shuffle(accounts)
        return accounts
    
    def run_session_for_account(self, username: str, password: str) -> int:
        """Run a comment session for a single account"""
        self.current_account = username
        
        # Check if bot is paused
        while self.paused and self.running:
            time.sleep(1)
        
        if not self.running:
            return 0
        
        # Check daily limit
        daily_count = self.stats_manager.get_daily_count(username)
        if daily_count >= self.config.daily_limit_per_account:
            self.logger.log(f"📊 Daily limit reached ({daily_count}/{self.config.daily_limit_per_account}), skipping", username)
            return 0
        
        # Calculate session limit
        remaining = self.config.daily_limit_per_account - daily_count
        session_limit = min(
            random.randint(self.config.min_comments_per_session, self.config.max_comments_per_session), 
            remaining
        )
        
        self.logger.log(f"🚀 Starting session (target: {session_limit} comments, daily: {daily_count}/{self.config.daily_limit_per_account})", username)
        
        bot = InstagramBot(
            username, password, self.config, self.logger, 
            self.cookie_manager, self.browser_manager
        )
        
        comments_made = 0
        
        try:
            if not self.running:
                return 0
                
            bot.start_session()
            
            if not bot.login():
                self.logger.log("❌ Login failed, ending session", username)
                return 0
            
            # Randomly select and shuffle hashtags
            available_hashtags = self.config.hashtags.copy()
            random.shuffle(available_hashtags)
            
            self.logger.log(f"🎯 Processing hashtags: {', '.join(available_hashtags)}", username)
            
            for hashtag in available_hashtags:
                if comments_made >= session_limit or not self.running:
                    break
                
                # Check if paused
                while self.paused and self.running:
                    self.logger.log("⏸️ Session paused, waiting for resume...", username)
                    time.sleep(5)
                
                if not self.running:
                    break
                
                self.logger.log(f"🏷️ Processing hashtag: {hashtag}", username)
                post_links = bot.get_post_links(hashtag)
                
                if not post_links:
                    self.logger.log(f"⚠️ No posts found for {hashtag}, trying next hashtag", username)
                    continue
                
                # Randomly shuffle posts
                random.shuffle(post_links)
                self.logger.log(f"🎲 Shuffled {len(post_links)} posts for random selection", username)
                
                for i, link in enumerate(post_links, 1):
                    if comments_made >= session_limit or not self.running:
                        if comments_made >= session_limit:
                            self.logger.log(f"✅ Session target reached ({comments_made}/{session_limit})", username)
                        break
                    
                    # Check if paused
                    while self.paused and self.running:
                        time.sleep(1)
                    
                    if not self.running:
                        break
                    
                    # Skip duplicates
                    if self.stats_manager.is_duplicate_link(username, link):
                        self.logger.log(f"⏭️ Skipping duplicate post ({i}/{len(post_links)})", username)
                        continue
                    
                    self.logger.log(f"💬 Attempting to comment on post {i}/{len(post_links)}", username)
                    
                    # Attempt to comment
                    result = bot.comment_on_post(link)
                    if result:
                        url, comment = result
                        comments_made += 1
                        
                        # Record the comment
                        self.stats_manager.record_comment(username, hashtag, url, comment)
                        
                        self.logger.log(f"✅ Success! Comment {comments_made}/{session_limit} completed", username)
                        
                        # Wait between comments using configured delay
                        if comments_made < session_limit and self.running:
                            delay = random.randint(
                                self.config.min_delay_between_comments, 
                                self.config.max_delay_between_comments
                            )
                            self.logger.log(f"⏱️ Waiting {delay} seconds before next comment...", username)
                            
                            # Sleep in chunks to allow for interruption
                            for _ in range(delay):
                                if not self.running:
                                    break
                                while self.paused and self.running:
                                    time.sleep(1)
                                if self.running:
                                    time.sleep(1)
                    else:
                        self.logger.log(f"❌ Failed to comment on post {i}/{len(post_links)}", username)
            
            self.logger.log(f"🏁 Session completed! Total comments: {comments_made}/{session_limit}", username)
            
        except Exception as e:
            self.logger.log_error(f"💥 Session error: {e}", username)
        finally:
            bot.close_session()
            self.current_account = None
        
        return comments_made
    
    def run_continuous(self) -> None:
        """Run the bot continuously across all accounts"""
        account_cycle = cycle(self.accounts)
        
        self.logger.log("Starting continuous bot operation")
        self.logger.log(f"Configuration: {len(self.accounts)} accounts, {self.config.daily_limit_per_account} daily limit, {self.config.min_delay_between_comments}-{self.config.max_delay_between_comments}s delays")
        
        # Start input handler
        self.input_handler.start()
        
        # Start Telegram command handler
        self.telegram_handler.start()
        
        try:
            while self.running:
                # Check if paused
                while self.paused and self.running:
                    time.sleep(1)
                
                if not self.running:
                    break
                
                username, password = next(account_cycle)
                self.run_session_for_account(username, password)
                
                # Brief pause between account switches
                for _ in range(5):
                    if not self.running:
                        break
                    while self.paused and self.running:
                        time.sleep(1)
                    if self.running:
                        time.sleep(1)
                        
        except KeyboardInterrupt:
            self.logger.log("Bot stopped by user")
        except Exception as e:
            self.logger.log_error(f"Critical error in main loop: {e}")
        finally:
            self.input_handler.stop()
            self.telegram_handler.stop()
            self.logger.log("Bot operation ended")


def create_sample_config_file():
    """Create a sample configuration file for users"""
    sample_config = {
        "daily_limit_per_account": 200,
        "min_delay_between_comments": 420,
        "max_delay_between_comments": 480,
        "min_comments_per_session": 2,
        "max_comments_per_session": 5,
        "comments_file": "comments.txt",
        "accounts_file": "accounts.txt",
        "chromedriver_path": "chromedriver.exe",
        "log_file": "log.txt",
        "stats_file": "comment_stats.json",
        "cookies_dir": "cookies",
        "proxy_file": "proxyscrape_premium_http_proxies.txt",
        "use_proxy": True,
        "proxy_timeout": 5,
        "max_proxy_latency": 3000,
        "headless_mode": False,
        "telegram_token": "",
        "telegram_chat_id": "",
        "enable_telegram_logging": False,
        "enable_telegram_commands": False,
        "hashtags": ["#freepalestine", "#gazaunderattack", "#savepalestine"],
        "max_posts_per_hashtag": 50,
        "max_scroll_attempts": 3,
        "login_wait_time": 8,
        "post_load_wait_time": 5
    }
    
    try:
        with open('bot_config_sample.json', 'w', encoding='utf-8') as f:
            json.dump(sample_config, f, indent=4, ensure_ascii=False)
        print("✅ Sample configuration file created: bot_config_sample.json")
        print("📝 Edit this file with your settings and rename to 'bot_config.json'")
    except Exception as e:
        print(f"❌ Failed to create sample config: {e}")


def print_usage_help():
    """Print usage instructions"""
    print("""
=== Instagram Bot - Educational Version ===

USAGE OPTIONS:
1. python main.py --setup          - Interactive configuration setup
2. python main.py --create-config  - Create sample configuration file
3. python main.py --help          - Show this help
4. python main.py                 - Run bot with current configuration

CONFIGURATION FILES:
- bot_config.json                  - Main configuration (auto-created from setup)
- bot_config_sample.json          - Sample configuration template
- comments.txt                     - Your comment templates (one per line)
- accounts.txt                 - Account credentials (username:password format)
- proxyscrape_premium_http_proxies.txt - Proxy list (optional)

KEY CONFIGURABLE OPTIONS:
📊 Limits & Timing:
   - daily_limit_per_account       - Max comments per account per day
   - min/max_delay_between_comments - Wait time between comments (seconds)
   - min/max_comments_per_session  - Comments per session range

📁 File Paths:
   - comments_file                 - Path to comments file
   - accounts_file                 - Path to accounts file
   - proxy_file                    - Path to proxy file
   - chromedriver_path             - Path to ChromeDriver executable

🌐 Network & Browser:
   - use_proxy                     - Enable/disable proxy rotation
   - proxy_timeout                 - Proxy connection timeout (seconds)
   - max_proxy_latency            - Skip proxies slower than this (ms)
   - headless_mode                 - Run browser in background
   
📱 Telegram Notifications:
   - telegram_token                - Bot token (leave empty to disable)
   - telegram_chat_id              - Chat ID for notifications
   - enable_telegram_commands      - Remote control via Telegram

🏷️ Targeting:
   - hashtags                      - List of hashtags to target

FIRST TIME SETUP:
1. Run: python main.py --setup
2. Follow the interactive prompts
3. Your settings will be saved to bot_config.json
4. Run: python main.py to start

INTERACTIVE COMMANDS (while bot is running):

🖥️ Console Commands:
- 'status' - Show current bot status and configuration
- 'stats'  - Display today's comment statistics per account
- 'pause'  - Pause bot operation (can be resumed)
- 'resume' - Resume paused bot operation
- 'stop'   - Stop bot gracefully (completes current session)
- 'quit'   - Force quit immediately
- 'help'   - Show available commands

📱 Telegram Commands (if enabled):
- /status  - Show current bot status and configuration
- /stats   - Display today's comment statistics per account
- /pause   - Pause bot operation (can be resumed)
- /resume  - Resume paused bot operation
- /stop    - Stop bot gracefully (completes current session)
- /help    - Show available Telegram commands

EXAMPLE FILES NEEDED:
- comments.txt: "Great post! 🔥", "Amazing content!", "Love this! ❤️"
- accounts.txt: "username1:password1", "username2:password2"
- proxyscrape_premium_http_proxies.txt: "192.168.1.1:8080", "10.0.0.1:3128"
""")


def main():
    """Main entry point with command line argument handling"""
    import sys
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h', 'help']:
            print_usage_help()
            return
        
        elif arg in ['--setup', '-s', 'setup']:
            print("🔧 Starting interactive configuration setup...")
            config = BotConfig()
            config.interactive_setup()
            return
        
        elif arg in ['--create-config', '-c', 'create-config']:
            create_sample_config_file()
            return
        
        else:
            print(f"Unknown argument: {arg}")
            print("Use --help for usage instructions")
            return
    
    # Load configuration and run bot
    try:
        # Try to load existing config file
        config = BotConfig.load_from_file()
        
        # Validate essential files exist
        missing_files = []
        if not os.path.exists(config.comments_file):
            missing_files.append(config.comments_file)
        if not os.path.exists(config.accounts_file):
            missing_files.append(config.accounts_file)
        if not os.path.exists(config.chromedriver_path):
            missing_files.append(config.chromedriver_path)
        
        if missing_files:
            print(f"❌ Missing required files: {', '.join(missing_files)}")
            print("💡 Run 'python main.py --setup' for initial configuration")
            print("💡 Run 'python main.py --help' for detailed instructions")
            return
        
        # Check proxy file if proxy is enabled
        if config.use_proxy and not os.path.exists(config.proxy_file):
            print(f"⚠️ Warning: Proxy enabled but file not found: {config.proxy_file}")
            use_without_proxy = input("Continue without proxy? (y/n): ").lower()
            if use_without_proxy != 'y':
                return
            config.use_proxy = False
        
        # Display current configuration
        print("📋 Current Configuration:")
        print(f"   📊 Daily limit per account: {config.daily_limit_per_account}")
        print(f"   ⏱️ Delay between comments: {config.min_delay_between_comments}-{config.max_delay_between_comments}s")
        print(f"   💬 Comments per session: {config.min_comments_per_session}-{config.max_comments_per_session}")
        print(f"   🌐 Proxy usage: {'✅ Enabled' if config.use_proxy else '❌ Disabled'}")
        print(f"   👁️ Headless mode: {'✅ Enabled' if config.headless_mode else '❌ Disabled'}")
        print(f"   📱 Telegram notifications: {'✅ Enabled' if config.enable_telegram_logging else '❌ Disabled'}")
        print(f"   📱 Telegram remote control: {'✅ Enabled' if config.enable_telegram_commands else '❌ Disabled'}")
        print(f"   🏷️ Target hashtags: {', '.join(config.hashtags)}")
        print()
        
        # Confirm start
        confirm = input("Start the bot with these settings? (y/n): ").lower()
        if confirm != 'y':
            print("🔧 Run 'python main.py --setup' to modify configuration")
            return
        
        # Start the bot
        orchestrator = BotOrchestrator(config)
        orchestrator.run_continuous()
        
    except FileNotFoundError as e:
        print(f"❌ Configuration file not found: {e}")
        print("💡 Run 'python main.py --setup' for initial setup")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("💡 Run 'python main.py --help' for troubleshooting")


if __name__ == "__main__":
    main()