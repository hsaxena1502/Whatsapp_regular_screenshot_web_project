import os
import time
from datetime import datetime
from selenium import webdriver

# ✅ Set Chrome profile path (Change this to your actual profile path)
chrome_profile_path = os.path.expanduser("~/Library/Application Support/Google/Chrome/Profile 1")

# ✅ Ensure screenshot folder exists
screenshot_folder = os.path.expanduser("~/Desktop/WhatsApp_Screenshots")
os.makedirs(screenshot_folder, exist_ok=True)

# ✅ Set Chrome options to use the existing profile
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={chrome_profile_path}")  # Use existing Chrome profile
options.add_argument("--profile-directory=Default")  # Adjust if needed

# ✅ Start WebDriver
driver = webdriver.Chrome(options=options)

# Open WhatsApp Web (it should already be logged in)
driver.get("https://web.whatsapp.com")
time.sleep(10)  # Wait for page to load

print(f"✅ WhatsApp Web opened. Saving screenshots to: {screenshot_folder}")

# ✅ Take screenshots every 1 minute
while True:
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(screenshot_folder, f"whatsapp_{timestamp}.png")

        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")

        time.sleep(16)  # Wait for 1 minute

    except Exception as e:
        print(f"❌ Error: {e}")
        break
