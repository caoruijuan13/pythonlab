import re
line = '192.168.0.1 25/Oct/2012:14:46:34 "GET /api HTTP/1.1" 200 44 "http://abc.com/search" "Mozilla/5.0"'
reg = re.compile('^(?P<remote_ip>[^ ]*) (?P<date>[^ ]*) "(?P<request>[^"]*)" (?P<status>[^ ]*) (?P<size>[^ ]*) "(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"')
regMatch = reg.match(line)
linebits = regMatch.groupdict()
print(linebits)
for k, v in linebits.items() :
    print(k+": "+v)