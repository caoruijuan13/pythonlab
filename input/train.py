from pygrok import Grok
from datetime import datetime
from icalendar import Calendar, Event
import re
import requests
from bs4 import BeautifulSoup
import os
import sys
import pytz
import sqlite3


filename = "/Users/crj/data.txt"

default_station = [u"杭州东", u"杭州", u"无锡", u"无锡东", u"济南西"]
def get_travel(info):
	m_c = info["train_number"]
	#get info by search
	url = "http://search.huochepiao.com/checi/" + str(m_c)
	header = {'User-Agent': 'Mozilla/5.0'}
	req = requests.get(url, headers=header)

	soup = BeautifulSoup(req.content, 'lxml')
	table = soup.find_all("table")[6]
	td_th = re.compile('t[dh]')

	dcc = []
	for row in table.findAll("tr"):
		tmp = {}
		cells = row.findAll(td_th)
		if len(cells) == 12 or len(cells) == 13:
			tmp["name"] = cells[2].find(text=True)
			tmp["end"] = cells[3].find(text=True)
			tmp["start"] = cells[4].find(text=True)
			tmp["cost"] = cells[6].find(text=True)
			dcc.append(tmp)

	start_station_index = 0
	start_station_name = info["site_name"]

	for i in dcc:
		m = re.compile(i["name"]).search(start_station_name)
		if m:
			start_station_index = dcc.index(i)

	default_to_station_index = 0
	default_to_station_name = ""
	k = 0
	for i in dcc:
		if k > start_station_index:
			if i["name"] in default_station:
				default_to_station_index = k
				default_to_station_name = i["name"]
		k += 1
	print(u"from " + start_station_name + u" to " + default_to_station_name + u" yes(y) or no(n)?")

	to_station_index = 0
	to_station_name = "y" #input()
	if to_station_name == "y":
		return start_station_index, default_to_station_index, dcc

	k = 0
	for i in dcc:
		if k > start_station_index:
			if i["name"] == to_station_name:
				to_station_index = k
				print(u"now to_station_name is "+to_station_name)
				return start_station_index, to_station_index, dcc
		k += 1
	while to_station_index == 0 or to_station_index <= start_station_index:
		print(u"目的地选择有误，请重新选择")
		to_station_name = input()
	return start_station_index, to_station_index, dcc

def con_t(cost):
	pattern = "%{INT:hour}小时%{INT:min}"
	if "小时" not in cost:
		pattern = "%{INT:min}"
	tmp = Grok(pattern).match(cost)
	total_min = 0
	if 'hour' in tmp:
		total_min += int(tmp['hour']) * 60

	if 'min' in tmp:
		total_min += int(tmp['min'])

	return total_min

def get_cost(start, end, dcc):
	start_cost = con_t(dcc[start]["cost"])
	end_cost = con_t(dcc[end]["cost"])
	total_mins = end_cost - start_cost
	hour = int(total_mins / 60)
	mins = total_mins % 60
	return hour, mins

#get info by stations
def get_info(line):
	info = parse_line(line)
	start, end, dcc = get_travel(info)
	start_station_name = dcc[start]["name"]
	to_station_name = dcc[end]["name"]
	cost_hour, cost_mins = get_cost(start, end, dcc)

	start_time = info["hour"] + u":" + info["min"]
	end_time = dcc[end]["end"]

	return start_station_name, to_station_name, cost_hour, cost_mins, info["train_number"], info["seat_info"], info["ticket_gate"], info["month"], info["day"], start_time, end_time

#parse_line
def parse_line(line):
	# pattern = '【%{NOTSPACE:type}】%{NOTSPACE:id}，%{INT:month}月%{INT:date}日%{NOTSPACE:train_number}次%{INT:train_id}车%{INT:seat_id}\s*'
	pattern = '【%{NOTSPACE:type}】'
	type = Grok(pattern).match(line)

	if type["type"] == '12306':
		# pattern2 = "%{INT:month}月%{INT:day}日%{NOTSPACE:train_number}次%{INT:train_id}车%{INT:seat_id},%{NOTSPACE:site_name}站%{HOUR:hour}:%{MINUTE:minute}开，%{NOTSPACE:ticket_gate}。"
		pattern2 = "%{INT:month}月%{INT:day}日%{NOTSPACE:train_number}次%{NOTSPACE:seat_info},%{NOTSPACE:site_name}站%{HOUR:hour}:%{MINUTE:min}开，%{NOTSPACE:ticket_gate}。"
		info = Grok(pattern2).match(line);
	return info


def make_ics(line, id):
	start_station_name, to_station_name, cost_hour, cost_mins, cc, zc, djk, month, day, start_time, end_time = get_info(line)

	year = datetime.now().year
	cal = Calendar()
	event = Event()
	event.add('dtstart',
		datetime(int(year), int(month), int(day), int(start_time.split(":")[0]), int(start_time.split(":")[1]), 0,
			tzinfo=pytz.timezone("Asia/Shanghai")))
	event.add('dtend',
		datetime(int(year), int(month), int(day), int(end_time.split(":")[0]), int(end_time.split(":")[1]), 0,
			tzinfo=pytz.timezone("Asia/Shanghai")))
	event.add('summary', start_station_name + u'-' + to_station_name + u":" 
		+ str(cost_hour) + u"小时" + str(cost_mins) + u"分")
	event.add('LOCATION', cc + u"次" + zc + u" " + djk)
	event.add('DESCRIPTION', line)
	cal.add_component(event)

	filename = 'cal' + str(id) +'.ics'

	f = open(os.path.join('/tmp', filename ), 'wb')
	f.write(cal.to_ical())
	f.close()
	os.system('open /tmp/' + filename)

# get messages from db
def get_messages_from_db():
	messages = []
	connection = sqlite3.connect("/Users/crj/Library/Messages/chat.db")
	cursor = connection.cursor()
	# sql = "select datetime(date / 1000000000 + strftime ('%s', '2001-01-01'), 'unixepoch', 'localtime') as time, text from message where text like '%12306%' and time >= datetime('now','start of day','-1 day');"
	sql = "select text from message where text like '%12306%' and is_read = 0"
	cursor.execute(sql)
	for row in cursor:
		messages.append(row[0])

	sql = "update message set is_read = 1 where text like '%12306%' and is_read = 0"
	cursor.execute(sql)
	connection.commit()
	cursor.close()
	connection.close()
	return messages

# read db
def read_db():
	messages = get_messages_from_db()
	id = 0
	for message in messages:
		print(message)
		make_ics(message, id)
		id += 1
	print(str(id) + u" train cals to import.")

# read file
def read_file():
	with open(filename,mode='r') as file:
		id = 0
		for line in file:
			print(line)
			make_ics(line, id)
			id += 1
	print(str(id) + u" train cals to import.")

read_db()
# read_file()