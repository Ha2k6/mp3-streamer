from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import yt_dlp
import time

app = Flask(__name__)

def search_and_get_url(query):
    try:
        # Setup Selenium headless browser
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Open YouTube and search
        driver.get("https://www.youtube.com/")
        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)  # Wait for results to load

        # Get first video link
        video_links = driver.find_elements(By.XPATH, '//a[@id="video-title"]')
        if not video_links:
            driver.quit()
            return None, "No results found"

        video_url = "https://www.youtube.com" + video_links[0].get_attribute("href")
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
        return None, str(e)

@app.route('/get_song', methods=['GET'])
def get_song():
    query = request.args.get("song")
    if not query:
        return jsonify({"error": "Missing song name"}), 400

    stream_url, error = search_and_get_url(query)
    if error:
        return jsonify({"error": error}), 500

    return jsonify({"song_url": stream_url})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
