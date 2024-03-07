import requests


ip = "127.0.0.1"
port = 5000

url = "http://localhost:"+str(port)+"/automations/query="

dict = {
            "service_type":"image_collection",
            "service_name":"redfin",
            "client_request_data":{
                "filters":["For sale"],
                "listing_requested":{
                    "type":"city&state",
                    "area":["Otay Mesa, CA"],
                    "storage":"cache"
                    }
                }
            }


header = {'Content-Type': 'application/json'}
#response = requests.post(url, json=dict, headers=header)
url += str(dict)
response = requests.post(url, headers=header)