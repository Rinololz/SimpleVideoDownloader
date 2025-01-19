from flask import Flask, request, send_file
import yt_dlp
import os
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')  # Serve the index.html page when visiting /

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(os.path.expanduser('~'), 'Downloads', '%(title).50s.%(ext)s'),  # Save to default Downloads folder
        'restrict_filenames': True,  # Enable filename restrictions
        'ffmpeg_location': './ffmpeg_files/',  # Point to the bundled ffmpeg files
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_file = ydl.prepare_filename(info_dict)
    
    # Send the file to the user
    response = send_file(video_file, as_attachment=True)
    
    return response

if __name__ == '__main__':
    # Open the browser automatically at the start
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(host='127.0.0.1', port=5000)
