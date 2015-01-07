'''
Websecweekly Module for Hackerone Public
MIT License
Using Kimonolabs API
'''
import requests
import sqlite3
import datetime
import json

i = datetime.datetime.now()
timestamp = "%s%s%s%s" % (i.day, i.month, i.year, i.hour)
conn = sqlite3.connect('../dbs/hackerone_public.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS public (company text, company_href text, reporter text, 
													reporter_href text, date text, 
													disclosed_name text, disclosed_href text, timestamp text)''')

def grab_data():
	r = requests.get("https://www.kimonolabs.com/api/1tr4p0ou?apikey=D8j6OeleId1EB8GbMHj9Fx3F3Wzfyxu0")
	data = r.text.encode("utf8")
	data_parsed = json.loads(data)
	return data_parsed

def check_if_new(disclosed_href):
	cmd = "SELECT COUNT(*) FROM public WHERE disclosed_href = ?"
	count = c.execute(cmd, (disclosed_href,))
	if count.fetchone()[0] == 0:
		return True
	else:
		return False

def push_new(company, company_href, reporter, reporter_href, date, disclosed_name, disclosed_href):
	results_dict = {}
	cmd = """INSERT INTO public(company, company_href, reporter, reporter_href, date, disclosed_name, disclosed_href, timestamp) VALUES (?,?,?,?,?,?,?,?)"""
	c.execute(cmd, (company, company_href, reporter, reporter_href, date, disclosed_name, disclosed_href,timestamp))
	conn.commit()
	results_dict[company] = reporter + ":" + disclosed_name
	return results_dict

data = grab_data()

try:
	for i in data['results']['collection1']:
		company = i['company']['text']
		company_href = i['company']['href']
		reporter = i['reporter']['text']
		reporter_href = i['reporter']['href']
		date = i['date']
		disclosed_name = i['disclosed_href']['text']
		disclosed_href = i['disclosed_href']['href']
		if check_if_new(disclosed_href) == True:
			print push_new(company, company_href, reporter, reporter_href, date, disclosed_name, disclosed_href)
except Exception as e:
	print e			