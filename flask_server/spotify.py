import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict
import json
import time

REDIRECT_URI = "http://127.0.0.1:5000/callback"  # Adjust port as per your Flask app port

class Spotify:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.playlist_id = None
        self.oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=REDIRECT_URI,
            scope="user-top-read playlist-modify-private playlist-modify-public",
            cache_path=".spotifycache",
            #show_dialog=True
        )
        self.sp = spotipy.Spotify(auth_manager=self.oauth)

    def get_authorize_url(self):
        return self.oauth.get_authorize_url()

    def get_access_token(self, code):
        token_info = self.oauth.get_access_token(code)
        self.sp = spotipy.Spotify(auth_manager=self.oauth)
        return token_info

    def refresh_access_token(self, refresh_token):
        token_info = self.oauth.refresh_access_token(refresh_token)
        self.sp = spotipy.Spotify(auth_manager=self.oauth)
        return token_info

    def is_token_expired(self, token_info):
        return self.oauth.is_token_expired(token_info)

    def get_top_artists(self, limit=10, time_range="long_term"):
        results = self.sp.current_user_top_artists(limit=limit, time_range=time_range)
        return results

    def final_data(self, user_emotion):
        try:
            data = self.get_top_artists(limit=10, time_range="long_term")
            
            current_user_emotion = user_emotion.lower()
            print(f"Current user emotion: {current_user_emotion}")
            artists_dict = {}
            
            for artist in data["items"]:
                artist_id = artist["id"]
                artist_name = artist["name"]
                
                # Retrieve top tracks for the artist
                try:
                    artist_top_tracks = self.sp.artist_top_tracks(artist_id)
                except spotipy.SpotifyException as e:
                    print(f"Error fetching top tracks for artist {artist_name}: {e}")
                    continue
                
                for track in artist_top_tracks["tracks"]:
                    track_name = track["name"]
                    track_id = track["id"]
                    
                    # Get mood for the track
                    try:
                        track_mood = self.get_track_mood(track_id)
                    except Exception as e:
                        print(f"Error fetching mood for track {track_name} ({track_id}): {e}")
                        track_mood = "unknown"
                    
                    temp_dict = {"id": track_id, "mood": track_mood}
                    artists_dict[track_name] = temp_dict
            
            organized_tracks = self.organize_by_mood(artists_dict)
            user_track = organized_tracks[current_user_emotion]
            self.create_playlist(user_track, current_user_emotion)
            return user_track
    
        except Exception as e:
            print(f"An error occurred in final_data function: {e}")
            return None
    
    def fetch_audio_features_with_retry(self, track_id, retries=5, backoff_factor=2):
        for attempt in range(retries):
            try:
                audio_features = self.sp.audio_features(track_id)
                if audio_features:
                    energy = audio_features[0]['energy']
                    valence = audio_features[0]['valence']
                    mood = self.get_mood(valence, energy)
                    return mood
                else:
                    return "unknown"
            except spotipy.SpotifyException as e:
                if e.http_status == 429:
                    print(f"Rate limit exceeded. Waiting {2**attempt} seconds before retrying.")
                    time.sleep(2**attempt)
                else:
                    raise
        return None

    def get_related_artists(self, artist_id):
        related_artists = self.sp.artist_related_artists(artist_id)
        related_artist = {}
        total_artists = 0
        for artist in related_artists['items']:
            if total_artists < 5:
                related_artist[artist['name']] = artist['id']
                total_artists += 1
        return related_artist

    def get_track_mood(self, track_id):
        try:
            return self.fetch_audio_features_with_retry(track_id)
        except Exception as e:
            print(f"Error retrieving audio features for track {track_id}: {e}")
            return "unknown"
        
    def organize_by_mood(self, data):
        organized_data = {}

        for track_name, track_info in data.items():
            mood = track_info['mood']
            track_id = track_info['id']

            if mood not in organized_data:
                organized_data[mood] = []

            organized_data[mood].append({
                "trackname": track_name,
                "id": track_id
            })

        return organized_data

    def get_mood(self, valence, energy):
        weight_valence = 0.5
        weight_energy = 0.5

        happy = valence * weight_valence + energy * weight_energy
        sad = weight_valence * (1 - valence) + weight_energy * (1 - energy)
        if happy > 0.6:
            return "happy"
        elif sad > 0.6:
            return "sad"
        else:
            return "neutral"

    def create_playlist(self, music,emotion):
        try:
            user_id = self.sp.current_user()["id"]
            user_playlist = self.sp.user_playlist_create(
                user=user_id,
                name=emotion.capitalize(),
                public=False,
                collaborative=False,
                description="Playlist generated using the emotion analyzer"
            )
            user_playlist_id = user_playlist["id"]
            self.playlist_id = user_playlist["id"] 
            print(self.playlist_id)
            
            tracks_to_add = [track['id'] for track in music]
            self.sp.user_playlist_add_tracks(
                user=user_id,
                playlist_id=user_playlist_id,
                tracks=tracks_to_add
            )

            print(f"Playlist created with {len(music)} tracks")
            return user_playlist_id
        
        except spotipy.SpotifyException as e:
            print(f"Error creating playlist: {e}")
            return None

            
