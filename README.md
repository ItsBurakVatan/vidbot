```markdown
# VidBot – YouTube View Automation Bot

VidBot is a YouTube view automation bot with support for proxy rotation, multithreading, headless Chrome execution, and GUI-based configuration using `customtkinter`.

> ⚠️ This project is intended **for educational and testing purposes only**.

## 🚀 Features

- 🎯 Automated YouTube view simulation
- 🌐 Full proxy support (with and without authentication)
- 🧠 Human-like behavior simulation (scrolling, delays, interaction)
- 🧩 Modular design with proxy handler and GUI interface
- 🔄 Multi-threaded view execution
- 🖥️ GUI interface for configuring delays, proxies, view counts, threads, and mode (headless or not)

## 🧱 Project Structure

```

├── bots/
│   └── youtube\_bot.py          # Core automation logic using Selenium
├── gui/
│   └── interface.py            # customtkinter GUI interface
├── proxies/
│   └── proxy\_handler.py        # Proxy management (load, rotate, shuffle)
├── utils/
│   └── proxy\_auth\_plugin.py    # Creates Chrome extension for proxy auth
├── chromedriver.exe            # Chrome WebDriver (user-provided)
├── requirements.txt            # Python dependencies

````

## ⚙️ Requirements

- Python 3.8+
- Google Chrome installed
- `chromedriver.exe` in root directory (match your Chrome version)

## 📦 Installation

```bash
pip install -r requirements.txt
````

## 🧪 Usage

1. Prepare a `proxies.txt` file with proxies in either of the formats:

   ```
   123.123.123.123:8080
   or
   123.123.123.123:8080:user:password
   ```

2. Run the GUI:

   ```bash
   python gui/interface.py
   ```

3. Enter the YouTube video URL, select `proxies.txt`, set view count and thread number, then click **Start** 🚀

## 👨‍💻 Developer Notes

* Simulates basic human behavior with small scrolls and delays
* View time is randomized between a specified delay range
* Can be configured to run in headless mode

## ⚠️ Disclaimer

This tool is intended for **research and educational purposes only**. Use it responsibly and do not violate YouTube’s Terms of Service or any platform’s policies.

---

**Developed by Burak for automation testing demonstrations.**

```

