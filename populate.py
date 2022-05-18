import psycopg2

def main():
    con = psycopg2.connect('postgres://hnewxezrserycc:fa7730d9660660f7dc0292e1282e327c0a93ff49d062cf25f270d30bc27747e3@ec2-3-209-61-239.compute-1.amazonaws.com:5432/d26q7d7nbt04qe')
    cur = con.cursor()
    select_query = """SELECT * FROM playlists;"""
    all_current_songs = cur.fetchall
    print(len(all_current_songs))
    con.commit()
    cur.close()

if __name__=="__main__":
    main()


