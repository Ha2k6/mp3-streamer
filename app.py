import os
import time
import yt_dlp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller

# Set Chrome binary path manually
CHROME_PATH = "/usr/bin/google-chrome-stable"
CHROMEDRIVER_PATH = chromedriver_autoinstaller.install()

def search_and_get_url(query):
    try:
        print(f"Searching for: {query}")

        # Setup Selenium
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = CHROME_PATH

        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)

        print("Opened browser...")

        driver.get("https://www.youtube.com/")
        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        video_links = driver.find_elements(By.XPATH, '//a[@id="video-title"]')
        if not video_links:
            print("No video found")
            driver.quit()
            return None, "No results found"

        video_url = "https://www.youtube.com" + video_links[0].get_attribute("href")
        print(f"Found video: {video_url}")

        driver.quit()

        # Extract streamable URL using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extract_audio': True,
            'audio_format': 'mp3',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return info.get('url'), None
    except Exception as e:
        print(f"Error: {e}")
        return None, str(e)
