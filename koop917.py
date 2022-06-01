	# main imports
import re
from datetime import date
from dateparser import parse
	# getting daily show schedule
import requests
import bs4
import lxml
	# getting playlist
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
	# spotify
import spot
	# writing to db
import write


def main():
	song = { 'station': 'koop917' }
	schedule = get_schedule()
	for day in schedule:
		# MAY WANT TO EDIT HOW DATE IS CONSIDERED 
		if(parse(day).strftime('%m %d %Y') == parse("Today").strftime('%m %d %Y')): 
			song['date'] = parse(day).strftime('%Y-%m-%d') or ''
			print(1)
			print(song['date'])
		else:
			song['date'] = parse(day, settings={'PREFER_DATES_FROM': 'past'}).strftime('%Y-%m-%d') or ''
			print(2)
			print(song['date'])

		for k, v in schedule[day].items():
			print("k", k)
			print("v", v)
			song['show'] = v or ''
			songs_played = None;
			try:
				songs_played = get_playlist(clean_url(v))
				for artist, track in songs_played.items():
						# reset spotify categories to blank strings
					song['artist_popularity'] = song['artist_genres'] = song['danceability'] = song['energy'] = song['instrumentalness'] = song['valence'] = ''
					song['artist'] = artist or ''
					song['track'] = track or ''
					write.pg(song)
					print(song)
					time.sleep(1)
			except Exception as e:
				print('This error comes from koop917.py', e)
			finally:
				if(songs_played == None):
					print("It's reached none")

def get_schedule():
	result = requests.get('https://koop.org/shows/', headers={'User-Agent': 'Mozilla/5.0'})
	soup = bs4.BeautifulSoup(result.text,'lxml')
	time_slots = soup.select('tbody tr')
	days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
	schedule = {
		'Sunday':{},
		'Monday':{},
		'Tuesday':{},
		'Wednesday':{},
		'Thursday':{},
		'Friday':{},
		'Saturday':{},
	}

	for slot in time_slots:
		shows = slot.select('.schedule-cell')
		    # skipping the first slot because it's just a marker of beginning of time slot
		for day, show in enumerate(shows):
			if show.select('.time'):
				time = show.select('.time')[0].getText()
				name = show.select('.show-name')[0].getText()
				schedule[days[day-1]][time] = name

	return schedule

def clean_url(show_name):
		show_name_no_apostrophes = show_name.replace("'",'')		
		show_cleaned = re.sub('[^0-9a-zA-Z]+','-',show_name.replace("'",'').lower().strip())
		return show_cleaned

def get_playlist(show_cleaned):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    url = 'https://koop.org/programs/' + show_cleaned
    driver.get(url)
    
    try:
        playlist_raw = driver.find_element_by_class_name("js-programPlaylist")
        if(playlist_raw.text == ''):
            print(f'{show_cleaned} is likely a musical show but playlist is not shown')
            return
        songs = playlist_raw.text.split('\n')
        playlist = {}
        
        for song in songs:
            song_split = song.split('-')
            artist = song_split[0].strip()
            track = song_split[1].split('(')[0].strip()
            playlist[artist] = track
        return(playlist)
    except Exception as e:
        print(f'The program {show_cleaned} does not have a playlist and is therefore likely not a musical show')
    finally:
        driver.quit()

if __name__ == "__main__":
	main()	

	# try:
	# 	artist_info = spot.artist_info(artist)
	# 	song["artist_popularity"] = artist_info["artist_popularity"]
	# 	song["artist_genres"] = artist_info["artist_genres"]
	# except TypeError as e:
	# 	print(f"Couldn't find artist {artist}, TypeError: {e}")
	
	# try:
	# 	track_info = spot.track_info(track, artist)
	# 	song["danceability"] = track_info["danceability"]
	# 	song["energy"] = track_info["energy"]
	# 	song["instrumentalness"] = track_info["instrumentalness"]
	# 	song["valence"] = track_info["valence"]
	# except TypeError as e:
	# 	print(f"Couldn't find artist {artist}, TypeError: {e}")