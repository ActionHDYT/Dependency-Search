import semantic_version as sv
from packaging import version
from packaging.utils import parse_wheel_filename, canonicalize_name
import pandas as pd
import requests as re
from bs4 import BeautifulSoup


    

def get_all_versions():
    soup = BeautifulSoup(response.content, 'html.parser')

    ol = soup.find_all("ol", attrs={"class":"list-row-container menu"})[1]
    span = ol.find_all("span", attrs={"class":"release-number"})
    global all_versions
    all_versions = []

    for i in span:
        all_versions.append(i.text.split(" ")[-1])
        
    return all_versions

def get_latest_version():
    return max(all_versions, key=version.parse)

def get_all_versions_by_start(start):
    versions = []
    for i in all_versions:
        if i.startswith(start):
            versions.append(i)
    return versions
        
def check_version(URL, current_version, by_major=False, by_minor=False):
    global response
    response = re.get(URL)
    all_versions = get_all_versions()
    if by_major and not by_minor:
        version_with_start = get_all_versions_by_start(str(version.Version(current_version).major))
        if get_latest_version() == current_version:
            return "Python", current_version, "", ""
        else:
            if max(version_with_start, key=version.parse) == current_version:
                return "Python", current_version, "", max(all_versions, key=version.parse)
            return "Python", current_version, max(version_with_start, key=version.parse), max(all_versions, key=version.parse)
        
    if by_minor and not by_major:
        version_with_start = get_all_versions_by_start(str(version.Version(current_version).major) + "." + str(version.Version(current_version).minor))
        if get_latest_version() == current_version:
            return "Python", current_version, "", ""
        else:
            if max(version_with_start, key=version.parse) == current_version:
                return "Python", current_version, "", max(all_versions, key=version.parse)
            else:
                return "Python", current_version, max(version_with_start, key=version.parse), max(all_versions, key=version.parse)

