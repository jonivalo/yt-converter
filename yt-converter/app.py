from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import yt_dlp as ytdlp
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            return redirect(url_for('converter'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/converter', methods=['GET', 'POST'])
def converter():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        link = request.form.get('link')
        if not link:
            flash('No URL provided.')
            return redirect(url_for('converter'))

        video_file = download_video(link)
        if video_file:
            mp3_file = convert_to_mp3(video_file)
            if os.path.exists(mp3_file):
                return send_file(mp3_file, as_attachment=True)
            else:
                flash('Error converting video to MP3.')
        else:
            flash('Failed to download video.')
    return render_template('converter.html')

def download_video(link, path='.'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            return os.path.join(path, f"{info_dict['title']}.mp3")
    except Exception as e:
        print(f"Error occurred while downloading video: {e}")
        return None

def convert_to_mp3(video_file, path='.'):
    return video_file

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
