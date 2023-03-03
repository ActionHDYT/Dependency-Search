import requests as re
from packaging import version
import json
from dotenv import load_dotenv
from os import environ

load_dotenv()

KEY = environ.get("KEY")

response = json.load(open("github_response_pretty.json", "r"))


def get_repo_owner(URL):
    global owner, repo
    split = URL.split("/")
    owner = split[3]
    repo = split[4]
    return owner, repo
    

def get_all_versions(beta):
    all_versions = []
    for i in response:
        try:
            split_version = i["ref"].split("/")[-1].split("v")[-1]
            version.Version(split_version)
            if beta:
                all_versions.append(split_version)
            elif not beta:
                if version.Version(split_version).is_prerelease:
                    pass
                else:
                    all_versions.append(split_version)
        except:
            pass
    return all_versions

def get_latest_version(beta):
    all_versions = get_all_versions(beta)

    return max(all_versions, key=version.parse)

def get_response(URL):
    global response
    headers = {'Authorization': KEY}
    response = re.get(URL, headers=headers).json()
    print(response)
    return response

def get_all_versions_by_start(start, beta):
    all_versions = get_all_versions(beta)
    all_versions_by_start = []
    for i in all_versions:
        if i.startswith(str(start)):
            all_versions_by_start.append(i)
    return all_versions_by_start

def main(URL, current_version, by_major=False, by_minor=False, beta=False):
    #get_response(URL + "/tags")
    get_all_versions(beta)


    
    if by_minor and not by_major:
        if current_version == max(get_all_versions_by_start(f"{version.Version(current_version).major}.{version.Version(current_version).minor}", beta), key=version.parse):
            return get_repo_owner(URL)[1], current_version, "", ""
        else:
            return get_repo_owner(URL)[1], current_version, max(get_all_versions_by_start(f"{version.Version(current_version).major}.{version.Version(current_version).minor}", beta), key=version.parse), get_latest_version(beta)

    if by_major and not by_minor:
        if current_version == max(get_all_versions_by_start(f"{version.Version(current_version).major}", beta), key=version.parse):
            return get_repo_owner(URL)[1], current_version, "", ""
        else:
            return get_repo_owner(URL)[1], current_version, max(get_all_versions_by_start(f"{version.Version(current_version).major}", beta), key=version.parse), get_latest_version(beta)


#print(main("https://github.com/git/git", "2.34.7", by_minor=True))
print(main("https://github.com/git/git", "1.1.1", by_minor=True, beta=False))