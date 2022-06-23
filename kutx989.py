    # for day's playlist
from selenium import webdriver
import datetime
from datetime import date # might be able to delete this line
from datetime import timedelta # might be able to delete this line
import os
import re
from zoneinfo import ZoneInfo
from webdriver_manager.chrome import ChromeDriverManager

    # for day's schedule
import calendar
import requests
from bs4 import BeautifulSoup as bs4
import lxml

    # for writing to db
import write

    # for spotify api
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import spot

def main(): 
    days_shows = get_days_shows()
    total_tracks = get_days_songs()
    today = str(datetime.datetime.now(ZoneInfo("America/Chicago")).date())
    
    for t in total_tracks:
        song = { 'station': 'kutx989'}
        details = t.split("song-data")
        if(len(details)==4):
            # track
            result = re.search('&gt;(.*?)&lt;', details[1])
            track = result.group(1)
            # artist
            result = re.search('&gt;(.*?)&lt;', details[2])
            artist = result.group(1)
            # album
            result = re.search('&gt;(.*?)&lt;', details[3])
            album = result.group(1)
            # time
            result = re.findall('&gt;(.*?)&lt;', details[3])
            time = result[-4]
            hour = get_army_time(time)

            for show in days_shows:
                if(int(hour) >= int(show["start"]) and int(hour) < int(show["end"])):
                    song["show"] = show["title"]
                    song["date"] = today
                    song["track"] = track
                    song["artist"] = artist
                    song["album"] = album
                    write.connect(write.write_song, use='song', song=song)
                    print(song)

    print("Finished!")

def get_army_time(time):
    meridian = time.split(" ")[1]
    initial = time.split(":")[0]

    # add 12 if after noon
    if(initial == 12 and meridian == "AM"):
        time = 0
    elif(meridian == "AM"):
        time = initial
    elif(initial == "12" and meridian == "PM"):
        time = 12
    elif(meridian == "PM" and initial != 12):
        time = int(initial) + 12

    return time
         
def get_days_shows():
    day = []
    headers = {
        'authority': 'api.composer.nprstations.org',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-ch-ua-mobile': '?1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36',
        'sec-ch-ua-platform': '"Android"',
        'origin': 'https://kutx.org',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://kutx.org/',
        'accept-language': 'en-US,en;q=0.9',
    }
    params = (
        ('date', str(date.today().strftime('%Y-%m-%d'))),
        ('format', 'json'),
    )
    response = requests.get('https://kutx.org/program-schedule/', headers=headers, params=params)
    soup = bs4(response.text, 'lxml')
    today = calendar.day_name[datetime.datetime.now(ZoneInfo("America/Chicago")).date().weekday()].lower()
    wkday = f"kutx-{today}"
    shows = soup.find("div", id=wkday).find_all("div", class_="kutx-schedule-list-item")

    for show in shows:
        name = show.find("div", class_="kutx-schedule-list-host")
        if(name):
            host = name.text
            title = show.find("div", class_="kutx-schedule-list-title").text
            start = adjust_time(show.find("div", class_="kutx-schedule-list-time").text.split("-")[0].split(" "), "start")
            end = adjust_time(show.find("div", class_="kutx-schedule-list-time").text.split("-")[1].split(" "), "end")

            day.append({
                'start': start,
                'end': end,
                'title': title,
                'host': host
            })

    return day

def adjust_time(time_initial, start_or_end):
        # if 12 am, 0
    if(time_initial[0] == '12' and time_initial[1] == "am"):
        if(start_or_end=='start'):
            return 0
        elif(start_or_end=='end'):
            return 24
        # if pm and not noon, +12
    if(time_initial[1] == "pm" and time_initial[0] != '12'):
        return int(time_initial[0]) + 12

    return time_initial[0]

def get_schedule():
    wkdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    schedule = {}

    for day in wkdays:
        schedule[day] = get_days_shows(day)
    
    return schedule

def get_days_songs():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    today = str(datetime.datetime.now(ZoneInfo("America/Chicago")).date())
    print(today)
    url = f"https://api.composer.nprstations.org/v1/widget/50ef24ebe1c8a1369593d032/day?date={today}&format=html&hide_amazon=false&hide_itunes=false&hide_arkiv=false"
    print(url)
    driver.get(url)
    total_tracks = driver.page_source.split('daily-track-data-column')[1:-1]
    return total_tracks

def get_spotify_data(song):
    client_credentials_manager = SpotifyClientCredentials(client_id='56cb54535a2840378768c32fb6539781', client_secret='cbaa3d2d0cb243fab9c5f8601bf89f20')
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    artist = song['artist']
    track = song['track']
    print("artist", artist)
    print("track", track)

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(artist_search['artists']['items'][0])
    
    try:
        artist_search = sp.search(q='artist:' + artist, type='artist')['artists']['items'][0]
        track_id = sp.search(q='artist:' + artist + ' track:' + track, type='track')['tracks']['items'][0]['id']
        audio_features = sp.audio_features(track_id)[0]
        song['artist_popularity'] = artist_search['popularity']
        song['artist_genres'] = artist_search['genres'][:3]
        song['danceability'] = audio_features['danceability']
        song['energy'] = audio_features['energy']
        song['instrumentalness'] = audio_features['instrumentalness']
        song['valence'] = audio_features['valence']


    except IndexError as e:
        print(f"IndexError: {e}")

if __name__=="__main__":
    main()
