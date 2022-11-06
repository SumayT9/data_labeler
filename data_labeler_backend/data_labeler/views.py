from django.shortcuts import render
from django.http import JsonResponse
import requests
from lxml import html
from lxml.html.clean import Cleaner
import os


def send_xpaths(request):
    url = request.GET.get("query")
    sitename = url.split("/")[2]
    response = {"field" :[], "xpath" : [], "renderPath": []}
    if sitename + ".txt" in os.listdir("../data_paths/"):
        with open("../data_paths/" + sitename + ".txt") as xpath_file:
            for line in xpath_file.readlines():
                field, xpath, render_path = line.split("|")
                response["field"].append(field)
                response["xpath"].append(xpath)
                response["renderPath"].append(render_path)
    print(response)
    return JsonResponse(response)


    



def set_field(request):
    label = request.GET.get("label")
    print(label)
    with open("../data_paths/labels.txt", "w") as label_file:
        label_file.write(label)
    data  = {"raw" : "successful label change"}
    return JsonResponse(data)

def write_to_file(request):
    data = request.GET.get("text").split("|")
    text = data[0]
    url = data[1]
    render_path = data[2]
    sitename = url.split("/")[2]
    xpath = extract_xpath(url, text)
    field = ""
    with open("../data_paths/labels.txt", "r") as name_file:
        field = str(name_file.readline())
    with open("../data_paths/" + sitename + ".txt", "a") as data_file:
        data_file.write(field + "|" + xpath + "|" + render_path + "\n")

    data  = {"raw" : "successful"}
    return JsonResponse(data)

def extract_xpath(url, text_data):
    print("extracting xpath")
    page = requests.get(url)
    tree = html.fromstring(page.text)
    xpath = ""
    site_text = text_data.strip().replace("\n", "").replace(" ", "")
    with open("base.txt", "w") as base_file:
        base_file.write(site_text)
    for tag in tree.iter():
        try:
            if tag.text_content() and tag.tag not in ["script", "noscript", "comment"]:
                tag_text = tag.text_content().strip().replace("\n", "").replace(" ", "")
                with open("tag.txt", "a") as f:
                    f.write(tag_text)
                if tag_text == site_text:
                    if tag.tag == "li":
                        tag = tag.getparent()
                    xpath = tag.getroottree().getpath(tag)
                    print(xpath)
                    return xpath
        except:
            continue
    return xpath
    
