import boto3, sys, json, os

instance_list = []
target_list = []

def get_ec2_tags():
        ec2 = boto3.client('ec2')
        
        for items in instance_list:
            instance = ec2.describe_instances(InstanceIds=[items])
            #print(instance['Reservations'][0]['Instances'][0]['Tags'])
            with open(f'{items}.json', 'w') as instance_file:
                   json.dump(instance['Reservations'][0]['Instances'][0]['Tags'], instance_file)

def print_ec2_tag_names():
       for filename in os.listdir('/home/vagrant/python-stuff/aws'):
             if filename.endswith(".json"): 
                with open(filename, 'r') as instance_file:
                    data = json.load(instance_file)
                app = ""
                env = ""
                for i in range(len(data)):
                    if data[i]["Key"] == "application-name":
                         app = data[i]["Value"]
                    if data[i]["Key"] == "environment":
                         env = data[i]["Value"]
                url = "http://jenkins/view/" + app + "/job/no-" + app + "-release-" + env + "/lastCompletedBuild"
                print(url)

def get_lb():
       lb = boto3.client('elbv2')
       load_balancer = lb.describe_target_groups()
       #print(load_balancer)
       for l in load_balancer['TargetGroups']:
           target_list.append(l['TargetGroupArn'])
           load_balancer_health = lb.describe_target_health(TargetGroupArn=l['TargetGroupArn'])
           if load_balancer_health['TargetHealthDescriptions'][0]['TargetHealth']['State'] == "healthy":
               for item in load_balancer_health['TargetHealthDescriptions']:
                   instance_list.append(item["Target"]["Id"])
           else:
               print("not healthy")

get_lb()
print("Healthy instances")
#print(target_list)
print(instance_list)
get_ec2_tags()
print("\nUrls: ")
print_ec2_tag_names()
