import os
from flask import Flask, request, jsonify
from ytmusicapi import YTMusic
import yt_dlp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS if needed

ytmusic = YTMusic()

def search_and_play(query):
    search_results = ytmusic.search(query)
    if not search_results:
        return None
    video_id = search_results[0]['videoId']

    # Configure yt-dlp to use browser cookies from Chrome.
    ydl_opts = {
        'format': 'bestaudio/best',
        'extract_audio': True,
        'audio_format': 'mp3',
        'nocheckcertificate':True  # Change to 'firefox' if using Firefox.
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
        return info['url']

@app.route('/get_stream_link', methods=['GET'])
def get_stream_link():
    try:
        song_name = request.args.get('song_name')
        if not song_name:
            return jsonify({'error': 'No song name provided'}), 400

        stream_url = search_and_play(song_name)
        if not stream_url:
            return jsonify({'error': 'Song not found'}), 404

        return jsonify({'stream_url': stream_url})
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == "__main__":
    # Use the PORT environment variable if provided (common on deployment platforms)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
