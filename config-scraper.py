#!/usr/bin/env python3
import json,urllib.request
import time

def downloadReposWithCircleCIConfig():
  url = "https://api.github.com/search/repositories?q=in%3Apath+.circleci?per_page=100"
  data = urllib.request.urlopen(url).read()
  return  json.loads(data)

def generateUrlToCircleCIConfig(path, branch):
    url = "https://raw.githubusercontent.com"
    return url+"/"+path+"/"+branch+"/.circleci/config.yml"


repos = downloadReposWithCircleCIConfig()
listOfRepos = repos["items"]

# For unauthenticated requests, the rate limit is up to 10 requests per minute.
rateLimitCounter = 0

for repo in listOfRepos:
    name = repo["name"]
    full_name = repo["full_name"]
    default_branch = repo["default_branch"]
    rateLimitCounter += 1
    url = generateUrlToCircleCIConfig(full_name, default_branch)
    try:
        if rateLimitCounter == 10:
            rateLimitCounter = 0
            # wait 10minutes before trying to request again
            time.sleep(60*10)
        urllib.request.urlretrieve(url, "configs/"+name+".yml")
        print("Downloaded "+name+".yml"+" successfully")


    except Exception as e:
        pass
