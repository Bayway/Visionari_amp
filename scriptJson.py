#!/usr/bin/python

import json
import requests
import feedparser
import time
from subprocess import check_output
from bs4 import BeautifulSoup
import sys

feed_name = 'VISIONARI'
url = 'https://medium.com/@visionari/latest?format=json'

db = 'feeds.json'

#
# function to get the current time
#
def save_post_in_file(jsonData):
    with open(db, 'w') as database:
        json.dump(jsonData, database, indent=4)
        return True
    return False




r = requests.get(url)
# Clean the wrong output and load json data
jsonData = json.loads(r.text.replace("])}while(1);</x>", "", 3))
save_post_in_file(jsonData)
#print(json)

