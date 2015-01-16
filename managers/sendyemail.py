#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sqlite3
from jinja2 import Environment, FileSystemLoader
import datetime
from dateutil.rrule import rrule, DAILY
from random import shuffle

date_now = '{dt:%A} {dt:%B} {dt.day}, {dt.year}'.format(dt=datetime.datetime.now())
PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=True,
    loader=FileSystemLoader(os.path.join(PATH, '../templates')),
    trim_blocks=False)

# Jinja Filters
def get_twitter_id(twitter_url):
	if "status" in twitter_url:
		return twitter_url.split('/')[5]

# Adding filters to enviroment to make them visible in the template
TEMPLATE_ENVIRONMENT.filters['twitter_id'] = get_twitter_id

# Limits within email
bugcrowd_range = list(range(0,5))
fulldisclosure_range = list(range(0,7))
hackerone_c_range = list(range(0,7))
hackerone_hacktivity_range = list(range(0,5))
hackerone_public_range = list(range(0,10))
netsec_range = 8
stackoverflow_range = 7
twitter_range = list(range(0,3))

# Data storage after filtering
bugcrowd_data = []
fulldisclosure_data = []
hackerone_c_data = []
hackerone_hacktivity_data = []
hackerone_public_data = []
netsec_data = []
stackoverflow_data = []
twitter_data = []

# Quality Control Variables
netsec_minimum_uv = 15
stackoverflow_minimum_answers = 3

template = TEMPLATE_ENVIRONMENT.get_template('newsletter.html')

startdate = datetime.date.today() - datetime.timedelta(days=7)
enddate = datetime.date.today()

weekdates = []

for dt in rrule(DAILY, dtstart=startdate, until=enddate):
    weekdates.append(dt.strftime("%-d%-m20%y"))

# Bugcrowd
try:
	cross = "&#10006;"
	tick = "&#10004;"
	bugcrowd_notations = []
	for date in weekdates:
		conn = sqlite3.connect('../dbs/bugcrowd.db')
		c = conn.cursor()
		cmd = "SELECT company, company_href, new, swag, reward, hall_of_fame FROM bugcrowd WHERE timestamp LIKE ?"
		count = c.execute(cmd, (date+'%',))
		if count.fetchone() == None or count.fetchone()[0] == 0:
			print "No new records to push @ " + date
		else:
			data = c.execute(cmd, (date+'%',))
			rows = data.fetchall()
			for row in rows:
				if row[2] == "Yes":
					new = tick
				else:
					new = cross
				if row[3] == "Yes":
					swag = tick
				else:
					swag = cross
				if row[4] == "Yes":
					reward = tick
				else:
					reward = cross
				if row[5] == "Yes":
					hof = tick
				else:
					hof = cross
				try:
					message = "New: {0} &#8226; Swag: {1} &#8226; Reward: {2} &#8226; Hall of Fame: {3}".format(new, swag, reward, hof)
					bugcrowd_notations.append(message)
				except:
					message = "error in encoding"
			for i in bugcrowd_range:
				try:
					bugcrowd_data.append(rows[i])
				except Exception as e:
					print e
except:
	print "Failed to pull data"

# Fulldisclosure
try:
	for date in weekdates:
		conn = sqlite3.connect('../dbs/fulldisclosure.db')
		c = conn.cursor()
		cmd = "SELECT title, link, date, description FROM fulldisclosure WHERE timestamp LIKE ?"
		count = c.execute(cmd, (date+'%',))
		if count.fetchone() == None:
			print "No new records to push @ " + date
		else:
			data = c.execute(cmd, (date+'%',))
			rows = data.fetchall()
			for i in fulldisclosure_range:
				try:
					fulldisclosure_data.append(rows[i])
				except Exception as e:
					print e
except:
	print "Failed to pull data"

# Hackerone Companies
try:
	for date in weekdates:
		conn = sqlite3.connect('../dbs/hackerone_companies.db')
		c = conn.cursor()
		cmd = "SELECT name, href FROM companies WHERE timestamp LIKE ?"
		count = c.execute(cmd, (date+'%',))
		if count.fetchone() == None:
			print "No new records to push @ " + date
		else:
			data = c.execute(cmd, (date+'%',))
			rows = shuffle(data.fetchall())
			for i in hackerone_c_range:
				try:
					hackerone_c_data.append(rows[i])
				except Exception as e:
					print e
except:
	print "Failed to pull data"

# Hackerone Hacktivity
try:
	for date in weekdates:
		conn = sqlite3.connect('../dbs/hackerone_hacktivity.db')
		c = conn.cursor()
		cmd = "SELECT company, company_href, hunter, hunter_href, bounty, time_ago FROM hacktivity WHERE timestamp LIKE ?"
		count = c.execute(cmd, (date+'%',))
		if count.fetchone() == None:
			print "No new records to push @ " + date
		else:
			data = c.execute(cmd, (date+'%',))
			rows = shuffle(data.fetchall())
			for i in hackerone_hacktivity_range:
				try:
					hackerone_hacktivity_data.append(rows[i])
				except Exception as e:
					print e
except:
	print "Failed to pull data"

# Hackerone Public
try:
	for date in weekdates:
		conn = sqlite3.connect('../dbs/hackerone_public.db')
		c = conn.cursor()
		cmd = "SELECT company, company_href, reporter, reporter_href, date, disclosed_name, disclosed_href FROM public WHERE timestamp LIKE ?"
		count = c.execute(cmd, (date+'%',))
		if count.fetchone() == None:
			print "No new records to push @ " + date
		else:
			data = c.execute(cmd, (date+'%',))
			rows = data.fetchall()
			for i in hackerone_public_range:
				try:
					hackerone_public_data.append(rows[i])
				except Exception as e:
					print e
except:
	print "Failed to pull data"

# Netsec
try:
	for date in weekdates:
		conn = sqlite3.connect('../dbs/netsec.db')
		c = conn.cursor()
		cmd = "SELECT name, href, author, author_href, rep, comment_count, comment_href, domain FROM posts WHERE timestamp LIKE ?"
		count = c.execute(cmd, (date+'%',))
		if count.fetchone() == None:
			print "No new records to push @ " + date
		else:
			data = c.execute(cmd, (date+'%',))
			rows = data.fetchall()
			try:
				for row in rows:
					if int(row[4]) >= netsec_minimum_uv:
						netsec_data.append(row)
			except Exception as e:
				print e
	netsec_data = netsec_data[:netsec_range]
except:
	print "Failed to pull data"

# Stackoverflow
try:
	for date in weekdates:
		conn = sqlite3.connect('../dbs/stackoverflow.db')
		c = conn.cursor()
		cmd = "SELECT title, link, answers, date, summary FROM stackoverflow WHERE timestamp LIKE ?"
		count = c.execute(cmd, (date+'%',))
		if count.fetchone() == None:
			print "No new records to push @ " + date
		else:
			data = c.execute(cmd, (date+'%',))
			rows = data.fetchall()
			try:
				for row in rows:
					if int(row[2]) >= stackoverflow_minimum_answers:
						stackoverflow_data.append(row)
			except Exception as e:
				print e
	stackoverflow_data = stackoverflow_data[:stackoverflow_range]
except:
	print "Failed to pull data"

# Twitter
try:
	for date in weekdates:
		conn = sqlite3.connect('../dbs/twitter.db')
		c = conn.cursor()
		cmd = "SELECT tweeter_name, tweeter_href, tweet_href, summary, display_pic FROM twitter WHERE timestamp LIKE ?"
		count = c.execute(cmd, (date+'%',))
		if count.fetchone() == None:
			print "No new records to push @ " + date
		else:
			data = c.execute(cmd, (date+'%',))
			rows = data.fetchall()
			for i in twitter_range:
				try:
					twitter_data.append(rows[i])
				except Exception as e:
					print e
except:
	print "Failed to pull data"

saved = template.render(date=date_now, bugcrowd_data=bugcrowd_data, bugcrowd_notations=bugcrowd_notations, fulldisclosure_data=fulldisclosure_data, 
					  hackerone_c_data=hackerone_c_data, hackerone_public_data=hackerone_public_data, hackerone_hacktivity_data=hackerone_hacktivity_data,
					  netsec_data=netsec_data, stackoverflow_data=stackoverflow_data, twitter_data=twitter_data).encode('utf8')

template_save = open("../templates/generated.html", "w")
template_save.write(saved)
template_save.close()