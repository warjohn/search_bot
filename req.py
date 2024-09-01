import json
import requests


url = ""
# url = "http://localhost:8030/run_query/"
data = {
    "query": 'Сколько корпусов?',
    "result_column": "Answer"
}

payload = json.dumps(data)

headers = {
    'accept': "application/json",
    'Content-Type': "application/json"
}

response = requests.request("POST", url, data=payload, headers=headers)
print(response)



