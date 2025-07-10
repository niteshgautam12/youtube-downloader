from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['url']
        download_type = request.form.get('type', 'video')
        quality = request.form.get('quality', 'best')

        output_path = os.path.join("downloads", "%(title).100s.%(ext)s")

        ydl_opts = {
            'outtmpl': output_path,
        }

        if download_type == 'audio':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            if quality == 'best':
                format_code = 'bestvideo+bestaudio/best'
            else:
                format_code = f'bestvideo[height<={quality}]+bestaudio/best'

            ydl_opts.update({
                'format': format_code,
                'merge_output_format': 'mp4'
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            if download_type == 'audio':
                filename = filename.rsplit('.', 1)[0] + '.mp3'

        if os.path.exists(filename):
            return send_file(filename, as_attachment=True)

    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)
