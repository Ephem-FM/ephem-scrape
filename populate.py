import psycopg2
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
from zoneinfo import ZoneInfo
from datetime import datetime,timedelta
import calendar

def main():
    daily('kutx989', 1)
    if(calendar.day_name[datetime.now(ZoneInfo("America/Chicago")).date().weekday()].lower()) == 'thursday':
        weekly('koop917')

def daily(station, days):
    con = psycopg2.connect(DB_URI)
    con.autocommit = True
    cur = con.cursor()
        # get yesterday's songs
    d = 0
    while d < int(days):
        select_query = """SELECT * FROM playlists WHERE date=%s AND station=%s;"""
        select_tuple = (str(datetime.now(ZoneInfo("America/Chicago")).date() - timedelta(d + 1)), station)
        cur.execute(select_query, select_tuple)
        rows = cur.fetchall()
        print(len(rows))
        d = d + 1

        count=0
        for row in rows:
            count = count + 1
            print("count", count)
            time.sleep(1)
            id = row[0]
            artist = row[4]
            track = row[5]
            client_credentials_manager = SpotifyClientCredentials(client_id='56cb54535a2840378768c32fb6539781', client_secret='cbaa3d2d0cb243fab9c5f8601bf89f20')
            sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
                # artist info (genres, popularity)
            try:
                artist_search = sp.search(q='artist:' + artist, type='artist')['artists']['items'][0]
                update_query = """ UPDATE playlists SET artist_popularity=%s, artist_genres=%s WHERE playlist_song_id=%s; """
                update_tuple = (round(artist_search['popularity'], 3), artist_search['genres'][:3], id)
                cur.execute(update_query, update_tuple)
                print("artist success!")
            except IndexError as e:
                # print("artist failure")
                print(f"Couldn't find artist {artist}, IndexError: {e}")

                # track info (danceability, energy, instrumentalness, valence)
            try:
                track_id = sp.search(q='artist:' + artist + ' track:' + track, type='track')['tracks']['items'][0]['id']
                audio_features = sp.audio_features(track_id)[0]
                update_query = """ UPDATE playlists SET danceability=%s, energy=%s, instrumentalness=%s, valence=%s WHERE playlist_song_id=%s; """
                update_tuple = (round(audio_features['danceability'], 3), round(audio_features['energy'], 3), round(audio_features['instrumentalness'], 3), round(audio_features['valence'], 3), id)
                cur.execute(update_query, update_tuple)
                print("track success!")
            except IndexError as e:
                # print("track failure")
                print(f"Couldn't find track {track}, IndexError: {e}")    
               
    con.commit()
    cur.close()

def weekly(station):
    daily(station, 7)

if __name__=="__main__":
    main()
    


