import sys 
sys.path.insert(0, r'C:\Users\yasha\Visual Studio Workspaces\SystemX\ResideImageScrapper')
from Router import RoutingTable
import copy
import json
import urllib.parse

#AUTOMATION MODULES
from Redfin.interface import *


class AutomationsHandler():

    def __init__(self):
        #Handles the automations.json and updates it 
        pass


class AvailableServices():

    def __init__(self):
        #Dynamically import modules of new automation folders/systems
        pass

    pass



class AutomationService():

    def __init__(self):
        self.router = RoutingTable()
        self.path = ""
        self.responses = []

    def __decode(self, path):
        self.path = path

        h = {"service_type": "image_collection", "service_name": "redfin", "client_request_data": {"filters": ["For-rent"], "listing_requested": {"type": "city&state", "area": "san diego, CA", "storage": "cache"}}}   
        print("\x1b[31mPATH\x1b[0m: ", self.path)
        if(("/query=" in self.path) == False):
            print("\x1b[34m/QUERY=NOT FOUND\x1b[0m")
            return
        
        print("\x1b[34m/QUERY=FOUND!!\x1b[0m")
        string = copy.copy(self.path).replace("/query=","")
        print("STRING: ", string)
        decoded_data = urllib.parse.unquote(string)
        decoded_data = decoded_data.replace("'", '"')
        #b = str(h)
        #b = b.replace("'", '"')
        print("Decoded DATA:", decoded_data)
        #print("DECODED: ", decoded_data)

        try:
            parsed_data = json.loads(decoded_data)
            print("After parsing:", parsed_data)
            return parsed_data
        except Exception as error:
            print("Error coverting from json to python dict", error)


    def get_response(self):
        return self.responses

    def _handle(self, path):
        self.path = path
        response = self.__decode(path)
        print(response)

    def handle(self, path):
        #DECODE THE JSON DATA RECIEVED
        response = self.__decode(path)
        #Check Service Type
        if(response["service_type"] == "image_collection"):

            if(response["service_name"] == "redfin"):
                filters = response["client_request_data"]["filters"]
                listing_requested = response["client_request_data"]["listing_requested"]
                type = listing_requested["type"]

                if(type == "housings"):
                    addresses = listing_requested["addresses"]
                    storage = listing_requested["storage"]
                    RedfinInterface.type("specific")
                    RedfinInterface.apply_filters(filters)

                    for address in addresses:
                        self.responses.append(RedfinInterface.search_images(address))
                    return self.responses

                elif(type == "city&state"):
                    area = listing_requested["area"]
                    RedfinInterface.type("general")
                    RedfinInterface.apply_filters(filters)
                    self.responses = RedfinInterface.search_images(area)
                    return self.responses
            
            elif(response["service_name"] == "zillow"):
                self.responses = "No Automation Service Available For Zillow"
                return self.responses


            elif(response["service_name"] == "compass"):
                self.responses = "No Automation Service Available For Compass"
                return self.responses
            pass