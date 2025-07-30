# bots/youtube_bot.py
import os
import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from utils.proxy_auth_plugin import create_proxy_auth_extension

class YouTubeBot:
    def __init__(self, url, action, proxy=None, delay_range=(35, 45), headless=False):
        self.url = url
        self.action = action
        self.proxy = proxy
        self.delay_range = delay_range
        self.headless = headless
        self.driver = None

    def setup_driver(self):
        options = Options()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_argument("--mute-audio")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,800")
        if self.headless:
            options.add_argument("--headless=new")

        if self.proxy and len(self.proxy.split(":")) == 4:
            host, port, user, pw = self.proxy.split(":")
            plugin_path = create_proxy_auth_extension(host, port, user, pw)
            options.add_extension(plugin_path)
        elif self.proxy and ":" in self.proxy:
            options.add_argument(f'--proxy-server={self.proxy}')

        driver_path = os.path.join(os.getcwd(), "chromedriver.exe")
        self.driver = webdriver.Chrome(service=Service(driver_path), options=options)

    def run(self):
        try:
            self.setup_driver()
            self.driver.get(self.url)
            time.sleep(3)
            self.simulate_human_behavior()

            if self.action == "view":
                self.simulate_view()
            elif self.action == "like":
                self.simulate_like()
            elif self.action == "share":
                self.simulate_share()
        except Exception as e:
            logging.error(f"Error in YouTubeBot: {e}")
        finally:
            if self.driver:
                self.driver.quit()

    def simulate_human_behavior(self):
        try:
            self.driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(2)
            self.driver.execute_script("window.scrollBy(0, -300);")
            time.sleep(1)
        except Exception as e:
            logging.warning("Human behavior simulation failed: " + str(e))

    def simulate_view(self):
        logging.info("Simulating view...")
        try:
            time.sleep(3)
            page_title = self.driver.title
            logging.info(f"📄 Page title: {page_title}")
            self.driver.save_screenshot("screen_after_load.png")

            video = None
            for _ in range(10):
                try:
                    video = self.driver.find_element(By.TAG_NAME, "video")
                    break
                except:
                    time.sleep(1)

            if not video:
                logging.error("❌ Video tag not found.")
                return

            self.driver.execute_script("arguments[0].muted = true; arguments[0].play();", video)
            wait_time = random.uniform(*self.delay_range)
            logging.info(f"▶️ Watching video for {int(wait_time)} seconds...")
            time.sleep(wait_time)

        except Exception as e:
            logging.error("❌ Error while simulating view: " + str(e))

    def simulate_like(self):
        try:
            time.sleep(3)
            like_button = self.driver.find_element(By.XPATH, "//ytd-toggle-button-renderer[1]//button")
            like_button.click()
            logging.info("👍 Like button clicked.")
            time.sleep(2)
        except Exception as e:
            logging.error("❌ Error while simulating like: " + str(e))

    def simulate_share(self):
        try:
            time.sleep(3)
            share_button = self.driver.find_element(By.XPATH, "//ytd-button-renderer[@id='share-button']//a")
            share_button.click()
            logging.info("🔗 Share button clicked.")
            time.sleep(2)
        except Exception as e:
            logging.error("❌ Error while simulating share: " + str(e))
