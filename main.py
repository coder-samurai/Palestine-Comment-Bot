import os
import time
import json
import random
from datetime import datetime
from itertools import cycle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === CONFIGURATION ===
DAILY_LIMIT_PER_ACCOUNT = 200
COMMENTS_FILE = 'comments.txt'
ACCOUNTS_FILE = 'accounts.txt'
CHROMEDRIVER_PATH = 'chromedriver.exe'
HASHTAGS = ['#freepalestine', '#gazaunderattack', '#savepalestine']
LOG_FILE = 'log.txt'
STATS_FILE = 'comment_stats.json'
COOKIES_DIR = 'cookies'
HEADLESS_MODE = False

# === Helper Functions ===
def strip_non_bmp(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

def today():
    return datetime.now().strftime("%Y-%m-%d")

def log_error_to_file(message):
    with open('errors.log', 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now()}] {message}\n")

def save_links_for_account(stats, username, tag, url, comment):
    entry = stats.setdefault(username, {}).setdefault(today(), {})
    entry.setdefault("count", 0)
    entry.setdefault("hashtags", {})
    entry["hashtags"].setdefault(tag, [])
    entry["hashtags"][tag].append({"url": url, "comment": comment})

def is_duplicate_link(stats, username, url):
    account_stats = stats.get(username, {}).get(today(), {}).get("hashtags", {})
    for links in account_stats.values():
        for item in links:
            if item["url"] == url:
                return True
    return False

def save_cookies(driver, username):
    os.makedirs(COOKIES_DIR, exist_ok=True)
    with open(os.path.join(COOKIES_DIR, f"{username}.json"), 'w', encoding='utf-8') as f:
        json.dump(driver.get_cookies(), f)

def load_cookies(driver, username):
    path = os.path.join(COOKIES_DIR, f"{username}.json")
    if not os.path.exists(path):
        return False
    driver.get("https://www.instagram.com")
    with open(path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://www.instagram.com")
    return True

# === Instagram Bot Class ===
class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.visited = set()
        self.comments = self.load_comments()
        self.driver = self.start_browser()

    def log(self, msg):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        line = f"{timestamp} [{self.username}] {msg}"
        print(line)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line + '\n')

    def load_comments(self):
        if not os.path.exists(COMMENTS_FILE):
            print("[X] comments.txt not found")
            exit()
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
            return [strip_non_bmp(l.strip()) for l in f if l.strip()]

    def start_browser(self):
        options = Options()
        if HEADLESS_MODE:
            options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        options.set_capability("pageLoadStrategy", "normal")

        try:
            driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                    window.navigator.chrome = { runtime: {} };
                    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                """
            })
            return driver
        except WebDriverException as e:
            log_error_to_file(f"[X] Failed to start browser: {e}")
            exit()

    def login(self):
        cookies_loaded = False
        cookie_path = os.path.join(COOKIES_DIR, f"{self.username}.json")
        if os.path.exists(cookie_path):
            self.driver.get("https://www.instagram.com/")
            with open(cookie_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.get("https://www.instagram.com/")
            cookies_loaded = True
            time.sleep(3)

        if cookies_loaded and "login" not in self.driver.current_url:
            self.log("✅ Session active, already logged in via cookies.")
            return

        self.log("🔐 Logging in manually...")
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(4)

        try:
            self.driver.find_element(By.NAME, 'username').send_keys(self.username)
            self.driver.find_element(By.NAME, 'password').send_keys(self.password + Keys.RETURN)
            time.sleep(8)

            if "challenge" in self.driver.current_url:
                self.log("⚠️ Challenge or 2FA detected. Exiting...")
                self.driver.quit()
                exit()

            if "accounts/login" in self.driver.current_url:
                self.log("❌ Login failed. Check credentials.")
                self.driver.quit()
                exit()

            save_cookies(self.driver, self.username)
            self.log("✅ Logged in and cookies saved.")

        except Exception as e:
            self.log(f"Login exception: {e}")
            self.driver.quit()
            exit()


    def get_post_links(self, tag):
        try:
            self.driver.get(f'https://www.instagram.com/explore/tags/{tag[1:]}/')
            time.sleep(5)
            for _ in range(2):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            links = self.driver.find_elements(By.TAG_NAME, 'a')
            return list({l.get_attribute('href') for l in links if '/p/' in l.get_attribute('href')})
        except Exception as e:
            self.log(f"Failed to get post links for {tag}: {e}")
            return []

    def comment_on(self, url):
        if url in self.visited:
            return False
        try:
            self.driver.get(url)
            time.sleep(3)

            try:
                icon = self.driver.find_element(By.XPATH, "//svg[@aria-label='Comment']")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", icon)
                icon.click()
                time.sleep(2)
            except NoSuchElementException:
                self.log("No comment icon found. Possibly already open.")
            except Exception as e:
                self.log(f"Error clicking comment icon: {e}")

            comment_box = None
            for attempt in range(5):
                try:
                    comment_box = self.driver.find_element(By.XPATH, "//textarea[@aria-label='Add a comment…']")
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", comment_box)
                    self.driver.execute_script("arguments[0].focus();", comment_box)
                    comment_box.click()
                    time.sleep(1)
                    comment_box = self.driver.find_element(By.XPATH, "//textarea[@aria-label='Add a comment…']")
                    if comment_box.is_displayed() and comment_box.is_enabled():
                        break
                except StaleElementReferenceException as e:
                    self.log(f"[Try {attempt+1}/5] Stale element: retrying...")
                    time.sleep(1)
                except Exception as e:
                    self.log(f"[Try {attempt+1}/5] Failed to locate/focus comment box: {e}")
                    time.sleep(1)

            if not comment_box:
                self.log("❌ Unable to locate comment box after retries.")
                return False

            comment = strip_non_bmp(random.choice(self.comments))

            try:
                comment_box.send_keys(comment)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", comment_box)
            except Exception as e:
                self.log(f"❌ Error typing comment: {e}")
                return False

            time.sleep(1)

            for _ in range(10):
                try:
                    post_btn = self.driver.find_element(By.XPATH, "//div[@role='button' and text()='Post']")
                    if post_btn.is_enabled():
                        post_btn.click()
                        break
                except Exception:
                    time.sleep(0.5)

            time.sleep(2)
            self.visited.add(url)
            self.log(f"✅ Commented on {url} with: {comment}")
            return url, comment

        except TimeoutException:
            self.log("⏱️ Timeout while waiting for comment box.")
            return False
        except Exception as e:
            self.log(f"❌ Failed at {url}: {e}")
            return False


    def close(self):
        self.driver.quit()

# === JSON Utilities ===
def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_stats(stats):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        print(f"[X] File not found: {ACCOUNTS_FILE}")
        exit()
    with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
        accounts = [tuple(line.strip().split(':', 1)) for line in f if ':' in line.strip()]
    random.shuffle(accounts)
    return accounts

# === Main Execution Loop ===
if __name__ == "__main__":
    stats = load_stats()
    accounts = cycle(load_accounts())

    while True:
        username, password = next(accounts)
        used = stats.get(username, {}).get(today(), {}).get("count", 0)
        if used >= DAILY_LIMIT_PER_ACCOUNT:
            print(f"[~] {username} reached daily limit. Skipping...")
            time.sleep(2)
            continue

        limit_this_session = min(random.randint(2, 5), DAILY_LIMIT_PER_ACCOUNT - used)
        print(f"[>] Starting session for {username} (target: {limit_this_session} comments)")

        try:
            bot = InstagramBot(username, password)
            # load_cookies(bot.driver, username)
            bot.login()
            comments_done = 0

            for tag in random.sample(HASHTAGS, len(HASHTAGS)):
                links = bot.get_post_links(tag)
                random.shuffle(links)
                for link in links:
                    if comments_done >= limit_this_session:
                        break
                    if is_duplicate_link(stats, username, link):
                        continue
                    result = bot.comment_on(link)
                    if result:
                        url, comment = result
                        comments_done += 1
                        save_links_for_account(stats, username, tag, url, comment)
                        stats[username][today()]["count"] += 1
                        save_stats(stats)
                        delay = random.randint(420, 480)
                        bot.log(f"Waiting {delay} sec...")
                        time.sleep(delay)

            bot.log(f"Finished session. Comments this session: {comments_done}.")
            bot.close()
        except Exception as e:
            print(f"[X] Fatal error with account {username}: {e}")
            log_error_to_file(f"{username}: {e}")
            continue

        time.sleep(5)
