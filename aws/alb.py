import boto3

alb = boto3.client('elbv2')

load_balancer = alb.create_load_balancer(Name='test-alb', Subnets=['subnet-0e47a0e4d1e2d4971','subnet-040fe1aa4611cda26'])

