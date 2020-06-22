from pygrok import Grok
import matplotlib.pyplot as plt

def Average(lst): 
    return round(sum(lst) / len(lst),2) 

data1 = []
data2 = []
with open("log.txt",mode='r') as file:
	for line in file:
		# pattern = '%{NOTSPACE:timestamp}\s* %{NOTSPACE:level}\s* %{NOTSPACE:target}\s* %{INT:line} %{NOTSPACE:module}\s* %{NOTSPACE:thread}\s* - %{NOTSPACE:type},%{INT:fromid},%{INT:toid},%{INT:sendnum},%{INT:value},%{NUMBER:float}'
		pattern = '[%{NOTSPACE:flag}\s*] %{NOTSPACE:timestamp}\s* - %{NOTSPACE:level}\s* - %{NOTSPACE:target}\s* - ,%{NOTSPACE:type},%{INT:ms},%{INT:toid},%{INT:sendnum},%{INT:value}'
		xx = Grok(pattern)
		y = xx.match(line)
		# print(y['toid'])
		data_id = int(y['toid'])
		value = int(y['value'])
		if data_id == 1:
			data1.append(value)
		else:
			data2.append(value)
	data_avg = Average(data2);
	data_min = min(data2);
	data_max = max(data2);
	print( data_avg, data_max, data_min);
	# plt.hist(data, bins=30, facecolor="blue", edgecolor="black", alpha=0.7)
	plt.plot(data2)
	plt.show()
