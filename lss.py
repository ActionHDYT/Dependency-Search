import requests as re
from bs4 import BeautifulSoup


def split_file(lastest_version):
    split = lastest_version.split("-")
    one = split[1]
    two = split[2]
    lastest_version = f"{one}-{two}"
    return lastest_version

def get_version(URL):
    global lastest_version
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    page = re.get(URL, headers=headers).content

    soup = BeautifulSoup(page, 'html.parser')
    lastest_version = soup.find_all("ul", attrs={"class":"RefList-items"})[1]
    lastest_version = lastest_version.find("a").text
    
    return lastest_version

def get_old_version(URL):
    global old_version
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    page = re.get(URL, headers=headers).content

    soup = BeautifulSoup(page, 'html.parser')
    old_version = soup.find_all("ul", attrs={"class":"RefList-items"})[1]

    old_version = old_version.find_all("a")[1].text
    return old_version

def check_version(URL, current_version):
    latest_version = get_version(URL)
    if not latest_version == current_version:
        #print(f"ISS - new version available")
        package_name = "ISS"
        if get_old_version(URL) == current_version:
            return package_name, current_version, "", latest_version
        elif current_version.startswith(old_version.split(".")[0]):
            return package_name, current_version, get_old_version(URL), latest_version
        else:
            return package_name, current_version, "", latest_version
    else:
        #print(f"ISS - no update available")
        package_name = "ISS"
        return package_name, current_version, "", ""
    

        