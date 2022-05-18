import psycopg2
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# xxx get all existing items
# xxx retrieve artist and track for each
# xxx create spotify object
# xxx populate given connection to spotify
# xxx create a relevant update statement
# confirm that update statement works

def main():
    con = psycopg2.connect('postgres://hnewxezrserycc:fa7730d9660660f7dc0292e1282e327c0a93ff49d062cf25f270d30bc27747e3@ec2-3-209-61-239.compute-1.amazonaws.com:5432/d26q7d7nbt04qe')
    cur = con.cursor()
    cur.execute("""SELECT * FROM playlists;""")
    rows = cur.fetchall()
    for row in rows[:4]:
        id = row[0]
        artist = row[4]
        track = row[5]
        client_credentials_manager = SpotifyClientCredentials(client_id='56cb54535a2840378768c32fb6539781', client_secret='cbaa3d2d0cb243fab9c5f8601bf89f20')
        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        try:
                # artist info (genres, popularity)
            artist_search = sp.search(q='artist:' + artist, type='artist')['artists']['items'][0]
            update_query = """ UPDATE playlists SET artist_popularity=%s, artist_genres=%s WHERE playlist_song_id=%s; """
            update_tuple = (artist_search['popularity'], artist_search['genres'][:3], id)
            cur.execute(update_query, update_tuple)
                # track info (danceability, energy, instrumentalness, valence)
            track_id = sp.search(q='artist:' + artist + ' track:' + track, type='track')['tracks']['items'][0]['id']
            audio_features = sp.audio_features(track_id)[0]
            update_query = """ UPDATE playlists SET danceability=%s, energy=%s, instrumentalness=%s, valence=%s WHERE playlist_song_id=%s; """
            update_tuple = (audio_features['danceability'], audio_features['energy'], audio_features['instrumentalness'], audio_features['valence'], id)
            cur.execute(update_query, update_tuple)

        except IndexError as e:
            print(artist)
            print(sp.search(q='artist:' + artist, type='artist'))
            print(track)
            print(sp.search(q='artist:' + artist + ' track:' + track, type='track'))
            print(f"IndexError: {e}")

    con.commit()
    cur.close()

if __name__=="__main__":
    main()


