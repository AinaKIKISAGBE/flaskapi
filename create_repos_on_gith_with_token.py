

import os 

def import_or_install(package_name):
    try:
        globals()[package_name] = __import__(package_name)
    except ImportError:
        import subprocess
        subprocess.check_call(["python", "-m", "pip", "install", package_name])
        globals()[package_name] = __import__(package_name)

import_or_install(package_name="requests")
import_or_install(package_name="argparse")
#import requests
#import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--name", "-n", type=str, dest="name", required=True) # alias : -n
parser.add_argument("--description", "-d", type=str, dest="is_description", default="nono", required=False) # alias : -d
parser.add_argument("--private", "-p", dest="is_private", #action="store_true", 
                    required=False, type=str , default="false" ) # alias : -p
parser.add_argument("--github_token", "-g", type=str, dest="github_token", required=True) # alias : -g
args = parser.parse_args()

repo_name = args.name
is_private = args.is_private
description = args.is_description


GITHUB_TOKEN = args.github_token


API_URL = "https://api.github.com"
paylod = '{"name": "%s", "private":  %s , "description": "%s"}' %(repo_name, is_private, description)
headers = {
    "Authorization": "token " + GITHUB_TOKEN,
    "Accept": "application/vnd.github.v3+json",
}

try :
    r= requests.post(API_URL + "/user/repos", data = paylod, headers = headers)
    r.raise_for_status()
except Exception as error :
    raise SystemExit(error)

# exemple run :
# python create_repos_on_gith_with_token.py --name tools_private --private true --description "begin tools_private" --github_token "your github token"
# python create_repos_on_gith_with_token.py --github_token "your github token" --name tools_public --private false --description "begin tools_public" 

# avec les alias 
# python create_repos_on_gith_with_token.py -g "your github token" -n tools_public -p false -d "begin tools_public" 

