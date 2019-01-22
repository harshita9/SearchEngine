import pprint
from crawler import crawler
import urllib2
import urlparse
from bs4 import BeautifulSoup
from bs4 import Tag
from collections import defaultdict
import redis
from pagerank import page_rank
import re

# Testing File for Lab 3
# What I did in crawler was that I saved the page ranks by descending order,
# using the direct urls of the pages instead of the doc id
# -Marinette

if __name__ == "__main__":
    redisConnection = redis.Redis()
    bot = crawler(redisConnection, "urls.txt")
    bot.crawl(depth=1)
    print "Printing Page Ranks:"
    pprint.pprint(bot.crawler_page_ranks())
