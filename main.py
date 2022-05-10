    # for day's playlist
from selenium import webdriver
from datetime import date
from datetime import timedelta
import os
import re

    # for day's schedule
import calendar
import requests
from bs4 import BeautifulSoup as bs4
import lxml

def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    yesterday = str(date.today()- timedelta(days = 1))
    url = f"https://api.composer.nprstations.org/v1/widget/50ef24ebe1c8a1369593d032/day?date={yesterday}&format=html&hide_amazon=false&hide_itunes=false&hide_arkiv=false"
    day = wkshows()

    driver.get(url)
    total_tracks = driver.page_source.split('daily-track-data-column')[1:-1]
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

            for show in day:
                if(int(hour) >= int(show["start"]) and int(hour) < int(show["end"])):
                    song["show"] = show["title"]
                    song["date"] = date.today().strftime('%Y-%m-%d')
                    song["track"] = track
                    song["artist"] = artist
                    song["album"] = album
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
    
    day = []
    today = calendar.day_name[date.today().weekday()].lower()
    wkday = f"kutx-{today}"
    response = requests.get('https://kutx.org/program-schedule/', headers=headers, params=params)
    soup = bs4(response.text, 'lxml')
    shows = soup.find("div", id=wkday).find_all("div", class_="kutx-schedule-list-item")

    for show in shows:
        name = show.find("div", class_="kutx-schedule-list-host")
        if(name):
            host = name.text
            title = show.find("div", class_="kutx-schedule-list-title").text
            begin = show.find("div", class_="kutx-schedule-list-time").text.split("-")[0].split(" ")
            if(begin[0] == 12 and begin[1] == "am"):
                start = 0
            elif(begin[1] == "am"):
                start = begin[0]
            elif(begin[0] == "12" and begin[1] == "pm"):
                start = 12
            elif(begin[1] == "pm" and begin[0] != 12):
                start = int(begin[0]) + 12
            
            fin = show.find("div", class_="kutx-schedule-list-time").text.split("-")[1].split(" ")
            if(fin[0] == 12 and fin[1] == "am"):
                end = 0
            elif(fin[1] == "am"):
                end = fin[0]
            elif(fin[0] == "12" and fin[1] == "pm"):
                end = 12
            elif(fin[1] == "pm" and fin[0] != 12):
                end = int(fin[0]) + 12
            
            day.append({
                'start': start,
                'end': end,
                'title': title,
                'host': host
            })
    
    print(day)
    return day

if __name__=="__main__":
    main()