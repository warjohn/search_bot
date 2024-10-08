# -*- coding: utf-8 -*-
import requests
import json
import nest_asyncio

nest_asyncio.apply()

url = ""
data = {
    "query": "сколько общежитий в университете?",
    "result_column": "Answer"
}

payload = json.dumps(data)

headers = {
    'accept': "application/json",
    'Content-Type': "application/json"
    }

response = requests.request("POST", url, data=payload, headers = headers)

print(response.text)
