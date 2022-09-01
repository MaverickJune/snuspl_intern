import glob
import os
import matplotlib.pyplot as plt
import re

'''
[warning]
this graph drawing script can only be utilized in case of iperf3.pallelism_level == 1
Please make sure that your aws lambda handler has right configuration
'''

# pyplot configuration
plt.rcParams["figure.figsize"] = (13, 7)
plt.style.use('ggplot')


# lambda function for print_list
def pr_l(x):
    for t in x:
        print(t)


# get the latest created log file from log_server directory
list_of_files_s = glob.glob('/Users/zenius77/Desktop/study_aws_boto3_sdk/log_server/*')
list_of_files_c = glob.glob('/Users/zenius77/Desktop/study_aws_boto3_sdk/log_client/*')
latest_file_s = max(list_of_files_s, key=os.path.getctime)  # ./log_server/log_server_2022_xxxx.txt
latest_file_c = max(list_of_files_c, key=os.path.getctime)
target_file_name = latest_file_s.split('/')[6][:-4].replace("_server", "")

# make lists to draw a graph
with open(latest_file_s, 'r') as server_log:
    server_log_l = server_log.read().splitlines()

with open(latest_file_c, 'r') as client_log:
    client_log_l = client_log.read().splitlines()


# generate effective printlist for server log
start_flag = False
eff_server_log_list = []

list_s_bitrate = []     # lists used to draw graph, server side
list_s_timestamp = []   # lists used to draw graph, server side

for line in server_log_l:
    if start_flag == 0:
        if line == "[ ID] Interval           Transfer     Bitrate":
            start_flag = True
        continue
    if line == "- - - - - - - - - - - - - - - - - - - - - - - - -":
        break
    eff_server_log_list.append(line)

for line in eff_server_log_list:
    tmp_split_s = re.split(r'\s+', line)
    list_s_timestamp.append(tmp_split_s[2])
    list_s_bitrate.append(float(tmp_split_s[6]))

# generate effective printlist for client log
list_c_bitrate = []
list_c_timestamp = []

for i, item in enumerate(client_log_l):
    tmp = item.split(":")
    if tmp[0] == "Lambda":
        break
    bitrate = float(tmp[2].strip().split(' ')[0])
    timestamp_c = f"{i}.00-{i+1}.00"
    list_c_bitrate.append(bitrate)
    list_c_timestamp.append(timestamp_c)

# draw bw_server graph using given lists
fig1 = plt.figure()
plt.plot(list_s_timestamp, list_s_bitrate, linestyle="solid", label="server")
plt.gcf().autofmt_xdate()
plt.title(f"{target_file_name}_server")
plt.xlabel("sec")
plt.ylabel("Mbits/sec")
plt.legend(loc="upper left")
plt.savefig(f'./graph/{target_file_name}_server.png')
plt.close("all")

fig2 = plt.figure()
plt.plot(list_c_timestamp, list_c_bitrate, linestyle="solid", label="client")
plt.gcf().autofmt_xdate()
plt.title(f"{target_file_name}_client")
plt.xlabel("sec")
plt.ylabel('Mbits/sec')
plt.legend(loc="upper left")
plt.savefig(f'./graph/{target_file_name}_client.png')
plt.close("all")














