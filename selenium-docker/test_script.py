from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time

# Selenium Grid URL (Hub)
GRID_URL = "http://selenium-hub:4444/wd/hub"

# ----- Chrome -----
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")  # Remove if you want GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver_chrome = webdriver.Remote(
    command_executor=GRID_URL,
    options=chrome_options
)

driver_chrome.get("https://www.google.com")
print("Chrome title:", driver_chrome.title)

# ----- Firefox -----
firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")  # Remove if you want GUI

driver_firefox = webdriver.Remote(
    command_executor=GRID_URL,
    options=firefox_options
)

driver_firefox.get("https://www.google.com")
print("Firefox title:", driver_firefox.title)

# ----- Close browsers -----
driver_chrome.quit()
driver_firefox.quit()
