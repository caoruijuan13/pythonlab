from pygrok import Grok
text = '[Status] 2020-06-19T17:10:03.772382+08:00 INFO status 108 spot main - rtt,0,1,234,137,7.9'
pattern = '%{NOTSPACE:timestamp}\s* %{NOTSPACE:level}\s* %{NOTSPACE:target}\s* %{INT:line} %{NOTSPACE:module}\s* %{NOTSPACE:thread}\s* - %{NOTSPACE:type},%{INT:fromid},%{INT:toid},%{INT:sendnum},%{INT:value},%{NUMBER:float}'
xx = Grok(pattern)
y = xx.match(text)
print(y)