#!/usr/bin/python

from datetime import datetime
import time
from elasticsearch import Elasticsearch
import random

user = "kullanici.txt"
ip = "ipaddress.txt"
server = "sunucu.txt"

filenames = [user, ip, server]
strippedLines = []

print("# Producer starting ...")
for filename in filenames:
    try:
        file = open(filename)
        lines = file.readlines()
        file.close()
    except Exception as e:
        print("# File couldn't be opened.")
        print(e)
        exit(1)
    strippedLines.append([line.rstrip() for line in lines])

str1 = ""

while True:
    es = Elasticsearch("elasticsearch")
    if not es.ping():
        print("# Connection failed. Trying to reconnect ...")
        time.sleep(1)
        continue
    print("# Producer connected.")
    break

while True:
    try:
        flag = es.get(index="progress", id=1)
        if(flag["_source"]["stringFound"]):
            print("# Producer exiting ...")
            exit()
    except Exception as e:
        pass

    str1 = ""
    # Select random entry for each file
    for list in strippedLines:
        randomElement = random.choice(list)
        str1 += randomElement + " "
        text = str1.rstrip()  # delete last whitespace

    print(text)
    doc = {
        'text': text,
        'timestamp': datetime.now()
    }
    # Push to elastic
    result = es.index(index="test-index", body=doc)
    # print(result['result'])
    time.sleep(1)
