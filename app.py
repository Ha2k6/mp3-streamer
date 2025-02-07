from flask import Flask, request, jsonify
from ytmusicapi import YTMusic
import yt_dlp
import os

app = Flask(__name__)

# Load YouTube Music API
ytmusic = YTMusic()

# Get cookies from environment variable
cookies_string = os.getenv("YOUTUBE_COOKIES")

# If cookies exist, save them to a file
if cookies_string:
    with open("cookies.txt", "w") as f:
        f.write(cookies_string)

# Function to search and get a streamable link
def search_and_play(query):
    search_results = ytmusic.search(query)

    if not search_results:
        return {"error": "No results found"}

    video_id = search_results[0]['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    # yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'nocheckcertificate': True,
        'extract_audio': True,
        'cookies': "cookies.txt" if cookies_string else None,  # Use cookies if available
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return {"stream_url": info['url']}
    except Exception as e:
        return {"error": str(e)}

@app.route('/get_stream_link', methods=['GET'])
def get_stream_link():
    song_name = request.args.get('song_name')

    if not song_name:
        return jsonify({"error": "Missing 'song_name' parameter"}), 400

    result = search_and_play(song_name)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
