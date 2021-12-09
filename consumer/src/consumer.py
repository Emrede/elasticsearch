#!/usr/bin/python

import time
from elasticsearch import Elasticsearch

filePath = "hedef.txt"


def query(es, index, mins, string):
    result = es.search(index=index, body={
        "query": {
            "bool": {
                "must": [
                    {
                        "match_phrase": {
                            "text": "%s" % string
                        }
                    },
                    {
                        "range": {
                            "timestamp": {
                                "gte": "now-%dm" % mins,
                                "lt":  "now"
                            }
                        }
                    }
                ]
            }
        }
    })
    return result


print("# Consumer starting ...")
try:
    with open(filePath) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        searchString = lines[0]
except:
    print("# Failed to open target text file.")
    # If can't read the file
    # searchString = "Onur 192.168.1.12 server4"
    exit(1)

# Connect to server
while True:
    es = Elasticsearch("elasticsearch")
    if not es.ping():
        print("# Connection failed.")
        time.sleep(1)
        continue
    print("# Connection established.")
    break

print("# Search string:" + searchString)

while True:
    # Check flag status
    try:
        # Try to read progress, create if it doesn't exist
        res = es.get(index="progress", id=1)
        print('# Progress flag:', end='')
        print(res['found'])
    except Exception as e:
        print("# Adding progress flag")
        # Mark consumer as active
        res = es.index(index="progress", id=1, body={"stringFound": False})
    break

while True:
    # Get last minute results
    try:
        res = query(es, "test-index", mins=1, string=searchString)
    except Exception as e:
        print(e)
        time.sleep(1)
        continue
    resLen = len(res["hits"]["hits"])
    print("# Found %d records" % resLen)
    if(resLen > 0):
        print("%s - Basarili" % res["hits"]["hits"][0]["_source"]["text"])
        print("# Setting progress flag")
        res = es.index(index="progress", id=1, body={"stringFound": True})
        print("# Consumer exiting.")
        exit(0)
    # print(res)
    time.sleep(1)
