import requests
import time
import json

"""
headers = {'Content-Type': 'application/json'}
data = {
    "search_config":199999
}
string_json = json.dumps(data)
req = requests.post('http://localhost:9999/automations/query=sandiego,CA', data=string_json, headers=headers)"""

url = 'http://38.56.138.77:8888/automations/query='

# Headers for the request
headers = {'Content-Type': 'application/json'}

# Data to be sent in the request body
data_S = {
    "automation_service_meta_data":{
        "type":"specific",
        "website": "any"
    },
    "filters":["","",""],
    "address":"San Diego"
    }

data_M = {
   "service_type":"image_collection",
   "service_name":"redfin",
   "client_request_data":{
      "filters":["For rent"],
      "listing_requested":{
         "type":"city&state",
         "area":["san diego, CA", "Austin, TX", "Sacramento, CA"],
         "storage":"cache"
      }
   }
}

data_R = {
   "service_type":"image_collection",
   "service_name":"redfin",
   "client_request_data":{
      "filters":["For rent"],
      "listing_requested":{
         "type":"housings",
         "addresses":["5210 Rain Creek Pkwy, Austin, TX", "7122 Wood Hollow Dr 13, Austin, TX", "2914 Sorin St, Austin, TX", "6303 Dorchester Dr, Austin, TX 78723"],
         "storage":"cache"
      }
   }
}
    #7122 Wood Hollow Dr #13, Austin, TX

string = '"{service_type":"image_collection","service_name":"redfin","client_request_data":"{"filters":["For rent"],"listing_requested":{"type":"city&state","area":"san diego, CA", "storage":"cache"}"}"}"'
s = str(data_M)
j = str(data_R)


# Convert data to JSON string
#string_json = json.dumps()

# Send POST request with JSON data
#url += '{"area":"AustinTX"}'
#req = requests.post(url, headers=headers)
url += j
req = requests.post(url, headers=headers)

# Check if the request was successful
if req.status_code == 200:
    print("Request successful")
    print("Response:", req.text)
else:
    print("Request failed with status code:", req.status_code)



"""
NOTE:
    GET
    - Routes:
         - /library:
            - /fetch specific:
            - /fetch an array of specific address

         POST/PUT
         - /bot:
            - /site_data=cache|return|discard:
                - /general
                - /specific

            - /any_site_data=cache|return|discard: (Must choose a prefered website)
                - /general
                - /specific

                
http://38.56.138.77:8888/automations/query={Address:1024 St, San Diego, CA}, {filters:'for-rent', 'sale','price=(10,1000)},{website=redfin, action=cache}

query {
    search_config:{
        type:'specific' | 'general' ,
        website: 'any' | 'redfin' ,
        result: cache | return | discard
    },
    bot_data:{
        filters:['','',''],
        address:'San Diego'
    }
}


 FOR AUTOMATION POST REQUEST ONLY
{
   "service_type":"image_collection",
   "service_name":"redfin",

   "client_request_data":{
      "filters:["","",""],
      listing_requested:{
         "type":"housings",
         "addresses":["1024 Main St, San diego, CA, 91912"],
         "storage":"cache"
      }

      listing_requested:{
         "type":"city&state",
         "area":san diego, CA,
         "storage":"cache"
      }
   }
}


FOR DATA FETCHING GET REQUEST ONLY


http://localhost:9999/automations/query={"search_config":1,"data":28777}
"""



"""
TODO:
 1) TEST Specific Search funcatinality  Done
 2) Test Multiple specific search funcationality  Done
 3) Implement ERROR codes as well.  Not Done
 4) Start preparing a quick API in java/python Done

 5) Implement auto folder add
   - Search for available automations
   - Add routes automatically

PROBLEMS:
 WHEN sending an address that contains  a special character like '#' the json.load() on server or the decoder won't process it and throw an error
 have to be able to find the addresses no matter what kind. 
 May need to seperate out /automations from /library endpoint on two different servers or processes since POST can be blocking. 
"""