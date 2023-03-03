from packaging import version
from packaging.utils import parse_sdist_filename
import pandas as pd
import requests as re
from bs4 import BeautifulSoup


    
def get_all_file_versions():
    global all_file_versions
    all_file_versions = []
    soup = BeautifulSoup(respone.content, 'html.parser')
    soup = soup.select("table")[0]
    table = pd.read_html(str(soup))
    df = pd.DataFrame(table[0])
    df = df.drop(columns=["Modified", "Size", "InfoDownloads / Week"])
    df = df.iloc[1:]
    df = df.iloc[:-1]
    for i in df["Name"]:
        all_file_versions.append(i)
    return all_file_versions
    
    
def get_all_versions():
    all_versions = []
    for i in get_all_file_versions():
        _, ver = parse_sdist_filename(i)
        all_versions.append(ver.base_version)
    return all_versions

def get_website(URL):
    global respone
    respone = re.get(URL)
            
def get_version_by_start(start):
    all_versions = get_all_versions()
    all_versions_by_start = []
    for i in all_versions:
        if i.startswith(str(start)):
            all_versions_by_start.append(i)
    return all_versions_by_start

def compare_versions(start):
    last_version = []
    for i in get_version_by_start(start):
        if start <= i:
            
            last_version.append(i)
    return max(last_version, key=version.parse)

def get_latest_version():
    all_versions = get_all_versions()
    return max(all_versions, key=version.parse)
            
def main(URL, current_version, by_major=False, by_minor=False):
    get_website(URL)
    if by_minor and not by_major:
        latest_minor = compare_versions(f"{version.Version(current_version).major}.{version.Version(current_version).minor}")
        if current_version == get_latest_version():
            return "Ipmiutil", current_version, "", ""
        if current_version == latest_minor:
            return "Ipmiutil", current_version, "", get_latest_version()
        else:
            return "Ipmiutil", current_version, latest_minor, get_latest_version()
    
    
    if by_major and not by_minor:
        latest_major = compare_versions(f"{version.Version(current_version).major}")
        if current_version == get_latest_version():
            return "Ipmiutil", current_version, "", ""
        if current_version == latest_major:
            return "Ipmiutil", current_version, "", get_latest_version()
        else:
            return "Ipmiutil", current_version, latest_major, get_latest_version()
    




