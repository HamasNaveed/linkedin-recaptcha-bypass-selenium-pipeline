from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
options = Options()
options.add_argument("--start-maximized")  # Optional

# Point to the path where you saved chromedriver.exe
driver_path = r"D:\University\Personals\Intership\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Setup service and driver
service = Service(driver_path)
browser = webdriver.Chrome(service=service, options=options)

# Open Google Sheets
url = "https://www.youtube.com/"
browser.get(url)

# Wait and close
time.sleep(5)
browser.quit()
