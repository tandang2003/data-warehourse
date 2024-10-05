from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

url = 'https://batdongsan.com.vn/nha-dat-cho-thue-an-giang'

# Set up Chrome options (headless, if you don't want a visible browser)
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")
chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering
chrome_options.add_argument("--no-sandbox")  # Sandbox can cause issues in some environments

# Provide the path to the ChromeDriver executable
service = Service('./driver/chromedriver-linux64/chromedriver')

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the webpage
driver.get(url)

# Let JavaScript load by waiting a bit
time.sleep(5)  # Adjust the sleep time based on the page's load time

# Get the page source after JavaScript execution
page_source = driver.page_source

from bs4 import BeautifulSoup

soup = BeautifulSoup(page_source, 'html.parser');

print(soup.prettify());
