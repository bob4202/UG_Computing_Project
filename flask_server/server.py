from flask import Flask, request, jsonify, redirect,session
from analyze import Analyze
from spotify import Spotify
import requests, urllib
from flask_cors import CORS
from werkzeug.utils import secure_filename
import datetime
import os

app = Flask(__name__)
app.secret_key ="6A464BA81846E"
CORS(app)  # Enable CORS for all routes

CLIENT_ID = "936de7b258614e848dc30cdbe159ad0f"
CLIENT_SECRET = "f7d53bbf159c4a60a8df92fdc7250c04"

# FILE_PATH = "./uploads/"

spotify = Spotify(CLIENT_ID,CLIENT_SECRET)
# analyze = Analyze(FILE_PATH)


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/login')
def login():
    auth_url = spotify.get_authorize_url()
    return redirect(auth_url)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file = file.save(filepath)
            return jsonify({'message': 'File uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    if 'spotify_token_info' not in session:
        return redirect('/login')
    
    token_info = session['spotify_token_info']
    if spotify.is_token_expired(token_info):
        token_info = spotify.refresh_access_token(token_info['refresh_token'])
        
    user_top_artists = spotify.final_data()
    # Use token_info['access_token'] to make requests to Spotify API

    return jsonify(user_top_artists)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = spotify.get_access_token(code)
    session['spotify_token_info'] = token_info
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
