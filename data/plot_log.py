from pygrok import Grok
import matplotlib.pyplot as plt


def Average(lst):
    return round(sum(lst) / len(lst), 2)

data0_1 = []
data0_2 = []
data1_1 = []
data1_2 = []

with open("/Users/crj/Documents/code/spot-rust/log/status.log", mode='r') as file:
# with open("/Users/crj/worklab/log/status.log", ：mode='r') as file:
    for line in file:
        # print(line)
        pattern = '%{NOTSPACE:timestamp}\s* %{NOTSPACE:level}\s* %{NOTSPACE:target}\s* %{INT:line} %{NOTSPACE:module}\s* %{NOTSPACE:thread}\s* - '
        pattern_status = pattern + \
            '%{NOTSPACE:type},%{INT:fromid},%{INT:toid},%{INT:sendnum},%{INT:value},%{NUMBER:float}'
        pattern_qos = pattern + \
            '%{NOTSPACE:type},%{INT:fromid},%{INT:toid},%{INT:sendnum},%{INT:value}'
        pattern2 = '[%{NOTSPACE:flag}\s*] %{NOTSPACE:timestamp}\s* - %{NOTSPACE:level}\s* - %{NOTSPACE:target}\s* - ,%{NOTSPACE:type},%{INT:myid},%{INT:toid},%{INT:adjust_type},%{INT:strategy}'
        pattern3 = '[%{NOTSPACE:flag}\s*] %{NOTSPACE:timestamp}\s* - %{NOTSPACE:level}\s* - %{NOTSPACE:target}\s* - ,%{NOTSPACE:type},%{INT:myid},%{INT:upid},%{INT:downid},%{INT:delay},%{NUMBER:throughput},%{NUMBER:lossrate}'
        xx = Grok(pattern_qos)
        y = xx.match(line)
        # print(y)
        from_id = int(y['fromid'])
        to_id = int(y['toid'])
        value = int(y['value'])
        if from_id == 0:
            if to_id == 1:
                data0_1.append(value)
            elif to_id == 2:
                data0_2.append(value)
        elif from_id == 1:
            if to_id == 1:
                data1_1.append(value)
            elif to_id == 2:
                data1_2.append(value)

data_avg = Average(data1_2)
data_min = min(data1_2)
data_max = max(data1_2)
print( data_avg, data_max, data_min)

# plt.hist(data2, bins=30, facecolor="blue", edgecolor="black", alpha=0.7)
plt.plot(data1_1)
plt.plot(data1_2)
plt.legend(['data1-1','data1-2'])
plt.show()