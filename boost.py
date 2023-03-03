import requests as re
from bs4 import BeautifulSoup

URL = "https://www.openssl.org/source/"

current_version = "openssl-1.0.1t.tar.gz"

def get_version():
    
    page = re.get(URL).content

    soup = BeautifulSoup(page, 'html.parser')

    table = soup.find("a", attrs={"href":"openssl-1.1.1t.tar.gz"}).text
    return table


if not current_version == get_version():
    print("new release available")

