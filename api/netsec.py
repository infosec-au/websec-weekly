'''
Websecweekly Module for /r/netsec
MIT License
Using Kimonolabs API
'''
import requests
import sqlite3
import datetime
import json

i = datetime.datetime.now()
timestamp = "%s%s%s%s" % (i.day, i.month, i.year, i.hour)
conn = sqlite3.connect('../dbs/netsec.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS posts (name text, href text, author text, author_href text, rep text,
			 comment_count text, comment_href text, domain text, timestamp text)''')

def grab_data():
	r = requests.get("https://www.kimonolabs.com/api/au7slmkw?apikey=D8j6OeleId1EB8GbMHj9Fx3F3Wzfyxu0")
	data = r.text.encode("utf8")
	data_parsed = json.loads(data)
	return data_parsed

def check_if_new(href):
	cmd = "SELECT COUNT(*) FROM posts WHERE href = ?"
	count = c.execute(cmd, (href,))
	if count.fetchone()[0] == 0:
		return True
	else:
		return False

def push_new(name, href, author, author_href, rep, comment_count, comment_href, domain):
	results_dict = {}
	cmd = """INSERT INTO posts(name, href, author, author_href, rep, comment_count, comment_href, domain, timestamp) VALUES (?,?,?,?,?,?,?,?,?)"""
	c.execute(cmd, (name, href, author, author_href, rep, comment_count, comment_href, domain, timestamp))
	conn.commit()
	results_dict[name] = href
	return results_dict

data = grab_data()

for i in data['results']['collection1']:
	name = i['name']['text']
	href = i['name']['href']
	author = i['author']['text']
	author_href = i['author']['href']
	rep = i['rep']
	comment_count = i['comments']['text']
	comment_href = i['comments']['href']
	domain = i['link']['text']
	if check_if_new(i['name']['href']) == True:
		print push_new(name, href, author, author_href, rep, comment_count, comment_href, domain)