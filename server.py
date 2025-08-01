from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get("url")
    quality = data.get("quality", "720")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'noplaylist': True,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])

            best_format = None
            for f in formats:
                if (
                    f.get('height') == int(quality)
                    and f.get('vcodec') != 'none'
                    and f.get('acodec') != 'none'
                    and f.get('ext') == 'mp4'
                ):
                    best_format = f
                    break

            if not best_format:
                valid_formats = [
                    f for f in formats
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none'
                ]
                valid_formats.sort(key=lambda x: x.get('height') or 0, reverse=True)
                best_format = valid_formats[0] if valid_formats else None

            if not best_format:
                return jsonify({"error": "No video format available for the requested resolution"}), 500

            video_direct_url = best_format.get('url')
            return jsonify({"download_url": video_direct_url})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed: " + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
