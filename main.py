from selenium import webdriver
from datetime import date
from datetime import timedelta
import os
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

yesterday = str(date.today()- timedelta(days = 1))
print(yesterday)
url = f"https://api.composer.nprstations.org/v1/widget/50ef24ebe1c8a1369593d032/day?date={yesterday}&format=html&hide_amazon=false&hide_itunes=false&hide_arkiv=false"
print(url)

driver.get(url)
tracks = driver.page_source.split('daily-track-data-column')[1:-1]
for track in tracks:
    details = track.split("song-data")
    if(len(details)==4):
        # song
        result = re.search('&gt;(.*?)&lt;', details[1])
        song = result.group(1)
        print("song", song)
        # track
        result = re.search('&gt;(.*?)&lt;', details[2])
        track = result.group(1)
        print("track", track)
        # album
        result = re.search('&gt;(.*?)&lt;', details[3])
        album = result.group(1)
        print("album", album)
        # time
        result = re.findall('&gt;(.*?)&lt;', details[3])
        time = result[-4]
        print("time", time)
        print(" ")
      
print("Finished!")