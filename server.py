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
    quality = data.get("quality", "720")  # default resolution ni 720p

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    # configuration ya yt-dlp
    ydl_opts = {
        "quiet": True,
        "noplaylist": True,
        "skip_download": True,
        # "cookiefile": "cookies.txt",  # shyiraho aho wabitse cookies.txt niba ukoresha authentication
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get("formats", [])

            # Hitamo format ifite height = quality dusabye
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

            # Niba quality dusabye ntiboneka, turebe iya quality iri hejuru iboneka
            if not best_format:
                valid = [
                    f for f in formats
                    if f.get("vcodec") != "none" and f.get("acodec") != "none"
                ]
                valid.sort(key=lambda x: x.get("height") or 0, reverse=True)
                best_format = valid[0] if valid else None

            if not best_format:
                return jsonify({"error": "No video format available"}), 500

            return jsonify({"download_url": best_format.get("url")})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": f"Failed: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
