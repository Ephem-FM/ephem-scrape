from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import psycopg2


# retrieve all songs
# create a loop to go through each of them
# for each, locate the station it corresponds to--need to do more here
# get the id of that song

def main():
    conn = psycopg2.connect('postgres://qckrwbcldmcbua:d843c6fcbe8d0411c1f113f00fdc458459f530b6bbf629a7c15e25ad09bf23e7@ec2-3-226-163-72.compute-1.amazonaws.com:5432/dc3j53nnljkf17')
    # conn = psycopg2.connect(os.environ.get('HEROKU_POSTGRESQL_ORANGE_URL'))
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("""SELECT * FROM playlists;""")
    all_songs = cur.fetchall()

    for row in all_songs:
        station, show, date = row[1], row[2], row[3]
        foreign_id = find_corresponding_show(station, show, date, cur)
        update_q = """ UPDATE playlists SET show_id=%s WHERE playlist_song_id=%s """
        update_t = (foreign_id, row[0])
        cur.execute(update_q, update_t)

    conn.commit()
    cur.close()


def find_corresponding_show(station, show, date, cur):
    if (station=='koop917'):
        select_q = """ SELECT id FROM showverviews WHERE station=%s AND name=%s AND day_of_week=%s"""
        select_t = (station, show, date.weekday())
    elif (station == 'kutx989'):
        select_q = """ SELECT id FROM showverviews WHERE station=%s AND name LIKE %s AND day_of_week=%s"""
        select_t = (station, '%' + show + '%', date.weekday())

    cur.execute(select_q, select_t)
    return cur.fetchone()

if __name__=="__main__":
    main()
    print((datetime.now(ZoneInfo("America/Chicago")).date() - timedelta(1)).weekday())
    print(datetime.today().weekday())