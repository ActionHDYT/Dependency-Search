import requests as re
import json
import semantic_version as sv
from packaging import version


def get_package_name(URL):
    split = URL.split("/")
    package_name = split[-2]
    return package_name

def get_last_version():
    last_release = data["info"]["version"]
    return last_release
    

    
def get_last_beta():
    last_beta_version = list(data["releases"].keys())[-1]
    return last_beta_version
    
def beta_available():
    if get_last_beta() == get_last_version():
        return False
    else:
        return True

def get_all_versions():
    all_versions = list(data["releases"].keys())
    return all_versions

def get_all_versions_by_start(major, beta=False):
    all_major = []
    all_versions = get_all_versions()
    for i in all_versions:
        if i.startswith(major):
            if version.Version(i).pre is not None and beta:
                all_major.append(i)
            elif version.Version(i).pre is None:   
                all_major.append(i)
    return all_major
    
def compare_versions(start, beta):
    last_version = []
    for i in get_all_versions_by_start(start, beta):
    
        if start <= i:
            
            last_version.append(i)
    return max(last_version, key=version.parse)
               
    
                    
                    

    
def check_version(URL, current_version, beta=False, by_major=False, by_minor=False):
    global data
    URL = URL + 'json'
    response = re.get(URL)
    data = response.json()
    package_name = get_package_name(URL)
    
    if by_major and not by_minor:
        current_version_major = str(version.Version(current_version).major)
        if compare_versions(current_version_major, beta) == current_version:
            return package_name, current_version, "", ""
        else:
            return package_name, current_version, compare_versions(current_version_major, beta), get_last_version()
    if by_minor and not by_major:
        current_version_major = version.Version(current_version).major
        current_version_minor = version.Version(current_version).minor
        if compare_versions(f"{current_version_major}.{current_version_minor}", beta) == current_version:
            return package_name, current_version, "", ""
        else:
            return package_name, current_version, compare_versions(f"{current_version_major}.{current_version_minor}", beta), get_last_version()
    if by_major and by_minor:
        return ("Provide by_major or by_minor", "")
    else:
        return ("Provide by_major or by_minor", "")
        
    
    
    # if beta and available:
    #     if not current_version == get_last_beta():
    #         beta = get_last_beta()
    #         # print(f"{package_name} - new beta release available ({beta})")
    #         version = f"{current_version} → (beta: {beta})"
    #         return package_name, version
    #     else:
    #         # print(f"{package_name} - no update available")
            
    #         return package_name, current_version
    # else:
    #     if by_major:
    #         current_version_major = str(sv.Version(current_version).major)
    #         return package_name, compare_versions(current_version_major)
    #     if by_minor:
    #         current_version_major = sv.Version(current_version).major
    #         current_version_minor = sv.Version(current_version).minor
    #         return package_name, compare_versions(f"{current_version_major}.{current_version_minor}")
            
    #     if not current_version == get_last_version():
    #         # print(f"{package_name} - new release available ({get_last_version()})")
    #         version = f"{current_version} → {get_last_version()}"
    #         return package_name, version
    #     else:
    #         # print(f"{package_name} - no update available")
    #         return package_name, current_version

    

    
    

#print(check_version("https://pypi.org/pypi/Django/", current_version="4.1rc1", by_minor=True, by_major=True, beta=True))
