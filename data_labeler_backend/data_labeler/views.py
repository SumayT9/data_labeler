from django.shortcuts import render
from django.http import JsonResponse
import requests
from lxml import html
from lxml.html.clean import Cleaner
import os
import json

from data_labeler.wrapper import WrapperInductor

def set_field(request):
    label = request.GET.get("label")
    print(label)
    with open("../data_paths/labels.txt", "w") as label_file:
        label_file.write(label)
    data  = {"raw" : "successful label change"}
    return JsonResponse(data)

def train_wrapper(request):
    data = request.GET.get("text").split("|")
    text = data[0]
    url = data[1]
    sitename = url.split("/")[2]
    field = ""
    with open("../data_paths/labels.txt", "r") as name_file:
        field = str(name_file.readline())
    wrapper_data = {
        "urls" : [],
        "texts" : [],
        "labels" : []
    }
    if sitename + ".json" in os.listdir("../data_paths"):
        with open("../data_paths/" + sitename + ".json", "r") as wrapper_file:
            wrapper_data = json.load(wrapper_file)
    
    wrapper_data["urls"].append(url)
    wrapper_data["texts"].append(text)
    wrapper_data["labels"].append(field)
    
    train_dict = {}
    for i in range(len(wrapper_data["urls"])):
        if wrapper_data["urls"][i] not in train_dict:
            train_dict[wrapper_data["urls"][i]] = {"texts" : [], "labels" : []}
        
        train_dict[wrapper_data["urls"][i]]["texts"].append(wrapper_data["texts"][i])
        train_dict[wrapper_data["urls"][i]]["labels"].append(wrapper_data["labels"][i])

    urls = list(train_dict.keys())
    texts = [data["texts"] for _, data in train_dict.items()]
    labels = [data["labels"] for _, data in train_dict.items()]

    print(texts)
    



    wi = WrapperInductor(urls=urls, texts=texts, labels=labels)
    wi.save("../data_paths/" + sitename + "_wrapper.json")


    with open("../data_paths/" + sitename + ".json", "w") as data_file:
        json.dump(wrapper_data, data_file)

    data  = {"raw" : "successful"}
    return JsonResponse(data)

def extract_text(request):
    url = request.GET.get("query")
    sitename = url.split("/")[2]
    wi = WrapperInductor(wrapper_file="../data_paths/" + sitename + "_wrapper.json")
    data = wi.extract_text(url)
    print(data)
    return JsonResponse(data)
    
def debug(request):
    text = request.GET.get("query")
    with open("fails.txt", "a") as file:
        file.write(text + "\n" + "____________________________")
    return JsonResponse({"raw" : "W"})



    
