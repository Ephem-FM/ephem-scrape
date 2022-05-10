import psycopg2
import uuid
import os

def pg(song):
	con = psycopg2.connect(os.environ.get("POSTGRES_URI"))
	cur = con.cursor()
	print("writing ", song)
	insert_query = """ INSERT INTO playlists (playlist_song_id, station, show, date, artist, track) VALUES (%s, %s, %s, %s, %s, %s); """
	insert_tuple = (uuid.uuid4().hex), str(song["station"]), str(song["show"]), song["date"], str(song["artist"]), str(song["track"])
	cur.execute(insert_query, insert_tuple)
	con.commit()
	cur.close()
