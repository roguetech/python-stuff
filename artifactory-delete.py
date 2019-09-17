#!/usr/bin/python
import requests
import json
import sys
import re
import datetime as DT

today = DT.date.today()
week_ago = today - DT.timedelta(days=1)

username = "admin"
password = "password!"
artifactory = "http://192.168.169.130:8081/artifactory/"
headers = {"Content-Type": "text/plain"}

#Below Query looks for items whos last update was before date
#query = 'items.find({"updated": {"$lt":"'+str(week_ago)+'"},"$and":[{"name":{"$match":"*.pom"}}]}).include("name","repo","path")'
query = 'items.find({"updated": {"$lt":"2019-09-17T12:50:00"}}).include("name","repo","path")'
# Below Query looks for file with end in jar or pom
#query = 'items.find({"type":"file","$or":[{"name":{"$match":"*.jar"}},{"name":{"$match":"*.pom"}}]}).include("name")'

def getitems():

    global name
    global repo
    global path

    itemurl = "api/search/aql"
    url = artifactory + itemurl
    r = requests.post(url, auth = (username, password), headers=headers, data=query)
    json_data = json.loads(r.text)
    y = len(json_data['results'])

    x = 0
    for (k, v) in json_data.items():
        if k == 'results':
            while (x<y):
               name = v[x]['name']
               repo = v[x]['repo']
               path = v[x]['path']
               x = x+1
        else:
            continue

def deleteItems():
    try:
        itemPath = repo + "/" + path + "/" + name
        print itemPath

        newURL = artifactory + itemPath + "&dry=1"
        print newURL

        print "Delete Artifact"
        r = requests.delete(newURL, auth = (username, password))

        print "Check if it is Deleted"
        r = requests.get(newURL)
        print r

    except Exception as e:
        print "Nothing Found"

    # DELETE http://localhost:8081/artifactory/libs-release-local/ch/qos/logback/logback-classic/0.9.9

if __name__ == "__main__":
    getitems()
    deleteItems()
