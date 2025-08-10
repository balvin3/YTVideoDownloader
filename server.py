from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

# Check if cookies.txt exists
COOKIES_FILE = "cookies.txt"
if os.path.exists(COOKIES_FILE):
    print("✅ Cookies found: Using cookies.txt")
    use_cookies = True
else:
    print("⚠️ No cookies.txt found: Continuing without cookies")
    use_cookies = False

@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        "format": "best",
        "outtmpl": "%(title)s.%(ext)s"
    }

    # Add cookies if available
    if use_cookies:
        ydl_opts["cookiefile"] = COOKIES_FILE

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "title": info.get("title", "Unknown Title"),
                "url": info.get("url", "")
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
