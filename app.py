from flask import Flask, request, jsonify
from ytmusicapi import YTMusic
import yt_dlp

app = Flask(__name__)
ytmusic = YTMusic()

def search_and_play(query):
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

@app.route('/get_stream_link', methods=['GET'])
def get_stream_link():
    song_name = request.args.get('song_name')
    if not song_name:
        return jsonify({'error': 'No song name provided'}), 400
    
    stream_url = search_and_play(song_name)
    
    if not stream_url:
        return jsonify({'error': 'Song not found'}), 404
    
    return jsonify({'stream_url': stream_url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
