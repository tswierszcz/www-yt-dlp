from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
import subprocess
import threading
import configparser
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class URLForm(FlaskForm):
    url = StringField('YouTube URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Download')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
download_folder = config['settings']['download_folder']

# List to store information about current downloads
current_downloads = []

def download_video(url, download_folder):
    video_info = {'url': url, 'status': 'downloading'}
    current_downloads.append(video_info)
    command = ['yt-dlp', '-o', os.path.join(download_folder, '%(title)s.%(ext)s'), url]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        video_info['status'] = 'completed'
        print(f'Download completed: {result.stdout}')
    except subprocess.CalledProcessError as e:
        video_info['status'] = 'failed'
        print(f'Failed to download video: {e.stderr}')
    finally:
        current_downloads.remove(video_info)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url = form.url.data
        download_thread = threading.Thread(target=download_video, args=(url, download_folder))
        download_thread.start()
        flash('Download started successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, current_downloads=current_downloads)

@app.route('/status', methods=['GET'])
def status():
    return jsonify(current_downloads)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
