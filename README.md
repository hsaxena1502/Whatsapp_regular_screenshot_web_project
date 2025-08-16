import os
import time
import datetime



# WhatsApp Web Screenshot Automation




A simple Python script that automates taking periodic screenshots of WhatsApp Web using Selenium.

## Features

- Takes screenshots of WhatsApp Web at regular intervals
- Uses an existing Chrome profile to maintain login session
- Saves screenshots with timestamps for easy tracking
- Runs continuously until stopped

## Prerequisites

- Python 3.6+
- Google Chrome browser installed
- Chrome WebDriver (compatible with your Chrome version)
- Required Python packages:
  - selenium

## Installation

1. Clone this repository or download the script:
   ```bash
   git clone <repository-url>
   cd pythonProject1
   ```

2. Install the required Python packages:
   ```bash
   pip install selenium
   ```

3. Download the appropriate Chrome WebDriver for your Chrome version from:
   https://sites.google.com/chromium.org/driver/

## Configuration

1. Update the Chrome profile path in `Utilities/common.py` if needed:
   ```python
import os
chrome_profile_path = os.path.expanduser("~/Library/Application Support/Google/Chrome/Profile 1")
```

2. (Optional) Change the screenshot save location:
   ```python
import os
screenshot_folder = os.path.expanduser("~/Desktop/WhatsApp_Screenshots")
```

3. (Optional) Adjust the screenshot interval (in seconds):
   ```python
import time
time.sleep(16)  # Current interval is 16 seconds
```

## Usage

1. Make sure WhatsApp Web is logged in on your Chrome profile
2. Run the script:
   ```bash
   python Utilities/common.py
   ```
3. The script will start taking screenshots and save them to the specified folder
4. To stop the script, press `Ctrl+C` in the terminal

## Notes

- The script uses your existing Chrome profile to maintain the WhatsApp Web session
- Screenshots are saved with timestamps in the filename
- The default screenshot location is `~/Desktop/WhatsApp_Screenshots/`
- Make sure Chrome is not running when you start the script

## Troubleshooting

- If you get a WebDriver error, make sure you have the correct Chrome WebDriver version installed
- Ensure the Chrome profile path in the script matches your system
- If screenshots are not being saved, check if the destination folder has write permissions

## License

This project is open source and available under the [MIT License](LICENSE).
