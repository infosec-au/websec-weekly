'''
Websecweekly Module for Fulldisclosure List
MIT License
Using Kimonolabs API
'''
import requests
import sqlite3
import datetime
import json

i = datetime.datetime.now()
timestamp = "%s%s%s%s" % (i.day, i.month, i.year, i.hour)
conn = sqlite3.connect('../dbs/fulldisclosure.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS fulldisclosure (title text, link text, date text, description text, timestamp text)''')

def grab_data():
	r = requests.get("https://www.kimonolabs.com/api/dm32e5ni?apikey=D8j6OeleId1EB8GbMHj9Fx3F3Wzfyxu0")
	data = r.text.encode("utf8")
	data_parsed = json.loads(data)
	return data_parsed

def check_if_new(title):
	cmd = "SELECT COUNT(*) FROM fulldisclosure WHERE title = ?"
	count = c.execute(cmd, (title,))
	if count.fetchone()[0] == 0:
		return True
	else:
		return False

def push_new(title, link, date, description):
	results_dict = {}
	cmd = """INSERT INTO fulldisclosure(title, link, date, description, timestamp) VALUES (?,?,?,?,?)"""
	c.execute(cmd, (title, link, date, description, timestamp))
	conn.commit()
	results_dict[title] = link
	return results_dict

data = grab_data()

for i in data['results']['collection1']:
	title = i['title']['text']
	link = i['title']['href']
	date = i['date']
	description = i['description']['text']
	if check_if_new(i['title']['text']) == True:
		print push_new(title, link, date, description)