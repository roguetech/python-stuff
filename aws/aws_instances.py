import boto3, sys, json, os

#
instance_list = []

def get_ec2_tags():
#	session = boto3.session(profile_name = env)
        ec2 = boto3.resource('ec2')
        
        for instance in ec2.instances.all():
                instance_list.append([instance.id, instance.tags])
        
        for items in instance_list:
             name = items[0]
             with open(f'{name}.json', 'w') as instance_file:
                  json.dump(items[1], instance_file)

def print_ec2_tag_names():
       for filename in os.listdir('/home/vagrant/python-stuff/aws'):
             if filename.endswith(".json"): 
                with open(filename, 'r') as instance_file:
                    data = json.load(instance_file)
                for i in data:
                    print(data[0]["Key"])
                    print(data[0]["Value"])
                

get_ec2_tags()
print_ec2_tag_names()
