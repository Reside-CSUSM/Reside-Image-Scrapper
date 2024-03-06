import requests


ip = "127.0.0.1"
port = 5000

url = "http://localhost:"+str(port)+"/endpoint"

dict = {
    "Type":"ImageCollection"
}

header = {'Content-Type': 'application/json'}
response = requests.post(url, json=dict, headers=header)