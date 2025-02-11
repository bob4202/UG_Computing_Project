from flask import Flask, request, jsonify, redirect, session, send_from_directory
from analyze import Analyze
from spotify import Spotify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "APP-SECRET-KEY"
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem session storage
CORS(app)  # Enable CORS for all routes

CLIENT_ID = "YOUR-CLIENT-ID-FROM-SPOTIFY"
CLIENT_SECRET = "YOUR-CLIENT-SECRET-FROM-SPOTIFY"

spotify = Spotify(CLIENT_ID, CLIENT_SECRET)
analyze = Analyze()  # Instantiate Analyze class

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


temp_emotion = {
    'user_emotion': None
}

@app.route('/login')
def login():
    auth_url = spotify.get_authorize_url()
    return redirect(auth_url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    global user_emotion
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            emotion_result = analyze.analyze_emotion(filepath)
            temp_emotion['user_emotion'] = emotion_result
            user_emotion = emotion_result  # Store emotion in session
            print(f"Emotion stored in session: {user_emotion}")  # Debug print
            file_url = f"http://127.0.0.1:5000/uploads/{filename}"  # URL to access the uploaded file
            print(file_url)
            return jsonify({'message': 'File uploaded successfully', 'emotion': emotion_result, 'file_url': file_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    if 'spotify_token_info' not in session:
        return redirect('/login')
    token_info = session['spotify_token_info']
    if spotify.is_token_expired(token_info):
        token_info = spotify.refresh_access_token(token_info['refresh_token'])
    emotion = temp_emotion['user_emotion']
    print(emotion)
    print(f"Emotion retrieved from session: {emotion}")  # Debug print
    user_top_artists = spotify.final_data(emotion)  # Pass emotion to final_data()
    # Use token_info['access_token'] to make requests to Spotify API

    return redirect('/display')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = spotify.get_access_token(code)
    session['spotify_token_info'] = token_info
    return redirect('/')

@app.route('/display')
def display():
    return redirect("http://localhost:3000/display")

@app.route('/delete_photo', methods=['POST'])
def delete_photo():
    try:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.remove(file_path)
        return redirect('/playlist')  # Redirect to the Spotify playlist page
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/playlist')
def show_playlist():
    try:
        # Delete the uploaded file
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.remove(file_path)

        # Redirect to Spotify playlist URL
        playlist_id = spotify.playlist_id
        if playlist_id:
            playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
            return redirect(playlist_url)
        else:
            return jsonify({'error': 'Playlist ID not found'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/get_emotion', methods=['GET'])
def get_emotion():
    emotion = temp_emotion['user_emotion']
    return jsonify({'emotion': emotion})


if __name__ == '__main__':
    app.run(debug=True)
