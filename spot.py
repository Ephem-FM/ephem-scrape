import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

def artist_info(artist):
    time.sleep(0.5)
    client_credentials_manager = SpotifyClientCredentials(client_id='56cb54535a2840378768c32fb6539781', client_secret='cbaa3d2d0cb243fab9c5f8601bf89f20')
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        # artist info (genres, popularity)
    try:
        artist_search = sp.search(q='artist:' + artist, type='artist')['artists']['items'][0]
        return {
            'artist_popularity': round(artist_search['popularity'], 3), 
            'artist_genres': artist_search['genres'][:3]
        }
    except IndexError as e:
        print(f"Couldn't find artist {artist}, IndexError: {e}")

def track_info(track, artist):
    time.sleep(0.5)
    client_credentials_manager = SpotifyClientCredentials(client_id='56cb54535a2840378768c32fb6539781', client_secret='cbaa3d2d0cb243fab9c5f8601bf89f20')
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        # track info (danceability, energy, instrumentalness, valence)
    try:
        track_id = sp.search(q='artist:' + artist + ' track:' + track, type='track')['tracks']['items'][0]['id']
        audio_features = sp.audio_features(track_id)[0]
        return {
            'danceability': round(audio_features['danceability'], 3),
            'energy': round(audio_features['energy'], 3),
            'instrumentalness': round(audio_features['instrumentalness'], 3),
            'valence': round(audio_features['valence'], 3)
        }
        
    except IndexError as e:
        print(f"Couldn't find track {track}, IndexError: {e}")   
