import requests
import copy



class Response():

    def __init__(self):
        pass

class ImagingAPI():

    def __init__(self):
        self.proto = "http://"
        self.server_ip = ""
        self.server_port = ""
        self.housing_list = []
        self.area_list = []

        self.housing_payload = {
            "service_type":"image_collection",
            "service_name":"redfin",
            "client_request_data":{
                "listing_requested":{
                    "type":"housings",
                    "addresses":[],
                    "storage":"cache"
                    }
               }
            }
        #"5210 Rain Creek Pkwy, Austin, TX", "7122 Wood Hollow Dr 13, Austin, TX", "2914 Sorin St, Austin, TX", "6303 Dorchester Dr, Austin, TX 78723"
        self.area_payload = {
            "service_type":"image_collection",
            "service_name":"redfin",
            "client_request_data":{
                "filters":[""],
                "listing_requested":{
                    "type":"city&state",
                    "area":[],
                    "storage":"cache"
                    }
            }
        }
        #"san diego, CA", "Austin, TX", "Sacramento, CA"

    
    def initialize(self, ip, port):
        self.server_ip = ip
        self.server_port = port

    def add_general_search_filter(self, filter):
        self.area_payload["client_request_data"]["filters"].append(filter)

    def remove_general_search_filter(self, filter):
        index = 0
        for _filter in self.area_payload["client_request_data"]["filters"]:
            if(_filter == filter):
                self.area_payload["client_request_data"]["filters"].pop(index)
            index += 1

    def add_housings(self, address):
        self.housing_payload["client_request_data"]["listing_requested"]["addresses"].append(address)
        return self

    def add_areas(self, area):
        self.area_payload["client_request_data"]["listing_requested"]["area"].append(area)
        return self

    def search_area(self):
        url = self.proto + self.server_ip + ":"+str(self.server_port) + "/automations/query="
        string = str(self.area_payload)
        url += string
        headers = {'Content-Type': 'application/json'}
        req = requests.post(url, headers=headers)
        print(req)
        return self

    def search_housings(self):
        url = self.proto + self.server_ip + ":"+str(self.server_port) + "/automations/query="
        string = str(self.housing_payload)
        url += string
        headers = {'Content-Type': 'application/json'}
        req = requests.post(url, headers=headers)
        print(req)
        return self



image_api = ImagingAPI()
image_api.initialize("38.56.138.77", 8888)
image_api.add_housings("5210 Rain Creek Pkwy, Austin, TX").add_housings("7122 Wood Hollow Dr 13, Austin, TX").search_housings()
image_api.add_areas("san diego, CA").add_areas("Austin, TX").search_area()
