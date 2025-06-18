from flask import Flask, request, render_template, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["url"]
        unique_id = str(uuid.uuid4())
        output_path = f"{DOWNLOAD_FOLDER}/{unique_id}.mp4"

        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': output_path
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return f"<h2 style='color:red;'>Error: {str(e)}</h2>"

    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
