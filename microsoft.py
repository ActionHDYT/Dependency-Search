import requests as re
from bs4 import BeautifulSoup
import pandas as pd
from packaging import version



def get_versions(URL):
    global latest_version
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    page = re.get(URL, headers=headers).content

    soup = BeautifulSoup(page, 'html.parser')

    try:
        latest_version = soup.select("table")[1]
        table = pd.read_html(str(latest_version))[0]
        df = pd.DataFrame(table)
        all_versions = df["Version"]
        return all_versions
            
    except IndexError:
        latest_version = soup.select("table")[0]
        table = pd.read_html(str(latest_version))[0]
        all_versions = table["Version"]
        return all_versions


def get_latest_version(URL):
    all_versions = get_versions(URL)
    return max(all_versions, key=version.parse)

def get_all_versions_by_start(major, URL):
    all_major = []
    all_versions = get_versions(URL)
    for i in all_versions:
        if i.startswith(major):
            all_major.append(i)
    return all_major

def compare_versions(start, URL):
    last_version = []
    for i in get_all_versions_by_start(start, URL):
    
        if start <= i:
            
            last_version.append(i)
    return max(last_version, key=version.parse)


def check_version(URL, current_version, name, by_major=False, by_minor=False):
    all_versions = get_versions(URL)
    

    if by_major and not by_minor:
        current_version_major = str(version.Version(current_version).major)
        if current_version == compare_versions(current_version_major, URL):
            return name, current_version, ""
        else:
            return name, current_version, compare_versions(current_version_major, URL), get_latest_version(URL)
    if by_minor and not by_major:
        current_version_major = version.Version(current_version).major
        current_version_minor = version.Version(current_version).minor
        if current_version == compare_versions(f"{current_version_major}.{current_version_minor}", URL):
            return name, current_version, "", ""
        else:
            return name, current_version, compare_versions(f"{current_version_major}.{current_version_minor}", URL), get_latest_version(URL)

    else:
        # print(f"{name} - no update available")
        return name, current_version, "", ""


