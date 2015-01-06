'''
Websecweekly Module for Stackoverflow
MIT License
Using Kimonolabs API
'''
import requests
import sqlite3
import datetime
import json

i = datetime.datetime.now()
timestamp = "%s%s%s%s" % (i.day, i.month, i.year, i.hour)
conn = sqlite3.connect('../dbs/stackoverflow.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS stackoverflow (title text, link text, answers text, date text, summary text,
			 timestamp text)''')

def grab_data():
	r = requests.get("https://www.kimonolabs.com/api/9jh2m9am?apikey=D8j6OeleId1EB8GbMHj9Fx3F3Wzfyxu0")
	data = r.text.encode("utf8")
	data_parsed = json.loads(data)
	return data_parsed

def check_if_new(title):
	cmd = "SELECT COUNT(*) FROM stackoverflow WHERE title = ?"
	count = c.execute(cmd, (title,))
	if count.fetchone()[0] == 0:
		return True
	else:
		return False

def push_new(title, link, answers, date, summary):
	results_dict = {}
	cmd = """INSERT INTO stackoverflow(title, link, answers, date, summary, timestamp) VALUES (?,?,?,?,?,?)"""
	c.execute(cmd, (title, link, answers, date, summary, timestamp))
	conn.commit()
	results_dict[title] = answers
	return results_dict

data = grab_data()

for i in data['results']['collection1']:
	title = i['title']['text']
	link = i['title']['href']
	answers = i['answers']
	date = i['date']
	summary = i['summary']
	if check_if_new(i['title']['text']) == True:
		print push_new(title, link, answers, date, summary)