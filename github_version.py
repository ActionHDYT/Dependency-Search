import requests as re
from dotenv import load_dotenv
from os import environ

load_dotenv()

KEY = environ.get("KEY")




def get_repo_owner(URL):
    global owner, repo
    split = URL.split("/")
    owner = split[3]
    repo = split[4]
    return owner, repo
    
    
    
def get_latest(URL):
    global lastest_release
    owner, repo = get_repo_owner(URL)
    headers = {'Authorization': KEY}
    response = re.get(f"https://api.github.com/repos/{owner}/{repo}/releases/latest", headers=headers)
    try:
        lastest_release = response.json()["name"]
        return lastest_release
    except:
        print(response.json()['message'])
        exit()
        
def get_date(URL):
    global lastest_release_date
    headers = {'Authorization': KEY}
    response = re.get(f"https://api.github.com/repos/{owner}/{repo}/releases/latest", headers=headers)
    try:
        lastest_release_date = response.json()["published_at"]
        return lastest_release_date
    except:
        print(response.json()['message'])
        exit()
    
    
def check_version(URL, current_version, by_date=False):
    if by_date:
        get_date(URL)
        if not lastest_release_date == current_version:
            #print(f"{repo} - new version available")
            version = f"{current_version} → {lastest_release_date}"
            return repo, version
        else:
            #print(f"{repo} - no update available")
            return repo, current_version, ""
    else:
        get_latest(URL)
        if not lastest_release == current_version:
            #print(f"{repo} - new version available")
            version = f"{current_version} → {lastest_release}"
            return repo, version
        else:
            #print(f"{repo} - no update available")
            return repo, current_version, ""
        

