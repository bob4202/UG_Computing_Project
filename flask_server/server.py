from flask import Flask, request, jsonify, redirect, session
from analyze import Analyze
from spotify import Spotify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "6A464BA81846E"
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem session storage
CORS(app)  # Enable CORS for all routes

CLIENT_ID = "936de7b258614e848dc30cdbe159ad0f"
CLIENT_SECRET = "f7d53bbf159c4a60a8df92fdc7250c04"

spotify = Spotify(CLIENT_ID, CLIENT_SECRET)
analyze = Analyze()  # Instantiate Analyze class

user_emotion = None
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
            user_emotion= emotion_result  # Store emotion in session
            print(f"Emotion stored in session: {user_emotion}")  # Debug print
            return jsonify({'message': 'File uploaded successfully', 'emotion': emotion_result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    global user_emotion
    if 'spotify_token_info' not in session:
        return redirect('/login')
    token_info = session['spotify_token_info']
    if spotify.is_token_expired(token_info):
        token_info = spotify.refresh_access_token(token_info['refresh_token'])
    emotion = user_emotion
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

# @app.route('/logout')
# def logout():
#     return redirect('/end_session')

# @app.route('/end_session', methods=['POST', 'GET'])
# def end_session():
#     for filename in os.listdir(app.config['UPLOAD_FOLDER']):
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         os.remove(file_path)
#     session.clear()
#     return redirect(url_for('index'))

# @app.after_request
# def delete_uploaded_files(response):
#     @app.after_this_request
#     def remove_files(response):
#         for filename in os.listdir(app.config['UPLOAD_FOLDER']):
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             os.remove(file_path)
#         return response
#     return response

if __name__ == '__main__':
    app.run(debug=True)
