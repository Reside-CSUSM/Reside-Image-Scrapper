import json

class ListingHandler():

    def __init__(self):
        self.file_address = ""
        self.city = ""
        self.current_listing = ""
    
    def __update_city(self, city):
        self.city = city
        pass

    def Fetch(self, address):
        #OPEN A FILE AND SEARCH USING REGEX
        #OPEN UP FILE PATH
        return self.current_listing + " Fetch"
        pass

    def Delete(self, address):
        #OPEN A FILE AND DELETE USING REGEX
        return self.current_listing + " Delete"
        pass

    def Update(self, address):
        #OPEN A FILE AND UPDATE USING REGEX4
        return self.current_listing + " Update"
        pass

    def Create(self, data):
        return self.current_listing + " Create"
        pass

    def Listing(self, name):
        self.current_listing = name
        return self



class CityHandler():

    def __init__(self):
        self.folder_address = ""
        self.city_file = ""
        self.state = ""
        self.current_city = ""
        self.listing_handler = ListingHandler()

    def __update_state(self, value):
        self.state = value

    def Create(self):
        #CREATE A CITY FILE
        #OPEN UP FILE PATH
        return self.current_city + " Create"
    
    def Delete(self):
        #DELETE A CITY FILE
        #OPEN UP FILE PATH
        return self.current_city + " Delete"

    def Update(self):
        #OPEN UP FILE PATH
        return self.current_city + " Update"
    
    def Fetch(self):
        #SEARCH FOR THE FILE NAME
        #OPEN UP FILE PATH
        return self.current_city + " Fetch"

    def City(self, city):
        self.current_city = city
        self.listing_handler.__update_city(self.state + ", " + city)
        return self
    
    def Listing(self, name):
        self.listing_handler.Listing(name)
        return self.listing_handler


class StateHandler():

    def __init__(self):
        self.folder_address = ""
        self.folder_name = ""
        self.city_handler = CityHandler()
        self.current_state = ""
    
    def Fetch(self):
        #FETCH THE STATE
        #OPEN UP THE PATH
        return self.current_state + " Fetch"
    
    def Create(self):
        #CREATE FOLDER
        #OPEN UP THE PATH
        return self.current_state +  " Create"
    
    def Update(self):
        #UPDATE STATE
        #OPEN UP THE PATH
        return self.current_state + " Update"

    def Delete(self):
        #DELETE FOLDER 
        #OPEN UP THE PATH
        return self.current_state  + " Delete"
    
    def State(self, name):
        self.current_state = name
        self.city_handler.__update_state(name)
        return self

    def City(self):
        return self.city_handler


class ListingAttributes():

    def __init__(self):
        self._attributes = {
            'address':None,
            'images':[],
            'price':None,
            'beds':None,
            'baths':None,
            'state':None,
            'city':None,
            'zipcode':None,
            'street':None
        }
    
    def getter(self, type):
        pass

    def setter(self):
        pass

    def getter(self):
        pass


class ListingPointer():

    def __init__(self):
        self.attributes = ListingAttributes()
        pass

    def __format(self):
        pass
    
    def attribute(self):
        return self.attributes
    
    def export(self):
        pass


class MicroBucket():

    def __init__(self):
        self.data = ""

    def get(self):
        return self.data
    
    def put(self, data):
        self.data = data


class ImagingLibraryManager():

    def __init__(self):
        self.state_handler = StateHandler()
       
    def SearchListing(self, listing_data):
        listing = ListingPointer(listing_data)
        state = listing.attribute().getter('state')
        city = listing.attribute().getter('city')
        street = listing.attribute().getter('street')
        address = listing.attribute().getter('address')
        self.state_handler.FetchState(state).CityHandler().FetchCityFile(city).ListingHandler().FetchListing(address)

    def command(self):
        return self.state_handler

manager = ImagingLibraryManager()
value = manager.command().State("California").City("San Diego").Listing("3045 Main St, san diego, CA 91912").Create("something")
print(value)
#state.State("Texas").City("Austin").Listing("1024 Main St, Austin, TX 91909").Fetch()
""" 
Manager:
    - State:
        - State()
        - Fetch = state directory
        - Update = state directory
        - Delete = state directory

        - City:
            - City()
            - Fetch = city file
            - Update = city file
            - Delete = state directory

            - Listing:
                - Listing()
                - Fetch = json object
                - Update = json object
                - Delete = json object
"""