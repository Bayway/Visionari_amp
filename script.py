#!/usr/bin/python

import feedparser
import time
from subprocess import check_output
from bs4 import BeautifulSoup
import sys

feed_name = 'VISIONARI'
url = 'https://medium.com/feed/visionari'

#feed_name = sys.argv[1]
#url = sys.argv[2]

db = 'feeds.db'
limit = 12 * 3600 * 1000

#
# function to get the current time
#
current_time_millis = lambda: int(round(time.time() * 1000))
current_timestamp = current_time_millis()

def post_is_in_db(post):
    with open(db, 'r', encoding='utf-8') as database:
        for line in database:
            if post in line:
                return True
    return False

# return true if the post is in the database with a timestamp > limit
def post_is_in_db_with_old_timestamp(post):
    with open(db, 'r', encoding='utf-8') as database:
        print(database.readlines())
        for line in database.readlines():
            if post in line:
                result = line.split('|', 1)
                ts_as_string = line.split('|', 1)[5]
                ts = int(ts_as_string)
                if current_timestamp - ts > limit:
                    return True
    return False

#
# get the feed data from the url
#
feed = feedparser.parse(url)

#
# figure out which posts to print
#
posts_to_print = []
posts_to_skip = []

for post in feed.entries:
    # if post is already in the database, skip it
    # TODO check the time
    statusupdate = post.content
    soup = BeautifulSoup(statusupdate[0]['value'])
    print("IMG------------------>" + soup.find("img")["src"])
    title = post.title
    description = str(soup.find("h4"))
    image = soup.find("img")["src"]
    link = post.link
    date = post.published
    result = title + "|" + description + "|" + image + "|" + link  + "|" + date
    if post_is_in_db_with_old_timestamp(result):
        posts_to_skip.append(result)
    else:
        posts_to_print.append(result)
    
#
# add all the posts we're going to print to the database with the current timestamp
# (but only if they're not already in there)
#
f = open(db, 'a', encoding='utf-8')
for post in posts_to_print:
    if not post_is_in_db(post):
        f.write(post + "|" + str(current_timestamp) + "\n")
f.close
    
#
# output all of the new posts
#
count = 1
blockcount = 1
for post in posts_to_print:
    if count % 5 == 1:
        print("\n" + time.strftime("%a, %b %d %I:%M %p") + '  ((( ' + feed_name + ' - ' + str(blockcount) + ' )))')
        print("-----------------------------------------\n")
        blockcount += 1
    print(post + "\n")
    count += 1