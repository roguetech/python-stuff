import boto3, sys, json, os, requests

ec2a = boto3.resource('ec2')
ec2 = boto3.client('ec2')

filters = [
	{
		'Name': 'instance-state-name',
		'Values': ['running']
	}
]

running_instances = ec2a.instances.filter(Filters=filters)
all_instances = ec2a.instances.all()

instances_to_delete = []

def terminate_instance():
	#for instance in ec2.instances.all():
	#	if instance.instance_lifecycle == 'spot':
	#		print('this is a spot')
	#	print(instance.id, instance.state, instance.spot_instance-request-id)

	instance = ec2.describe_instances(InstanceIds=[instances_to_delete])

	if ec2a.describe_instances(InstanceIds=[instance_to_delete])['Reservations'][0]['Instances'][0]['InstanceLifecycle'] == 'spot':
		print("this is spot")
	else:
		print("not spot")

	if instance['Reservations'][0]['Instances'][0]['InstanceLifecycle'] == 'spot':
		print('This is a spot instance')
               
		spotrequest = instance['Reservations'][0]['Instances'][0]['SpotInstanceRequestId']
		print(spotrequest)
		ec2a.cancel_spot_instance_requests(SpotInstanceRequestIds=[x])

def new_term_instance(instances_to_delete):
	instance = ec2.describe_instances(InstanceIds=[instances_to_delete])
	if 'InstanceLifecycle' in instance['Reservations'][0]['Instances'][0] and instance['Reservations'][0]['Instances'][0]['InstanceLifecycle'] == 'spot':
			print("This is a spot instance, cancelling spot request and deleting spot instance " + instances_to_delete)
			spotrequest = instance['Reservations'][0]['Instances'][0]['SpotInstanceRequestId']
			print(spotrequest)
			#ec2.cancel_spot_instance_requests(SpotInstanceRequestIds=[spotrequest])
	#ec2.terminate_instances(InstanceIds=[instances_to_delete])

def cancel_spot(env, instance_id):
        session = boto3.Session(profile_name=env)
        ec2 = session.resource('ec2')
        instance = ec2.describe_instances(InstanceIds=instances_id)
        if 'InstanceLifecycle' in instance['Reservations'][0]['Instances'][0] and instance['Reservations'][0]['Instances'][0]['InstanceLifecycle'] == 'spot':
            print("This is a spot instance, cancelling spot request and deleting spot instance ")
            spotrequest = instance['Reservations'][0]['Instances'][0]['SpotInstanceRequestId']
            ec2.cancel_spot_instance_requests(SpotInstanceRequestIds=[spotrequest])
        else:
            print("This is not a not a spot")

#new_term_instance()

for instance in all_instances:
        instances_to_delete.append(instance)
        #print(instances_to_delete)
        #new_term_instance(instances_to_delete)
        #print(running_instances)
print(instances_to_delete)

