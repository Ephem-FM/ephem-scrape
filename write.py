import psycopg2
import uuid
import os
import time as time_import

def connect(func, **kwargs):
	def wrapper():
		# con = psycopg2.connect('postgres://qckrwbcldmcbua:d843c6fcbe8d0411c1f113f00fdc458459f530b6bbf629a7c15e25ad09bf23e7@ec2-3-226-163-72.compute-1.amazonaws.com:5432/dc3j53nnljkf17')
		con = psycopg2.connect(os.environ.get('POSTGRES_URI'))
		con.autocommit = True
		cur = con.cursor()
		if[kwargs['use'] == 'schedule']:
			func(kwargs['station'], kwargs['schedule'], cur)
		elif[kwargs['use'] == 'song']:
			func(kwargs['song'], cur)
		cur.close()

	return wrapper

def write_song(song, cur):
	insert_query = """ INSERT INTO showverviews (playlist_song_id, station, show, date, artist, track) VALUES (%s, %s, %s, %s, %s, %s); """
	insert_tuple = (uuid.uuid4().hex), str(song["station"]), str(song["show"]), song["date"], str(song["artist"]), str(song["track"])
	cur.execute(insert_query, insert_tuple)

def write_schedule(station, schedule, cur):
	def adjust_time(time):
		adjusted = ''
		for char in time:
			if char.isdigit():
				adjusted = adjusted + char
			else:
				break
		if (('pm' in time or 'PM' in time) and ('12' not in time)):
			adjusted = str(int(adjusted) + 12)
		if ':30' in time:
			adjusted = adjusted + '.5'
		return adjusted
	
	for day in schedule:
		wkday_as_int = (time_import.strptime(day, "%A").tm_wday)

			# koop917
		if (station == 'koop917'):
			for time, show_name in schedule.get(day).items():
				start_time = adjust_time(time.split("-")[0])
				end_time = adjust_time(time.split("-")[1][1:])
				if(start_time and end_time):
					insert_query = """ INSERT INTO showverviews (id, name, station, day_of_week, start_time, end_time, num_shows, num_songs) VALUES (%s, %s, %s, %s, %s, %s, %s, %s); """
					insert_tuple = (uuid.uuid4().hex, show_name, station, wkday_as_int, start_time, end_time, 0, 0)
					cur.execute(insert_query, insert_tuple)
			# kutx989
		elif (station == 'kutx989'):
			for s in schedule[day]:
				insert_query = """ INSERT INTO showverviews (id, name, station, day_of_week, start_time, end_time, num_shows, num_songs) VALUES (%s, %s, %s, %s, %s, %s, %s, %s); """
				insert_tuple = (uuid.uuid4().hex, (s['title'] + " with " + s['host']), station, wkday_as_int, s['start'], s['end'], 0, 0)
				print(insert_tuple)
				cur.execute(insert_query, insert_tuple)

if __name__=="__main__":
	# connect(write_schedule, station="koop917", schedule=get_schedule(), use='schedule')()
	# connect(write_schedule, station="kutx989", schedule=get_schedule(), use='schedule')()
	print("tony baloney")