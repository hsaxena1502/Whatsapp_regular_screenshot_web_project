from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from datetime import datetime
import os
import time
from threading import Thread

# Selenium Grid URL (use service name from docker-compose)
GRID_URL = "http://selenium-hub:4444/wd/hub"

# Folder for screenshots inside container
screenshot_folder = "/app/Utilities/screenshots"
os.makedirs(screenshot_folder, exist_ok=True)

# Wait for hub to be ready
time.sleep(5)

def take_screenshot(browser_name):
    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    else:
        options = FirefoxOptions()
        options.add_argument("--headless")

    driver = webdriver.Remote(
        command_executor=GRID_URL,
        options=options
    )

    driver.get("https://web.whatsapp.com")
    time.sleep(15)  # wait for login QR scan

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(screenshot_folder, f"whatsapp_{browser_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"{browser_name} screenshot saved: {path}")

    driver.quit()

# Create threads for Chrome and Firefox
threads = []
for browser in ["chrome", "firefox"]:
    t = Thread(target=take_screenshot, args=(browser,))
    t.start()
    threads.append(t)

# Wait for both threads to finish
for t in threads:
    t.join()
