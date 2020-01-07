import boto3

ec2 = boto3.resource('ec2')
instance = ec2.create_instances(ImageId='ami-0987ee37af7792903', MinCount=1, MaxCount=1, InstanceType='t2.micro', SubnetId='subnet-040fe1aa4611cda26',
                                Placement={'AvailabilityZone': 'eu-west-1c'},)

print(instance[0])
