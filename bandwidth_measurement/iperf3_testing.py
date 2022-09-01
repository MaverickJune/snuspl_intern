import boto3
import json
import paramiko
from datetime import datetime
import time
import os

'''
you may suffer from boto3 client times out (ReadTimeoutError) because of 
NAT configuration, oryour lambda timeout configuration
please set your lambda timeout configuration in lenient manner
'''

# configuration variable
profile_name = "my_account_root"
region_name = "ap-northeast-2"
ec2_server_ipv4 = "13.125.54.142"
path_of_pem_key = "/Users/zenius77/Desktop/aws_keys/june.pem"
server_log_file_name = "log_server_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".txt"
client_log_file_name = "log_client_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".txt"

# define a session and clients
aws_con = boto3.session.Session(profile_name=profile_name)
lambda_client = aws_con.client('lambda', region_name=region_name)
s3_client = aws_con.client('s3', region_name=region_name)

# reading pem file and crate key object
key = paramiko.RSAKey.from_private_key_file(path_of_pem_key)
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# ssh connection to server ec2 instance
print("Connecting to : "+ec2_server_ipv4)
ssh_client.connect(hostname=ec2_server_ipv4, username="ubuntu", pkey=key)
print("Connected to : "+ec2_server_ipv4)

# establish iperf3 server to target ec2 instance
_, _, _ = ssh_client.exec_command(f"iperf3 -s --logfile {server_log_file_name} -1")
print("iperf3 server established")

# sleep for stablility
time.sleep(2)

print("lambda client iperf3 test started")
print("running...")
# invoke lambda iperf3 client function
response = lambda_client.invoke(
    FunctionName='test_iperf3',
    InvocationType='RequestResponse',
    LogType='None'
)
print("lambda client iperf3 test completed")

# get server log result to my local machine
_, stdout, stderr = ssh_client.exec_command(f"python3 sendlog.py {server_log_file_name}")
print("uploaded log file from ec2 to s3")
time.sleep(5)   # sleep for stability .. do not erase this!
s3_client.download_file("june0912bucket", server_log_file_name, "/Users/zenius77/Desktop/study_aws_boto3_sdk/log_server/" + server_log_file_name)
print("downloaded log file from s3 to local")

# delete log file created inside ec2 server
_, _, _ = ssh_client.exec_command("rm log*.txt")
print("log file is deleted from server")

# close ssh connection
_, _, _ = ssh_client.exec_command("exit")
print("ssh connection terminated \n")

# get client-side(lambda)log result
payload_result = json.loads(response['Payload'].read())['test_result'].splitlines()

# save result to txt file
with open("./log_client/"+client_log_file_name, 'w') as output_file:
    for element in payload_result:
        output_file.write(element + '\n')

# select graph drawing script and draw graph
os.system("python3 ./graph_drawing_script/draw_graph_default.py")




