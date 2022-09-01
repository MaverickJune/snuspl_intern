# What is this project about?
measuring bandwidth between lambda instance and ec2 instance

# How to use this project directory
1. you have to configure you vpc and subnet setting(make sure lambda and ec2 are in same vpc, subnet)
2. you have to set appropriate IAM roles for each services
3. you need account that has administrative access

upload zip file to your aws lambda function, and download rest of the files ad directories to your local maching

# How does it work
1. iperf3_testing.py invoke aws lambda function, and make ssh connection to ec2 instance
2. lambda function make tcp connection to ec2 instance, and measure bandwidth(lambda : client, ec2 : server)
3. iperf3_testing.py gather logs from lambda(lambda->local) and ec2(ec2->s3->local), than draw graph using scripts in graph_drawing_script

# Warning
1. do not change any subdirectory name on this project directory, otherwise you will have to change some code
2. you SHOULD change every path to the files inside iperf3_testing.py to your local machine path

# Special thanks
1. https://github.com/snuspl/incubator-nemo/blob/master/tools/network_profiling/network_profiling.py
2. https://github.com/KimJeongChul/aws-lambda

