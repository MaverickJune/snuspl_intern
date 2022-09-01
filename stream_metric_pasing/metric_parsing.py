import json
import datetime
import matplotlib.pyplot as plt
import os
import argparse

# set the argument
parser = argparse.ArgumentParser(description='draw plots for stream_metric of given .json file')
parser.add_argument('--path', required=True, help="filepath to the target json file")
parser.add_argument('--draw', required=True, help="all : draw all, stagex-y-z : draw plot for the stage")
args = parser.parse_args()

# set default figure size and style in matplotlib
plt.rcParams["figure.figsize"] = (13, 7)
plt.style.use('ggplot')

# open metric.json file
with open(args.path) as f:
    metric_data = json.load(f)

# step1 : get all existing stages in target json file
list_stages = []
for key in metric_data["TaskMetric"]:
    if 'Stage' in key:
        list_stages.append({key: []})

# step 2 : making list clusters for plotting to each stages
for stage in list_stages:
    stage_name = list(stage)[0]
    for vertex in metric_data["TaskMetric"][stage_name]["data"]["streamMetric"]:
        stage[stage_name].append(vertex)

# from now on .. [{"Stagex-y-z" : ['vertex1', 'vertex2', ...]} ... ]

# step 3 : create root folder to store all the plots
cwd = os.getcwd()
root_path = os.path.join(cwd, os.path.basename(f.name[:-5])+"_plots")
## os.mkdir(root_path)

## print out all stages in the json file
# for stage in list_stages:
#     print(list(stage)[0]+" ", end='')

# step 4 : plot all available plots
for stage in list_stages:
    stage_name = list(stage)[0]
    
    if args.draw != "all":
        if args.draw != stage_name:
            continue
        
    for vertex in stage[stage_name]:
        
        ## 1. make lists for each metric for stage 0-0-0, ("startTimeStamp","numOfProcessedTuples")
        
        list_startTimeStamp = [] ##original timestamp list
        list_conv_startTimeStamp = [] ## timestamp list after conversion
        list_numOfProcessedTuples = []
        
        for i in range(len(metric_data["TaskMetric"][stage_name]["data"]["streamMetric"][vertex])):
            startTimeStamp = metric_data["TaskMetric"][stage_name]["data"]["streamMetric"][vertex][i]["startTimeStamp"]
            numOfProcessedTuples = metric_data["TaskMetric"][stage_name]["data"]["streamMetric"][vertex][i]["numOfProcessedTuples"]
            list_startTimeStamp.append(startTimeStamp)
            list_numOfProcessedTuples.append(numOfProcessedTuples)
        
        ## 2. change list_startTimeStamp to korean datetime(KST)
        for item in list_startTimeStamp:
            second = item / 1000
            datetime_string = datetime.datetime.fromtimestamp(second).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            list_conv_startTimeStamp.append(datetime_string)
            
        ## 3. make directories and draw plots
        final_path = os.path.join(root_path, f"{stage_name}/{vertex}")
        os.makedirs(final_path)
        
        plt.plot(list_conv_startTimeStamp, list_numOfProcessedTuples, linestyle='solid')
        plt.gcf().autofmt_xdate()
        plt.title("processed tuples vs time")
        plt.ylabel('# of processed tuples')
        
        plt.savefig(f'{final_path}/{stage_name}_{vertex}.png')
        plt.close("all")


        

        
        
            
        


        
        
        
