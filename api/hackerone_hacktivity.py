'''
Websecweekly Module for Hackerone Hacktivity
MIT License
Using Kimonolabs API
'''
import requests
import sqlite3
import datetime
import json

i = datetime.datetime.now()
timestamp = "%s%s%s%s" % (i.day, i.month, i.year, i.hour)
conn = sqlite3.connect('../dbs/hackerone_hacktivity.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS hacktivity (company text, company_href text, hunter text, 
													hunter_href text, bounty text, time_ago text, 
													time_ago_href text, timestamp text)''')

def grab_data():
	r = requests.get("https://www.kimonolabs.com/api/31gjk7uy?apikey=D8j6OeleId1EB8GbMHj9Fx3F3Wzfyxu0")
	data = r.text.encode("utf8")
	data_parsed = json.loads(data)
	return data_parsed

def check_if_new(time_ago_href):
	cmd = "SELECT COUNT(*) FROM hacktivity WHERE time_ago_href = ?"
	count = c.execute(cmd, (time_ago_href,))
	if count.fetchone()[0] == 0:
		return True
	else:
		return False

def push_new(company, company_href, hunter, hunter_href, bounty, time_ago, time_ago_href):
	results_dict = {}
	cmd = """INSERT INTO hacktivity(company, company_href, hunter, hunter_href, bounty, time_ago, time_ago_href, timestamp) VALUES (?,?,?,?,?,?,?,?)"""
	c.execute(cmd, (company, company_href, hunter, hunter_href, bounty, time_ago, time_ago_href,timestamp))
	conn.commit()
	results_dict[company] = hunter + ":" + bounty
	return results_dict

data = grab_data()

for i in data['results']['collection1']:
	company = i['company']['text']
	company_href = i['company']['href']
	hunter = i['hunter']['text']
	hunter_href = i['hunter']['href']
	bounty = i['bounty']
	time_ago = i['time_ago']['text']
	time_ago_href = i['time_ago']['href']
	if check_if_new(time_ago_href) == True:
		print push_new(company, company_href, hunter, hunter_href, bounty, time_ago, time_ago_href)