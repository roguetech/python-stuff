import boto3, sys, json, os, requests

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
                BUILD_RELEASE_NUMBER = ""
                GIT_REVISION = ""
                BRANCH_NAME = ""
                for i in range(len(data)):
                    if data[i]["Key"] == "application-name":
                         app = data[i]["Value"]
                         app = app.split("-", 1)
                         app = app[1]
                    if data[i]["Key"] == "environment":
                         env = data[i]["Value"]
                    if data[i]["Key"] == "BUILD_RELEASE_NUMBER":
                         BUILD_RELEASE_NUMBER = data[i]["Value"]
                    if data[i]["Key"] == "GIT_REVISION":
                         GIT_REVISION = data[i]["Value"]
                    if data[i]["Key"] == "BRANCH_NAME":
                         BRANCH_NAME = data[i]["Value"]
                url = "http://jenkins/job/no-" + app + "-service-release-" + env  + "/buildWithParameters?BUILD_RELEASE_NUMBER=" + BUILD_RELEASE_NUMBER + "&GIT_REVISION=" + GIT_REVISION + "&BRANCH_NAME=" + BRANCH_NAME
                print(url)
                #r = requests.post(url = url)

def get_lb():
       lb = boto3.client('elbv2')
       load_balancer = lb.describe_target_groups()
       #print(load_balancer)
       for l in load_balancer['TargetGroups']:
           target_list.append(l['TargetGroupArn'])
           load_balancer_health = lb.describe_target_health(TargetGroupArn=l['TargetGroupArn'])
           if load_balancer_health['TargetHealthDescriptions'][0]['TargetHealth']['State'] == "healthy":
               for item in load_balancer_health['TargetHealthDescriptions']:
                   #if 'spot' == instance.instance_lifecycle:
                        instance_list.append(item["Target"]["Id"])
                   #else:
                   #     print("Not Spot instance")
                   #     continue
           else:
               print("not healthy")

get_lb()
print("Healthy instances")
#print(target_list)
print(instance_list)
get_ec2_tags()
print("\nUrls: ")
print_ec2_tag_names()
