from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time

def get_cookie(video_page_url):
    ua = UserAgent()
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(f'--user-agent={ua.random}')  # Use a random user agent to avoid detection

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(video_page_url)
        time.sleep(5)  # Allow page to load fully

        cookies = driver.get_cookies()
        return cookies

    finally:
        driver.quit()