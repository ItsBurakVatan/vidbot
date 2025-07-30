# proxies/proxy_handler.py
import random
import os
import sys

def resource_path(relative_path):
    try:
        return os.path.join(sys._MEIPASS, relative_path)
    except:
        return os.path.abspath(relative_path)

class ProxyHandler:
    def __init__(self, proxy_file):
        self.proxy_file = proxy_file
        self.proxies = []
        self.index = 0
        self.load_proxies()

    def load_proxies(self):
        try:
            path = resource_path(self.proxy_file)
            with open(path, 'r') as file:
                self.proxies = [line.strip() for line in file if line.strip()]
            random.shuffle(self.proxies)
        except FileNotFoundError:
            print(f"Proxy file not found: {self.proxy_file}")
            self.proxies = []

    def get_next_proxy(self):
        if not self.proxies:
            return None
        proxy = self.proxies[self.index]
        self.index = (self.index + 1) % len(self.proxies)
        return proxy
