from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import yt_dlp

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

@app.route('/')
def home():
    # Serve the main HTML file from the static folder
    return send_from_directory('static', 'index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get("url")
    quality = data.get("quality", "720")  # default 720p

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        "quiet": True,
        "noplaylist": True,
        "skip_download": True,
        # "cookiefile": "cookies.txt",  # Uncomment if you use cookies
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get("formats", [])

            # Find format with exact requested quality and mp4 video + audio
            best_format = None
            for f in formats:
                if (
                    f.get("height") == int(quality)
                    and f.get("vcodec") != "none"
                    and f.get("acodec") != "none"
                    and f.get("ext") == "mp4"
                ):
                    best_format = f
                    break

            # If exact quality not found, fallback to highest available
            if not best_format:
                valid = [
                    f for f in formats
                    if f.get("vcodec") != "none" and f.get("acodec") != "none"
                ]
                valid.sort(key=lambda x: x.get("height") or 0, reverse=True)
                best_format = valid[0] if valid else None

            if not best_format:
                return jsonify({"error": "No suitable video format found"}), 500

            return jsonify({
                "download_url": best_format.get("url"),
                "title": info.get("title", "Video")
            })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": f"Failed to process video: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
