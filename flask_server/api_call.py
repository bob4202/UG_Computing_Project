import os
import urllib.parse
import datetime
import requests
from flask import session, redirect, url_for, jsonify, request
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
CLIENT_ID = "936de7b258614e848dc30cdbe159ad0f"
CLIENT_SECRET = "f7d53bbf159c4a60a8df92fdc7250c04"
REDIRECT_URI = "http://127.0.0.1:5000/"

# Spotify API endpoints
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

API_BASE_URL = "https://api.spotify.com/v1"
SEARCH_URL = "https://api.spotify.com/v1/search"
FEATURE_URL = 'https://api.spotify.com/v1/audio-features'

USER_MOOD = 'Happy'

#Example Artists
EXAMPLE_ARTISTS = ['Adele', 'Eminem', 'Bruno Mars', 'Ed Sheeran', 'Billie Eilish']
user_artist_dict = {}
user_tracks_dict = {}




scopes = ('user-top-read')

TOKEN_INFO = {
	"access_token": None,
	"refresh_token": None,
	"expires_in": None
}

def get_token():
	headers = {
		"Content-Type": "application/x-www-form-urlencoded"
	}
	data = {
		"scope": scopes,
		"grant_type": "client_credentials",
		"client_id": CLIENT_ID,
		"client_secret": CLIENT_SECRET
	}
	response = requests.post(url = TOKEN_URL, headers=headers, data=data)
	#token = response.json()['access_token']
	token = response.json()['access_token']
	#print(token)
	#TOKEN_INFO["refresh_token"] = token["refresh_token"]
	return token

# def get_spotify_oauth():
# 	return SpotifyOAuth(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI, scope=scopes)

def get_authorization_header(token):
	return {f"Authorization": "Bearer " + token}

def user_info(token):
	url = "https://api.spotify.com/v1/me/top/artists"
	result = requests.get(url, headers=get_authorization_header(token=token))
	print(result)
	json_result = result.json()
	print(json_result)


def get_artists_info(token, artists):
	artist_dict = {}
	for artist in artists:
		query = f"q={artist}&type=artist&limit=1"
		query_url = SEARCH_URL + "?" + query
		result = requests.get(query_url, headers=get_authorization_header(token=token))
		temp_dict = result.json()
		artist_dict[artist] = temp_dict
	
	user_artist_dict = artist_dict
	#print(user_artist_dict)
	return user_artist_dict

def get_top_tracks(token, user_artist_dict):
	top_tracks_dict = {}
	temp_dict = {}
	if len(user_artist_dict) == 0:
		print("No artists found")
	else :
		for artist in user_artist_dict:
			artist_data = user_artist_dict[artist]
			artist_id = artist_data['artists']['items'][0]['id']
			url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
			result = requests.get(url, headers=get_authorization_header(token=token)).json()
			top_tracks_dict[artist] = result
			for track in result['tracks']:
				track_info = {
					'artist_name': artist,
					'track_name': track['name'],
					'track_id': track['id'],
					'track_image': track['album']['images'][0]['url'] if track['album']['images'] else None
				}
				temp_dict[track['name']] = track_info

	user_tracks_dict = temp_dict
	return user_tracks_dict


def energy_analysis(token, user_top_songs):
	for song in user_top_songs.keys():
		track_id = user_top_songs[song]['track_id']
		url = f"{FEATURE_URL}/{track_id}"
		result = requests.get(url, headers=get_authorization_header(token=token)).json()
		user_top_songs[song]['valence'] = result['valence']
		user_top_songs[song]['energy'] = result['energy']
		user_top_songs[song]['mood'] = get_mood(result['valence'], result['energy'])
		#print(song + ' ' + str(result['valence']) + ' ' + str(result['energy'])+ ' ' + str(mood))

	return organize_playlist(user_top_songs)
def generate_playlist(token):
	pass

#Organize playlist by mood
def organize_playlist(user_top_songs):
	temp_dict = {}
	for song, attribute in user_top_songs.items():
		mood = attribute['mood']
		if mood not in temp_dict:
			temp_dict[mood] = []

		song_data = { k:v for k, v in attribute.items() if k != 'mood' }
		temp_dict[mood].append({song:song_data})

	return temp_dict
	
		


def get_mood(valence, energy):
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
	
def get_user_info(token):
	url = "https://api.spotify.com/v1/me/top/artists"
	result = requests.get(url, headers=get_authorization_header(token=token))
	print(result)
	json_result = result.json()
	print(json_result)


token = get_token()
#user_artist_dict =get_artists_info(token,EXAMPLE_ARTISTS)
#user_top_tracks = get_top_tracks(token, user_artist_dict)
#tracks_analysis = energy_analysis(token, user_top_tracks)
get_user_info(token)