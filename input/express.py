import os
import sys
import sqlite3
from pygrok import Grok
from icalendar import Calendar, Event
from datetime import datetime
import pytz


def get_express_message(type):
    messages = []
    connection = sqlite3.connect("/Users/crj/Library/Messages/chat.db")
    cursor = connection.cursor()
    sql = "select datetime(date / 1000000000 + strftime ('%s', '2001-01-01'), 'unixepoch', 'localtime') AS message_date,text from message where text like '%丰巢%' and is_read = 0"
    if type == 2:
        sql = "select datetime(date / 1000000000 + strftime ('%s', '2001-01-01'), 'unixepoch', 'localtime') AS message_date,text from message where text like '%菜鸟%' and is_read = 0"
    if type == 3:
        sql = "select datetime(date / 1000000000 + strftime ('%s', '2001-01-01'), 'unixepoch', 'localtime') AS message_date,text from message where text like '%驿站%' and is_read = 0"
    cursor.execute(sql)
    for row in cursor:
        messages.append(row)

    # update is_read = 1
    sql = "update message set is_read = 1 where text like '%丰巢%取件%' and is_read = 0;"
    if type == 2:
        sql = "update message set is_read = 1 where text like '%菜鸟%' and is_read = 0;"
    if type == 3:
        sql = "update message set is_read = 1 where text like '%驿站%' and is_read = 0;"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
    return messages


def parse_text(text, type):
    if type == 1:
        pattern = "【%{NOTSPACE:type}】%{NOTSPACE}家园%{NOTSPACE:number}门%{NOTSPACE}%{INT:id}号"
    elif type == 2:
        pattern = "【%{NOTSPACE:type}】%{NOTSPACE}家园%{NOTSPACE:number}门%{NOTSPACE}%{INT:id}号"
    else:
        pattern = "【%{NOTSPACE:type}】%{NOTSPACE}码%{NOTSPACE:number}"

    info = Grok(pattern).match(text)
    print(info)
    if type == 2:
        number = info["number"]
        id = info["id"]
    elif type == 3:
        number = info["number"][0:8]
        id = "0"
    else:
        number = info["number"]
        id = info["id"]
    return info["type"], number, id


def make_ics(info, type, index):
    date = info[0].split(" ")[0]
    time = info[0].split(" ")[1]
    name, number, id = parse_text(info[1], type)
    print(name)
    print(number)
    print(id)
    cal = Calendar()
    event = Event()

    if type == 3:
        hour = 21
    elif type == 2:
        hour = 22
    else:
        hour = 23

    print(hour)
    event.add('dtstart',
              datetime(int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2]),
                       hour, 30, 0,
                       tzinfo=pytz.timezone("Asia/Shanghai")))
    event.add('dtend',
              datetime(int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2]),
                       hour, 59, 0,
                       tzinfo=pytz.timezone("Asia/Shanghai")))
    event.add('summary', name + u" " + id + u"号, " + number)
    event.add('DESCRIPTION', info[1])
    cal.add_component(event)

    filename = 'cal' + str(index) + '.ics'

    f = open(os.path.join('/tmp', filename), 'wb')
    f.write(cal.to_ical())
    f.close()
    os.system('open /tmp/' + filename)


index = 0
for i in range(1, 4):
    messages = get_express_message(i)
    for info in messages:
        print(info)
        make_ics(info, i, index)
        index += 1
print(str(index) + u" express cals to import.")
