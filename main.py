# main.py
import json
import logging
import os
import sys
from gui.interface import VidBotGUI
from proxies.proxy_handler import ProxyHandler

def resource_path(relative_path):
    """PyInstaller uyumlu dosya yolu çözücü"""
    try:
        base_path = sys._MEIPASS  # PyInstaller runtime klasörü
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_settings():
    settings_path = resource_path("config/settings.json")
    with open(settings_path, "r") as file:
        return json.load(file)

def main():
    settings = load_settings()
    proxy_file_path = resource_path(settings["proxy_file"])
    proxy_handler = ProxyHandler(proxy_file_path)
    app = VidBotGUI(settings, proxy_handler)
    app.mainloop()

if __name__ == "__main__":
    # Log klasörü ve ayarı
    os.makedirs(resource_path("logs"), exist_ok=True)
    log_path = resource_path("logs/vidbot.log")
    logging.basicConfig(
        filename=log_path,
        filemode='a',
        format='%(asctime)s | %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    main()
