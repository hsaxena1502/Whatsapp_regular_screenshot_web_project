import os
import time
import json
import socket
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import WebDriverException

HUB_HOST = os.getenv('SELENIUM_HUB_HOST', '127.0.0.1')
GRID_URL = f"http://{HUB_HOST}:4444"     # use root path on Selenium 4
STATUS_URL = f"{GRID_URL}/status"

def wait_grid_ready(timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(STATUS_URL, timeout=5)
            if r.status_code == 200 and r.json().get("value", {}).get("ready"):
                print("✅ Selenium Grid is ready")
                return True
        except requests.RequestException:
            pass
        print("…waiting for Grid…")
        time.sleep(1)
    raise RuntimeError("Grid not ready within timeout")

def create_remote_driver(browser: str):
    if browser.lower() == "chrome":
        opts = ChromeOptions()
        # Remove headless if you want to VNC into the session
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1920,1080")

        # Do NOT force browserVersion; let Grid match the node
        # Common cross-browser caps:
        opts.set_capability("platformName", "linux")
        opts.set_capability("acceptInsecureCerts", True)
        return webdriver.Remote(command_executor=GRID_URL, options=opts)

    elif browser.lower() == "firefox":
        opts = FirefoxOptions()
        opts.add_argument("-headless")
        opts.add_argument("--width=1920")
        opts.add_argument("--height=1080")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")

        # Set Firefox-specific capabilities
        opts.set_capability("browserName", "firefox")
        opts.set_capability("platformName", "linux")
        opts.set_capability("acceptInsecureCerts", True)
        
        # Increase session timeout
        opts.set_capability("se:timeZone", "UTC")
        opts.set_capability("se:timeout", {"implicit": 30000, "pageLoad": 300000, "script": 30000})
        
        return webdriver.Remote(
            command_executor=GRID_URL,
            options=opts,
            keep_alive=True
        )

    else:
        raise ValueError("Unsupported browser")

def smoke(browser: str):
    print(f"\n--- {browser} ---")
    drv = create_remote_driver(browser)
    try:
        drv.set_page_load_timeout(30)
        drv.implicitly_wait(10)
        drv.set_script_timeout(30)

        url = "https://www.google.com"
        drv.get(url)
        print("Title:", drv.title[:60])
        drv.save_screenshot(f"{browser.lower()}_screenshot.png")
        print("✅ Screenshot saved")
    finally:
        drv.quit()
        print("✅ Closed", browser)

def main():
    wait_grid_ready()
    smoke("Chrome")
    smoke("Firefox")
    print("\nAll good ✅")

if __name__ == "__main__":
    main()
