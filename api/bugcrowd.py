'''
Websecweekly Module for Bugcrowd
MIT License
Using Kimonolabs API
'''
import requests
import sqlite3
import datetime
import json

i = datetime.datetime.now()
timestamp = "%s%s%s%s" % (i.day, i.month, i.year, i.hour)
conn = sqlite3.connect('../dbs/bugcrowd.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bugcrowd (company text, company_href text, new text, swag text, reward text,
			 hall_of_fame text, timestamp text)''')

def grab_data():
	r = requests.get("https://www.kimonolabs.com/api/bwq1ewgs?apikey=D8j6OeleId1EB8GbMHj9Fx3F3Wzfyxu0")
	data = r.text.encode("utf8")
	data_parsed = json.loads(data)
	return data_parsed

def check_if_new(company):
	cmd = "SELECT COUNT(*) FROM bugcrowd WHERE company = ?"
	count = c.execute(cmd, (company,))
	if count.fetchone()[0] == 0:
		return True
	else:
		return False

def push_new(company, company_href, new, swag, reward, hall_of_fame):
	results_dict = {}
	cmd = """INSERT INTO bugcrowd(company, company_href, new, swag, reward, hall_of_fame, timestamp) VALUES (?,?,?,?,?,?,?)"""
	c.execute(cmd, (company, company_href, new, swag, reward, hall_of_fame, timestamp))
	conn.commit()
	results_dict[company] = company_href
	return results_dict

data = grab_data()

for i in data['results']['collection1']:
	company = i['company']['text']
	company_href = i['company']['href']
	new = i['new']
	swag = i['swag']
	reward = i['reward']
	hall_of_fame = i['hall_of_fame']
	if check_if_new(i['company']['text']) == True:
		print push_new(company, company_href, new, swag, reward, hall_of_fame)