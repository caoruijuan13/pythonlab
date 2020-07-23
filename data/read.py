from pygrok import Grok
import matplotlib.pyplot as plt

def Average(lst): 
    return round(sum(lst) / len(lst),2) 

data1 = []
data2 = []
with open("/Users/crj/worklab/log/status.log",mode='r') as file:
	for line in file:
		pattern0 = '%{NOTSPACE:timestamp}\s* %{NOTSPACE:level}\s* %{NOTSPACE:target}\s* %{INT:line} %{NOTSPACE:module}\s* %{NOTSPACE:thread}\s* - %{NOTSPACE:type},%{INT:fromid},%{INT:toid},%{INT:sendnum},%{INT:value},%{NUMBER:float}'
		pattern1 = '[%{NOTSPACE:flag}\s*] %{NOTSPACE:timestamp}\s* - %{NOTSPACE:level}\s* - %{NOTSPACE:target}\s* - ,%{NOTSPACE:type},%{INT:myid},%{INT:toid},%{INT:sendnum},%{INT:value}'
		pattern2 = '[%{NOTSPACE:flag}\s*] %{NOTSPACE:timestamp}\s* - %{NOTSPACE:level}\s* - %{NOTSPACE:target}\s* - ,%{NOTSPACE:type},%{INT:myid},%{INT:toid},%{INT:adjust_type},%{INT:strategy}'
		pattern3 = '[%{NOTSPACE:flag}\s*] %{NOTSPACE:timestamp}\s* - %{NOTSPACE:level}\s* - %{NOTSPACE:target}\s* - ,%{NOTSPACE:type},%{INT:myid},%{INT:upid},%{INT:downid},%{INT:delay},%{NUMBER:throughput},%{NUMBER:lossrate}'
		xx = Grok(pattern0)
		y = xx.match(line)
		print(y)
		data_id = int(y['toid'])
		value = int(y['value'])
		if data_id == 1:
			data1.append(value)
		else:
			data2.append(value)

data_avg = Average(data2)
data_min = min(data2)
data_max = max(data2)
print( data_avg, data_max, data_min)
# plt.hist(data, bins=30, facecolor="blue", edgecolor="black", alpha=0.7)
# plt.plot(data2)
# plt.show()