import sys, os
#sys.path.insert(0, r'C:\Users\yasha\Visual Studio Code Workspaces\SystemX\ResideImageScrapper')
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
import json
import time
from ImageLibrary.library import *


cache = ImagingLibraryManager()

class RentcastListing():

    def __init__(self, listing_json):
        self._exists_in_cache = False

        self.listing_properties = {
            'Address':listing_json["addressLine1"],
            'City':listing_json["city"],
            'State':listing_json["state"]
        }


    def search_in_cache(self):
        response = cache.directory().State( STATE_ABBREVIATION[self.listing_properties['State']]).City(self.listing_properties['City']).Listing(self.listing_properties['Address']).Search()
        return response
    
    def print(self):
        print("____RentCastListing____")
        print("Address:", self.listing_properties['Address'])
        print("City:", self.listing_properties['City'])
        print("State:", self.listing_properties['State'])
        print("\n\n")

    def get(self, property):
        try:
            return self.listing_properties[property]
        except Exception as error:
            return False
        
    def set(self, property, value):
        try:
            self.listing_properties[property] = value
            return True
        except Exception as error:
            return False


def RentcastList():
    file = open(r"C:\Visual Studio Code Workspaces\SystemX\ResideImageScrapper\Server\rentcast.json")
    rencast_list = json.load(file)
    print(rencast_list["rentcast_response"][0])
    RentCastListings = []


    match_count = 0
    for i in range(0, len(rencast_list["rentcast_response"])):
        listing = RentcastListing(rencast_list["rentcast_response"][i])
        val = listing.search_in_cache()
        print("\x1b[32m RESPONSE:\x1b[0m:", val, "  \x1b[31miteration:\x1b[0m", i)
        if(val != False): 
            match_count+= 1
            RentCastListings.append(listing)
   


    print("Total Rent Cast Listins: " + str(len(rencast_list["rentcast_response"])))
    print("Matched Cache Listing: " + str(match_count))

#Model rentcast listing objects
#Compare them with library objects

RentcastList()