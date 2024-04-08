import boto3
import os
import re
import subprocess

client = boto3.client('ecs')

response = client.list_clusters()
clusters = response['clusterArns']

cluster_pick = {}
print("Available Clusters:")
for i, cluster in enumerate(clusters):
    print(f"{i+1}. {re.sub(r'arn:aws:ecs:.*:cluster/','',cluster)}")

choice = input("Enter the number of the cluster you want to connect to: ")
chosen_cluster = clusters[int(choice)-1]
cluster_pick.update({'clustername':re.sub(r'arn:aws:ecs:.*:cluster/','',chosen_cluster)})

response = client.list_services(cluster=chosen_cluster)
services = response['serviceArns']

service_pick = {}
print("Available Services:")
for i, service in enumerate(services):
    print(f"{i+1}. {re.sub(r'arn:aws:ecs:.*:service/.*/','',service)}")

choice = input("Enter the number of the service you want to connect to: ")
chosen_service = services[int(choice)-1]
service_pick.update({'servicename':re.sub(r'arn:aws:ecs:.*:service/.*/','',chosen_service)})

# List all of the available ECS tasks for the specified cluster and service
response = client.list_tasks(cluster=chosen_cluster, serviceName=chosen_service)
tasks = response['taskArns']

task_pick = {}
print("Available Tasks:")
for i, task in enumerate(tasks):
    print(f"{i+1}. {re.sub(r'arn:aws:ecs:.*:task/.*/','',task)}")

choice = input("Enter the number of the task you want to connect to: ")
chosen_task = tasks[int(choice)-1]
task_pick.update({'taskname':re.sub(r'arn:aws:ecs:.*:task/.*/','',chosen_task)})

container_pick = {}
response = client.describe_tasks(cluster=chosen_cluster, tasks=tasks)
task = response['tasks']

for task in response['tasks']:
    print("Containers for task: " + task['taskArn'])
    container = task['containers']
    for i, name in enumerate(container):
        print(f"{i+1}. {name['name']}")

choice = input("Enter the number of the container you want to connect to: ")
chosen_container = container[int(choice)-1]
container_pick.update({'containername':chosen_container['name']})

command = 'aws ecs execute-command --cluster ' + cluster_pick['clustername'] + ' --task ' + task_pick['taskname'] + ' --container ' + container_pick['containername'] + ' --command "/bin/sh" --interactive' 

print ('Executing the following:' + command)
os.system(command)
