from packaging import version
import pandas as pd
import requests as re


def get_response(URL):
    global response
    response = re.get(URL)
    
def create_dataframe():
    global df
    table = pd.read_html(response.content)
    df = pd.DataFrame(table[0])


def get_all_versions():
    global all_versions
    all_versions = []
    for i in df["Name"]:

        try:
            if i.startswith("v") and version.InvalidVersion(i):
                if not i.split("v")[1].split("/")[0] == "CVS":
                    all_versions.append(i.split("v")[1].split("/")[0])
        except:
            pass
        
def get_versions_by_start(start):
    all_versions_by_start = []
    for i in all_versions:
        if i.startswith(str(start)):
            all_versions_by_start.append(i)
    return all_versions_by_start

def get_latest_version():
    return max(all_versions, key=version.parse)
        
def main(URL, current_version):
    get_response(URL)
    create_dataframe()
    get_all_versions()
    
    if current_version == max(all_versions, key=version.parse):
        return "Cmake", current_version, "", ""
    elif current_version == max(get_versions_by_start(f"{version.Version(current_version).major}"), key=version.parse):
        return "Cmake", current_version, "", get_latest_version()
    else:
        
        return "Cmake", current_version, max(get_versions_by_start(f"{version.Version(current_version).major}"), key=version.parse), get_latest_version()
