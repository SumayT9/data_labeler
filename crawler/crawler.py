from operator import truediv
from lxml import html
import requests
from googlesearch import search
import os

def search_google(person):
    query = person
    for url in search(query):
        sitename = url.split("/")[2]
        if sitename + ".txt" in os.listdir("data_paths"):
            fpath = "data_paths/" + sitename + ".txt"
            get_info(url, fpath)
            

def get_info(url, fpath):
    page = requests.get(url)
    tree = html.fromstring(page.text)
    with open(fpath, "r") as xpaths:
        for x in xpaths.readlines():
            label, data = x.split("|")
            if x:
                relevant = tree.xpath(data)
                for item in relevant:
                    print(label, item.text_content())
    
search_google("Joel Neal")