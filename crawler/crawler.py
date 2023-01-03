import sys
sys.path.insert(1, '../data_labeler_backend/') # avoiding import issues
from data_labeler.wrapper import WrapperInductor
from lxml import html
import requests
from googlesearch import search
import os

def crawl(person: str):
    """
    input: person - name of professor to search
    output: data (dictionary) - extraction results using wrapper induction system
    """
    query = person
    data = {}
    for url in search(query + "faculty profile"):
        sitename = url.split("/")[2]
        if sitename + "_wrapper.json" in os.listdir("../data_paths"):
            wi = WrapperInductor(wrapper_file="../data_paths/" + sitename + "_wrapper.json")
            data = wi.extract_text(url)
            print()
            for key in data.keys():
                for item in data[key]:
                    print(key + " : " + item)
    if not data:
        print("No wrapper found for " + person + "'s institution. Use chrome extension to create one!")

    return data
            
if __name__ == "__main__":    
    crawl("Ehsan Adeli")

