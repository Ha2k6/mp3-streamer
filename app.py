from flask import Flask, request, jsonify, send_from_directory, Response
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
        'outtmpl': '/tmp/%(id)s.%(ext)s'  # Save to temporary directory
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
        audio_file_path = f"/tmp/{info['id']}.mp3"
        return audio_file_path

def generate_audio_stream(audio_file_path):
    """Stream the audio file to the client."""
    with open(audio_file_path, 'rb') as f:
        while chunk := f.read(1024):
            yield chunk

@app.route("/")
def home():
    """Serve the frontend."""
    return send_from_directory("static", "index.html")

@app.route("/stream", methods=["GET"])
def stream():
    """API to stream the audio."""
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "No song name provided"}), 400

    # Get the path to the audio file
    audio_file_path = get_stream_url(query)
    if not audio_file_path:
        return jsonify({"error": "Song not found"}), 404

    # Stream the audio file
    return Response(generate_audio_stream(audio_file_path), content_type="audio/mp3")

if __name__ == "__main__":
    app.run(debug=True)
￼Enter
