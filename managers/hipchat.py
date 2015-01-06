import sys
import json
import urllib2
import datetime
import sqlite3
import textwrap
from jinja2 import utils

conn = sqlite3.connect('../hipchat_subscribers.db', check_same_thread=False)

c = conn.cursor()

header = {'content-type':'application/json'}
i = datetime.datetime.now()
timestamp = "%s%s%s%s" % (i.day, i.month, i.year, i.hour)

#html entities for cross and tick
cross = "&cross;"
tick = "&#10004;"

def send_message(room_id_or_name, message, color, token):
	try:
		url = "https://api.hipchat.com/v2/room/" + str(room_id_or_name) + "/notification"
		print url
		data = json.dumps({"message" : message,
							"message_format" : "html",
							"color" : color})
		print data
		print url+"?auth_token="+token, data, header
		req = urllib2.Request(url+"?auth_token="+token, data, header)
		res = urllib2.urlopen(req)
		return res.read()
	except:
		return "error"

def send_bugcrowd(room, token, limit=None):
	conn = sqlite3.connect('../dbs/bugcrowd.db')
	c = conn.cursor()
	cmd = "SELECT company, company_href, new, swag, reward, hall_of_fame FROM bugcrowd WHERE timestamp = ?"
	count = c.execute(cmd, (timestamp,))
	if count.fetchone() == None or count.fetchone()[0] == 0:
		print "No new records to push @ " + timestamp
	else:
		data = c.execute(cmd, (timestamp,))
		rows = data.fetchall()
		count = 0
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
				message = "<img src=\"{0}\"></img> New Bounty: <a href=\"{1}\">{2}</a> &#8226; New: {3} &#8226; Swag: {4} &#8226; Reward: {5} &#8226; Hall of Fame: {6}".format(
				"https://static.shubh.am/wsw/bugcrowd_small.png", str(utils.escape(row[1])), str(utils.escape(row[0])), new, swag, reward, hof)
			except:
				message = "error in encoding"
			print message
			if limit!= None and count != limit:
				send_message(room, message, "yellow", token)	
				count += 1
			elif limit == None:
				send_message(room, message, "yellow", token)


def send_fulldisclosure(room, token, limit=None):
	conn = sqlite3.connect('../dbs/fulldisclosure.db')
	c = conn.cursor()
	cmd = "SELECT title, link, date, description FROM fulldisclosure WHERE timestamp = ?"
	count = c.execute(cmd, (timestamp,))
	if count.fetchone() == None or count.fetchone()[0] == 0:
		print "No new records to push @ " + timestamp
	else:
		data = c.execute(cmd, (timestamp,))
		rows = data.fetchall()
		print rows
		count = 0
		for row in rows:
			description = textwrap.wrap(utils.escape(row[3]), width=25)[0] + " [...]"
			try:
				message = "<img src=\"{0}\"></img> New Mail: <a href=\"{1}\">{2}</a> &#8226; Posted on {3}: {4}".format(
				"https://static.shubh.am/wsw/seclists_small.png", str(utils.escape(row[1])), str(utils.escape(row[0])), row[2], description)
			except:
				message = "error in encoding"
			print message
			if limit!= None and count != limit:
				send_message(room, message, "purple", token)
				count += 1
			elif limit == None:
				send_message(room, message, "purple", token)


def send_hackerone_companies(room, token, limit=None):
	conn = sqlite3.connect('../dbs/hackerone_companies.db')
	c = conn.cursor()
	cmd = "SELECT name, href FROM companies WHERE timestamp = ?"
	count = c.execute(cmd, (timestamp,))
	if count.fetchone() == None or count.fetchone()[0] == 0:
		print "No new records to push @ " + timestamp
	else:
		data = c.execute(cmd, (timestamp,))
		rows = data.fetchall()
		print rows
		count = 0
		for row in rows:
			try:
				message = "<img src=\"{0}\"></img> New Company on H1: <a href=\"{1}\">{2}</a>".format(
				"https://static.shubh.am/wsw/hackerone_small.png", str(utils.escape(row[1])), str(utils.escape(row[0])))
			except:
				message = "error in encoding"
			print message
			if limit!= None and count != limit:
				send_message(room, message, "gray", token)
				count += 1
			elif limit == None:
				send_message(room, message, "gray", token)


def send_hackerone_hacktivity(room, token, limit=None):
	conn = sqlite3.connect('../dbs/hackerone_hacktivity.db')
	c = conn.cursor()
	cmd = "SELECT company, company_href, hunter, hunter_href, bounty, time_ago FROM hacktivity WHERE timestamp = ?"
	count = c.execute(cmd, (timestamp,))
	if count.fetchone() == None or count.fetchone()[0] == 0:
		print "No new records to push @ " + timestamp
	else:
		data = c.execute(cmd, (timestamp,))
		rows = data.fetchall()
		print rows
		count = 0
		for row in rows:
			try:
				message = "<img src=\"{0}\"></img> <a href=\"{1}\">{2}</a> rewarded <a href=\"{3}\">{4}</a> with a {5} bounty. ({6})".format(
				"https://static.shubh.am/wsw/hackerone_small.png", str(utils.escape(row[1])), str(utils.escape(row[0])), str(utils.escape(row[3])),
				str(utils.escape(row[2])), str(utils.escape(row[4])), str(utils.escape(row[5])))
			except:
				message = "error in encoding"
			print message
			if limit!= None and count != limit:
				send_message(room, message, "gray", token)
				count += 1
			elif limit == None:
				send_message(room, message, "gray", token)

def send_netsec(room, token, limit=None):
	conn = sqlite3.connect('../dbs/netsec.db')
	c = conn.cursor()
	cmd = "SELECT name, href, author, author_href, rep, comment_count, comment_href, domain FROM posts WHERE timestamp = ?"
	count = c.execute(cmd, (timestamp,))
	if count.fetchone() == None or count.fetchone()[0] == 0:
		print "No new records to push @ " + timestamp
	else:
		data = c.execute(cmd, (timestamp,))
		rows = data.fetchall()
		print rows
		count = 0
		for row in rows:
			try:
				message = "<img src=\"{0}\"></img> <a href=\"{1}\">{2}</a> submitted by <a href=\"{3}\">{4}</a><br>{5} upvotes &#8226; <a href=\"{6}\">{7}</a> &#8226; <a href=\"{8}\">{9}</a>.".format(
				"https://static.shubh.am/wsw/reddit_small.png", utils.escape(row[1]).encode("utf-8"), utils.escape(row[0]).encode("utf-8"), utils.escape(row[3]).encode("utf-8"),
				utils.escape(row[2]).encode("utf-8"), utils.escape(row[4]).encode("utf-8"), utils.escape(row[6]).encode("utf-8"), utils.escape(row[5]).encode("utf-8"), "http://" + utils.escape(row[7]).encode("utf-8"),utils.escape(row[7]).encode("utf-8"))
			except:
				message = "error in encoding"
			print message
			if limit!= None and count != limit:
				send_message(room, message, "green", token)	
				count += 1
			elif limit == None:
				send_message(room, message, "green", token)

def send_stackoverflow(room, token, limit=None):
	conn = sqlite3.connect('../dbs/stackoverflow.db')
	c = conn.cursor()
	cmd = "SELECT title, link, answers, date, summary FROM stackoverflow WHERE timestamp = ?"
	count = c.execute(cmd, (timestamp,))
	if count.fetchone() == None or count.fetchone()[0] == 0:
		print "No new records to push @ " + timestamp
	else:
		data = c.execute(cmd, (timestamp,))
		rows = data.fetchall()
		print rows
		count = 0
		for row in rows:
			description = textwrap.wrap(utils.escape(row[4]), width=25)[0] + " [...]"
			try:
				message = "<img src=\"{0}\"></img> <a href=\"{1}\">{2}</a><br> {3} answers &#8226; {4}".format(
				"https://static.shubh.am/wsw/stackoverflow_small.png", utils.escape(row[1]).encode("utf-8"), utils.escape(row[0]).encode("utf-8"),
				utils.escape(row[2]).encode("utf-8"), utils.escape(row[3]).encode("utf-8"))
			except:
				message = "error in encoding"
			print message
			if limit!= None and count != limit:
				send_message(room, message, "red", token)	
				count += 1
			elif limit == None:
				send_message(room, message, "red", token)

def send_twitter(room, token, limit=None):
	conn = sqlite3.connect('../dbs/twitter.db')
	c = conn.cursor()
	cmd = "SELECT tweeter_name, tweeter_href, tweet_href, summary, display_pic FROM twitter WHERE timestamp = ?"
	count = c.execute(cmd, (timestamp,))
	if count.fetchone() == None or count.fetchone()[0] == 0:
		print "No new records to push @ " + timestamp
	else:
		data = c.execute(cmd, (timestamp,))
		rows = data.fetchall()
		print rows
		count = 0
		for row in rows:
			description = textwrap.wrap(utils.escape(row[3]), width=75)[0] + " [...]"
			try:
				message = "<img src=\"{0}\"></img> &#8226; {1}<br> <a href=\"{2}\">{3}</a> &#8226; <a href=\"{4}\">Permalink</a>".format(
				"https://static.shubh.am/wsw/twitter_small.png", description.encode("utf-8"), utils.escape(row[1]).encode("utf-8"),
				utils.escape(row[0]).encode("utf-8"), utils.escape(row[2]).encode("utf-8"))
			except:
				message = "error in encoding"
			print message
			if limit!= None and count != limit:
				send_message(room, message, "green", token)
				count += 1
			elif limit == None:
				send_message(room, message, "green", token)

#Note: please URL encode your room names :)

cmd = "SELECT * FROM subscribers;"
data = c.execute(cmd)
rows = data.fetchall()
print rows
for row in rows:
	print row
	send_twitter(row[0], row[1], 5)
	send_bugcrowd(row[0], row[1], limit=None)
	send_fulldisclosure(row[0], row[1], limit=None)
	send_hackerone_companies(row[0], row[1], limit=None)
	send_hackerone_hacktivity(row[0], row[1], limit=None)
	send_netsec(row[0], row[1], limit=None)
	send_stackoverflow(row[0], row[1], limit=None)