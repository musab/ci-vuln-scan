#!/usr/bin/env python3
import json,urllib.request

def downloadReposWithCircleCIConfig():
  url = "https://api.github.com/search/repositories?q=in%3Apath+.circleci"
  data = urllib.request.urlopen(url).read()
  return  json.loads(data)

def generateUrlToCircleCIConfig(path, branch):
    url = "https://raw.githubusercontent.com"
    return url+"/"+path+"/"+branch+"/.circleci/config.yml"


repos = downloadReposWithCircleCIConfig()
listOfRepos = repos["items"]

for repo in listOfRepos:
    name = repo["name"]
    full_name = repo["full_name"]
    default_branch = repo["default_branch"]

    url = generateUrlToCircleCIConfig(full_name, default_branch)
    try:
        urllib.request.urlretrieve(url, "configs/"+name+".yml")
        print("Downloaded "+name+".yml"+" successfully")


    except Exception as e:
        pass
