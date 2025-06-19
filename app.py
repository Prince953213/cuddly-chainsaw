from flask import Flask, request, render_template, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")

@app.route("/api/download", methods=["POST"])
def download_video():
    data = request.json
    url = data.get("url")

    if not url or not url.startswith("http"):
        return jsonify({"error": "Invalid or missing URL"}), 400

    unique_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.mp4")

    ydl_opts = {
        "format": "best[ext=mp4]",
        "outtmpl": output_path,
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        filename = os.path.basename(output_path)
        return jsonify({"status": "success", "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
