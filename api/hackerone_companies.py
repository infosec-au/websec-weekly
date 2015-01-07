'''
Websecweekly Module for Hackerone Companies
MIT License
Using Kimonolabs API
'''
import requests
import sqlite3
import datetime
import json

i = datetime.datetime.now()
timestamp = "%s%s%s%s" % (i.day, i.month, i.year, i.hour)
conn = sqlite3.connect('../dbs/hackerone_companies.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS companies (name text, href text, timestamp text)''')

def grab_data():
	r = requests.get("https://www.kimonolabs.com/api/8t9v7jkm?apikey=D8j6OeleId1EB8GbMHj9Fx3F3Wzfyxu0")
	data = r.text.encode("utf8")
	data_parsed = json.loads(data)
	return data_parsed

def check_if_new(company_name):
	cmd = "SELECT COUNT(*) FROM companies WHERE name = ?"
	count = c.execute(cmd, (company_name,))
	if count.fetchone()[0] == 0:
		return True
	else:
		return False

def push_new(company_name, href):
	results_dict = {}
	cmd = """INSERT INTO companies(name, href, timestamp) VALUES (?,?,?)"""
	c.execute(cmd, (company_name,href,timestamp))
	conn.commit()
	results_dict[company_name] = href
	return results_dict

data = grab_data()

try:
	for i in data['results']['collection1']:
		if check_if_new(i['company']) == True:
			print push_new(i['company'])
except Exception as e:
	print e