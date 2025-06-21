from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time

def clean_video_url(video_page_url):
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

        # Optional: Handle CAPTCHA manually by logging in first and exporting cookies

        video_url = driver.current_url  # Get actual video URL (in most cases it's unchanged)

        return video_url

    finally:
        driver.quit()