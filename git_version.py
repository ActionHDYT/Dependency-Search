import requests as re
from bs4 import BeautifulSoup


def split_file(lastest_version):
    split = lastest_version.split("-")
    one = split[3]
    lastest_version = one
    return lastest_version

def get_version(URL):
    global lastest_version
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    page = re.get(URL, headers=headers).content

    soup = BeautifulSoup(page, 'html.parser')
    lastest_version = soup.find("a", attrs={"id":"auto-download-link"})["href"]
    return lastest_version

def check_version(URL, current_version):
    latest_version = split_file(get_version(URL))
    if not latest_version == current_version:
        #print(f"Git - new version available")
        package_name = "Git"
        version = f"{current_version} → {latest_version}"
        return package_name, current_version, latest_version
    else:
        #print(f"Git - no update available")
        package_name = "Git"
        return package_name, current_version, ""
        

