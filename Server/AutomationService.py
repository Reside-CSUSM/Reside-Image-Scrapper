import sys 
sys.path.insert(0, r'C:\Users\yasha\Visual Studio Workspaces\SystemX\ResideImageScrapper')
from Router import RoutingTable
import copy
import json
import urllib.parse
import time

#AUTOMATION MODULES
from Redfin.interface import *
from Redfin.redfind_errors import *

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
        if(("/query=" in self.path) == False):
            print("\x1b[34m/QUERY=NOT FOUND\x1b[0m")
            return
        
        print("\x1b[34m/QUERY=FOUND!!\x1b[0m")
        string = copy.copy(self.path).replace("/query=","")
        #print("STRING: ", string)
        decoded_data = urllib.parse.unquote(string)
        decoded_data = decoded_data.replace("'", '"')
        print("Decoded DATA:", decoded_data)
        #parsed_data = json.loads(decoded_data)
            #print("After parsing:", parsed_data)
        #return parsed_data
        try:
            parsed_data = json.loads(decoded_data)
            #print("After parsing:", parsed_data)
            return parsed_data
        except Exception as error:
            print("Error coverting from json to python dict", error)
            try:
                decoded_data += ']'
                parsed_data = json.loads(decoded_data)
                print("Success on retrying the decoding tho...")
            except Exception as error:
                print("Failure on retrying to decode as well.....")
                pass


    def get_response(self):
        return self.responses

    def _handle(self, path):
        self.path = path
        response = self.__decode(path)
        print(response)


    def __POST(self):
        response = self.__decode(self.path)
        #Check Service Type
        if(response["service_type"] == "image_collection"):

            if(response["service_name"] == "redfin"):
                listing_requested = response["client_request_data"]["listing_requested"]
                type = listing_requested["type"]

                if(type == "housings"):
                    addresses = listing_requested["addresses"]
                    storage = listing_requested["storage"]
                
                    for address in addresses:
                        RedfinInterface.create_bot()
                        RedfinInterface.activate()
                        RedfinInterface.type("specific")
                        self.responses.append(RedfinInterface.search_images(address))
                        RedfinInterface.close_bot()
                    return self.responses

                elif(type == "city&state"):
                    filters = response["client_request_data"]["filters"]
                    areas = listing_requested["area"]
                    error_count = None
                    for area in areas:
                        RedfinInterface.create_bot()
                        RedfinInterface.activate()
                        RedfinInterface.type("general")
                        RedfinInterface.apply_filters(filters)
                        self.responses.append(RedfinInterface.search_images(area))
                        RedfinInterface.close_bot()
                    
                    for response in self.responses:
                        if(response in REDFIN_ERROR_CODES):
                            if(error_count == None):
                                error_count = 0
                            error_count += 1
                    
                    if(error_count != None):
                        if(error_count > 0):
                            return self.responses
                    
                    self.responses = True
                    return self.responses
            
            elif(response["service_name"] == "zillow"):
                self.responses = "No Automation Service Available For Zillow"
                return self.responses

            elif(response["service_name"] == "compass"):
                self.responses = "No Automation Service Available For Compass"
                return self.responses
        pass
    
    def __PUT(self):
        pass

    def __GET(self):
        pass

    def __DELETE(self):
        pass

    def handle(self, path, TYPE):
        #DECODE THE JSON DATA RECIEVED
        self.path = path
        if(TYPE == 'POST'):
            try:
                self.__POST()
            except Exception as error:
                print("POST ERROR:", error)
        
        elif(TYPE == 'GET'):
            self.__GET()
        
        elif(TYPE == 'PUT'):
            self.__PUT()
        
        elif(TYPE == 'DELETE'):
            self.__DELETE()


#NOTE SPECIFIC SEARCH THROUGH IMAGERY.PY NOT WORKING THROWS AN ERRO, ALSO HAVE TO TEST SPECIFIC SEARCH FUNCTION IF IT PUTS THINGS IN FILE