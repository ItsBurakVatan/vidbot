# gui/interface.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import time
import os
from bots.youtube_bot import YouTubeBot

class VidBotGUI(ctk.CTk):
    def __init__(self, settings, proxy_handler):
        super().__init__()
        self.settings = settings
        self.proxy_handler = proxy_handler
        self.title("VidBot - YouTube View Bot")
        self.geometry("600x650")
        self.resizable(False, False)
        self.success_count = 0
        self.fail_count = 0
        self.create_widgets()

    def create_widgets(self):
        # Video URL
        self.url_label = ctk.CTkLabel(self, text="YouTube Video URL:")
        self.url_label.pack(pady=5)
        self.url_entry = ctk.CTkEntry(self, width=500)
        self.url_entry.pack()

        # Proxy seçme butonu
        self.proxy_button = ctk.CTkButton(self, text="🔍 Select proxies.txt", command=self.select_proxy_file)
        self.proxy_button.pack(pady=5)

        # Delay slider
        self.delay_label = ctk.CTkLabel(self, text="Delay Range (seconds):")
        self.delay_label.pack(pady=5)
        self.delay_value_label = ctk.CTkLabel(self, text="")
        self.delay_value_label.pack()
        self.delay_slider = ctk.CTkSlider(self, from_=10, to=120, number_of_steps=110, command=self.update_delay_label)
        self.delay_slider.set(sum(self.settings.get("delay_range", [60, 80])) // 2)
        self.delay_slider.pack()
        self.update_delay_label(self.delay_slider.get())

        # Views per proxy
        self.count_label = ctk.CTkLabel(self, text="Views per Proxy:")
        self.count_label.pack(pady=5)
        self.count_entry = ctk.CTkEntry(self, width=100)
        self.count_entry.insert(0, str(self.settings.get("views_per_proxy", 2)))
        self.count_entry.pack()

        # Max threads
        self.threads_label = ctk.CTkLabel(self, text="Concurrent Browsers (Threads):")
        self.threads_label.pack(pady=5)
        self.threads_entry = ctk.CTkEntry(self, width=100)
        self.threads_entry.insert(0, str(self.settings.get("max_threads", 5)))
        self.threads_entry.pack()

        # Headless checkbox
        self.headless_var = ctk.BooleanVar(value=self.settings.get("headless_mode", True))
        self.headless_checkbox = ctk.CTkCheckBox(self, text="Headless Mode", variable=self.headless_var)
        self.headless_checkbox.pack(pady=5)

        # Start button
        self.start_button = ctk.CTkButton(self, text="🚀 Start", command=self.start_mass_view)
        self.start_button.pack(pady=10)

        # Log box
        self.log_box = ctk.CTkTextbox(self, width=550, height=160)
        self.log_box.pack(pady=10)
        self.log("VidBot ready.")

        # Stats
        self.stats_label = ctk.CTkLabel(self, text="✅ Success: 0   ❌ Fail: 0")
        self.stats_label.pack(pady=5)

    def select_proxy_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.proxy_handler.proxy_file = file_path
            self.proxy_handler.load_proxies()
            self.log(f"✅ Loaded {len(self.proxy_handler.proxies)} proxies.")

    def update_delay_label(self, value):
        self.delay_value_label.configure(text=f"⏱️ Selected Delay: {int(float(value))} seconds")

    def log(self, message):
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")

    def update_stats(self):
        self.stats_label.configure(text=f"✅ Success: {self.success_count}   ❌ Fail: {self.fail_count}")

    def start_mass_view(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a video URL.")
            return

        try:
            views_per_proxy = int(self.count_entry.get())
            max_threads = int(self.threads_entry.get())
        except:
            messagebox.showerror("Error", "Please enter valid numbers for views and threads.")
            return

        self.success_count = 0
        self.fail_count = 0
        self.update_stats()

        self.log(f"🔁 Starting mass view for: {url} ({views_per_proxy} views/proxy, {max_threads} threads)")
        thread = threading.Thread(target=self.run_mass_view, args=(url, views_per_proxy, max_threads))
        thread.start()

    def run_mass_view(self, url, views_per_proxy, max_threads):
        proxies = self.proxy_handler.proxies
        delay = int(self.delay_slider.get())
        delay_range = [max(1, delay - 5), delay + 5]
        headless = self.headless_var.get()

        if not proxies:
            self.log("❌ No proxies loaded.")
            return

        from concurrent.futures import ThreadPoolExecutor

        def run_bot(proxy, count):
            try:
                self.log(f"▶️ Using proxy: {proxy} | View {count + 1}")
                bot = YouTubeBot(url, "view", proxy, tuple(delay_range), headless=headless)
                bot.run()
                self.success_count += 1
                self.log(f"✅ Finished view with proxy {proxy}")
            except Exception as e:
                self.fail_count += 1
                self.log(f"❌ Failed with proxy {proxy}: {e}")
            self.update_stats()
            time.sleep(2)

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            for proxy in proxies:
                for count in range(views_per_proxy):
                    executor.submit(run_bot, proxy, count)

        self.log("✅ Mass view completed.")
