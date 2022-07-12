# ephem-scrape
the scripts that scrape two stations and pass those tracks through spotify api

Included in this repo are two scripts that scrape the playlists of KUTX 98.9 and KOOP 91.7, two independent radio stations in Austin, Texas.  They use a combination of Selenium and BeautifulSoup to do so. These are deployed via Heroku and scheduled to run nightly.  Another script locates songs written to db the prior day then passes those through Spotify API to retrieve characteristics such as affiliated genres, artist popularity, danceability, mood (valence), energy, and instrumentalness of track.

A couple miscellaneous scripts create foreign key relationships between the songs in the 'playlists' table and shows in the 'showverviews' table.
