from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    # Render index.html ibikwa muri templates/
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get('url')
    quality = data.get('quality')

    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    # Aha wateza imbere logic yawe yo gukora download link
    # Ubu ni urugero gusa rw'igisubizo
    download_link = f"https://example.com/download?video={video_url}&quality={quality}"

    return jsonify({'download_link': download_link})

if __name__ == '__main__':
    # debug=True ituma ubona amakosa mu buryo burambuye igihe hari ikibazo
    app.run(debug=True, host='0.0.0.0', port=5000)
