from flask import Flask, request, jsonify, send_from_directory
from ytmusicapi import YTMusic
import yt_dlp
import os

app = Flask(__name__, static_folder="static")

ytmusic = YTMusic()

def get_stream_url(query):
    """Search for a song and return the streamable URL."""
    search_results = ytmusic.search(query)
    if not search_results:
        return None

    video_id = search_results[0]['videoId']
    ydl_opts = {
        'format': 'bestaudio/best',
        'extract_audio': True,
        'audio_format': 'mp3',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
        return info['url']

@app.route("/")
def home():
    """Serve the frontend."""
    return send_from_directory("static", "index.html")

@app.route("/stream", methods=["GET"])
def stream():
    """API to get the audio streaming URL."""
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "No song name provided"}), 400

    stream_url = get_stream_url(query)
    if not stream_url:
        return jsonify({"error": "Song not found"}), 404

    return jsonify({"stream_url": stream_url})

if __name__ == "__main__":
    app.run(debug=True)
