#!/usr/bin/python

import boto3
import json
from datetime import datetime

def runinstance(event_name, response):
	for event in response['Events']:
		print("=======================================")
		for j in range(len(event)):
			print("This is the " + str(j) + " event")
			print("============================================")
			print("Event Time " + str(event['EventTime']))
			for i in range(len(event['Resources'])):
				print("Resource Type: " + event['Resources'][i]['ResourceType'])
				print("Resource Name: " + event['Resources'][i]['ResourceName'] + "\n")

def consolelogin(event_name, response):
	for event in response['Events']:
		print(event['EventName'] + " \n")
		print(event['EventTime'])


def main():
	event_name = input("Please enter an Event Name: \n")

	client = boto3.client('cloudtrail')

	response = client.lookup_events(
        	LookupAttributes=[
                	{
                        	'AttributeKey': 'EventName',
                        	'AttributeValue': event_name
                	},
        	],
        	StartTime=datetime(2020, 2, 20),
        	EndTime=datetime(2020, 2, 25),
        	MaxResults=123,
        	#NextToken='string'
	)
	#print(response)
	if event_name == "RunInstances":
		runinstance(event_name, response)
	elif event_name == "ConsoleLogin":
		consolelogin(event_name, response)
	else:
		print("This is not a valid Event Name")

if __name__ == "__main__":
	main()
