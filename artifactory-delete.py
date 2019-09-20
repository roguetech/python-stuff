#!/usr/bin/python
import requests
import json
import sys
import re
import datetime as DT

today = DT.date.today()
week_ago = today - DT.timedelta(days=1)

# Setup Artifactory Credentials and url, the Credentials can be replaced by a Token
username = "admin"
password = "password!"
artifactory = "http://192.168.169.130:8081/artifactory/"
headers = {"Content-Type": "text/plain"}

# Setting up a number of lists to take the results of the query
name = []
repo = []
path = []

# Below are a Number of example Artifactory AQL search queries

#Below Query looks for items whos last update was before date
#query = 'items.find({"updated": {"$lt":"'+str(week_ago)+'"},"$and":[{"name":{"$match":"*.pom"}}]}).include("name","repo","path")'
#query = 'items.find({"updated": {"$lt":"2019-09-17T16:10:00"},"$and":[{"name":{"$match":"*.pom"}}]}).include("name","repo","path")'
query = 'items.find({"updated": {"$lt":"2019-09-19T16:30:00"}}).include("name","repo","path")'
# Below Query looks for file with end in jar or pom
#query = 'items.find({"type":"file","$or":[{"name":{"$match":"*.jar"}},{"name":{"$match":"*.pom"}}]}).include("name")'

def getitems():
# This Function finds based on the artifacts and adds there name, repo and path to different lists
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
               name.append(v[x]['name'])
               repo.append(v[x]['repo'])
               path.append(v[x]['path'])
               x = x+1

def deleteItems():
# This Function takes the lists that were created and does a dry run on the artifacts
# If you choose you can then delete the listed artifacts
        i = 0
        sizeofList = len(name)

        if sizeofList == 0:
            print "\n Based on your query, Nothing Matches the Criteria"
            sys.exit()

        print "-------------------------------------------------------------------"
        print "Based on your query, below is the artifacts that have been found"
        print "-------------------------------------------------------------------"

        while i < sizeofList:
            itemPath = repo[i] + "/" + path[i] + "/" + name[i]

            newURL = artifactory + itemPath + "&dry=1"
            print "\nDry Run - " + newURL

            print "\nDeleting Artifact"
            rdel = requests.delete(newURL, auth = (username, password))
            print rdel

            print "----------------------------------------------------------------"

            i = i+1

        print('Do you want to delete all listed artifacts?')
        ans = raw_input('(Y/N) << ').lower()
        if ans == "y":
            i = 0
            while i < sizeofList:
                itemPath = repo[i] + "/" + path[i] + "/" + name[i]
                newURL = artifactory + itemPath
                print "\nDeleting - " + newURL
                rdel = requests.delete(newURL, auth = (username, password))
                print rdel
                print "----------------------------------------------------------------"
                i = i+1

                print "\nCheck if it is Deleted"
                rcheck = requests.get(newURL)
                print rcheck
                print "----------------------------------------------------------------"

        elif ans == "n":
            print "\nExiting, Goodbye"

        else:
            print "\nYou did Enter a Valid Entry, Goodbye"

if __name__ == "__main__":

    print "========================================================="
    print "This application will find based on a AQL query, artifacts"
    print "These artifacts can then be deleted"
    print "========================================================="

    print "\nDo you want to continue: "
    con = raw_input('(Y/N) << ').lower()
    if con == "y":
        getitems()
        deleteItems()
    elif con == "n":
        print "\nGoodbye\n"
        sys.exit()
    else:
        print "\nYou didnt Enter a Valid Entry, Goodbye\n"
        sys.exit()

