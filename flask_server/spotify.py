import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict
import urllib.parse
import json
import time

REDIRECT_URI = "http://127.0.0.1:5000/callback"  # Adjust port as per your Flask app port
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"


class Spotify:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=REDIRECT_URI,
            scope="user-top-read",
            cache_path=".spotifycache",
            show_dialog=True
        )
        self.sp = spotipy.Spotify(auth_manager=self.oauth),
        

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
    


    def final_data(self):
        try:
            data = self.get_top_artists(limit=10, time_range="long_term")
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
            return organized_tracks
    
        except Exception as e:
            print(f"An error occurred in final_data function: {e}")
            return None

    # def final_data(self):
    #     data = self.get_top_artists(limit=10, time_range="long_term")
    #     artists_dict = {}
    #     for artist in data["items"]:
    #         artist_id = artist["id"]
    #         artist_name = artist["name"]
    #         artist_top_tracks = self.sp.artist_top_tracks(artist_id)
    #         for track in artist_top_tracks["tracks"]:
    #             track_name = track["name"]
    #             track_id = track["id"]
    #             track_mood = self.get_track_mood(track_id)

    #             temp_dict = {"id": track_id, "mood": track_mood}

    #             artists_dict[track_name] = temp_dict
        
    #     organized_tracks =self.organize_by_mood(artists_dict)
                
    #     return organized_tracks
    
    def fetch_audio_features_with_retry(self,track_id, retries=5, backoff_factor=2):
        for attempt in range(retries):
            try:
                audio_features = self.sp.audio_features(track_id)
                if audio_features:
                    energy = audio_features[0]['energy']
                    valence = audio_features[0]['valence']
                    mood = self.get_mood(valence, energy)
                    return mood
                else:
                    return print("No audio features found for track.")
            except spotipy.SpotifyException as e:
                if e.http_status == 429:
                    print(f"Rate limit exceeded. Waiting {2**attempt} seconds before retrying.")
                    time.sleep(2**attempt)
                else:
                    raise
        return None

    def get_related_artists(self, artist_id):
        total_artists = 5
        related_artists = self.sp.artist_related_artists(artist_id)
        related_artist = {}
        while total_artists <= 5:
            for artist in related_artists['items']:
                related_artist[artist]
                total_artists -= 1
                
        return related_artist

    def get_track_mood(self, track_id):
        try:
            return self.fetch_audio_features_with_retry(track_id)
        except Exception as e:
            print(f"Error retrieving audio features for track {track_id}: {e}")
            return None
        
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