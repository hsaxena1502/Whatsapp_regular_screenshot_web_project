import os
import time
import json
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HUB_HOST = os.getenv('SELENIUM_HUB_HOST', '127.0.0.1')
GRID_URL = f"http://{HUB_HOST}:4444"
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
    browser = browser.lower()
    if browser == "chrome":
        opts = ChromeOptions()
        # Remove headless to use VNC; keep headless for speed/CI
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1920,1080")

        # Common W3C capabilities
        opts.set_capability("platformName", "linux")
        opts.set_capability("acceptInsecureCerts", True)
        # (optional) W3C timeouts in ms
        opts.set_capability("timeouts", {"implicit": 10000, "pageLoad": 30000, "script": 30000})

        return webdriver.Remote(command_executor=GRID_URL, options=opts)

    elif browser == "firefox":
        opts = FirefoxOptions()
        opts.add_argument("-headless")
        opts.add_argument("--width=1920")
        opts.add_argument("--height=1080")
        # Do NOT add Chrome-only flags to Firefox

        opts.set_capability("platformName", "linux")
        opts.set_capability("acceptInsecureCerts", True)
        opts.set_capability("timeouts", {"implicit": 10000, "pageLoad": 60000, "script": 30000})

        return webdriver.Remote(command_executor=GRID_URL, options=opts)

    else:
        raise ValueError("Unsupported browser")

def smoke(browser: str):
    print(f"\n--- {browser} ---")
    drv = create_remote_driver(browser)
    try:
        # Redundant with W3C timeouts above, but fine to keep
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

def monitor_whatsapp_login(browser_name="Firefox", duration_minutes=20, screenshot_interval=30):
    """
    Open WhatsApp Web, wait for QR, take periodic screenshots.
    """
    print(f"\n--- Starting WhatsApp Web monitoring with {browser_name} ---")
    driver = create_remote_driver(browser_name)
    screenshot_count = 0
    screenshot_dir = ""  # Initialize with empty string
    try:
        driver.set_page_load_timeout(60)
        driver.implicitly_wait(10)

        print("Opening WhatsApp Web...")
        driver.get("https://web.whatsapp.com/")

        print("Waiting for QR code to load...")
        wait = WebDriverWait(driver, 60)

        # Try your original selector first, then fall back
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas[aria-label="Scan me!"]')))
        except TimeoutException:
            # Fallback selector (WhatsApp sometimes changes attributes)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="qrcode"] canvas')))

        print("QR code detected. Starting screenshot capture...")

        # Ensure screenshots directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        screenshot_dir = os.path.join(base_dir, "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        end_time = time.time() + duration_minutes * 60

        # Optional warm-up: avoid first headless blank capture delays
        driver.get("about:blank")
        driver.get("https://web.whatsapp.com/")

        while time.time() < end_time:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(
                screenshot_dir, f"whatsapp_{browser_name.lower()}_{timestamp}.png"
            )
            driver.save_screenshot(screenshot_path)
            screenshot_count += 1
            print(f"Screenshot {screenshot_count} saved: {screenshot_path}")

            wait_time = min(float(screenshot_interval), end_time - time.time())
            if wait_time > 0:
                time.sleep(wait_time)
            else:
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        print(f"\nMonitoring completed. {screenshot_count} screenshots were saved to {screenshot_dir}")

def main():
    wait_grid_ready()
    # Quick smoke (optional)
    # smoke("Chrome")
    # smoke("Firefox")
    monitor_whatsapp_login(browser_name="Firefox", duration_minutes=20)
    print("\nAll good ✅")

if __name__ == "__main__":
    main()
