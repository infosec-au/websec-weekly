'''
Websecweekly Module for Twitter Sec
MIT License
Using Kimonolabs API
'''
import requests
import sqlite3
import datetime
import json

i = datetime.datetime.now()
timestamp = "%s%s%s%s" % (i.day, i.month, i.year, i.hour)
conn = sqlite3.connect('../dbs/twitter.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS twitter (tweeter_name text, tweeter_href text, tweet_href text,
												 summary text, display_pic text, timestamp text)''')

def grab_data():
	r = requests.get("https://www.kimonolabs.com/api/1y9g92rc?apikey=D8j6OeleId1EB8GbMHj9Fx3F3Wzfyxu0")
	data = r.text.encode("utf8")
	data_parsed = json.loads(data)
	return data_parsed

def check_if_new(summary):
	cmd = "SELECT COUNT(*) FROM twitter WHERE summary = ?"
	count = c.execute(cmd, (summary,))
	if count.fetchone()[0] == 0:
		return True
	else:
		return False

def push_new(tweeter_name, tweeter_href, tweet_href, summary, display_pic):
	results_dict = {}
	cmd = """INSERT INTO twitter(tweeter_name, tweeter_href, tweet_href, summary, display_pic, timestamp) VALUES (?,?,?,?,?,?)"""
	c.execute(cmd, (tweeter_name, tweeter_href, tweet_href, summary, display_pic, timestamp))
	conn.commit()
	results_dict[tweeter_name] = summary
	return results_dict

data = grab_data()

# Temporary fix to adapt with current KimonoLabs API
# The following removes twitter status permalinks from email since they are no longer available.

try:
	for i in data['results']['collection1']:
		tweeter_name = i['name']['text']
		tweeter_href = i['name']['href']
		tweet_href = i['time']['href']
		summary = i['summary']['text']
		display_pic = i['display_pic']['src']
		if check_if_new(i['summary']['text']) == True:
			print push_new(tweeter_name, tweeter_href, tweet_href, summary, display_pic)
except Exception as e:
	print e