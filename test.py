from packaging import version
from packaging.utils import parse_sdist_filename
import pandas as pd
import requests as re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import environ
import os
import json

load_dotenv()

KEY = environ.get("KEY")


headers = {'Authorization': KEY}
test = re.get("https://github.com/git/git/tags", headers=headers)
print(f"{{ 'response': {test} \}}".json())