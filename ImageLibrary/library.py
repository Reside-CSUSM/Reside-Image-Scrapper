import json


class ListingHandler():

    def __init__(self):
        self.file_address = ""
        self.city = ""
        self.current_listing = ""
    
    def update_city(self, city):
        self.city = city

    
    def Fetch(self, address):
        #OPEN A FILE AND SEARCH USING REGEX
        #OPEN UP FILE PATH
        return self.current_listing + " Fetch"


    def Delete(self, address):
        #OPEN A FILE AND DELETE USING REGEX
        return self.current_listing + " Delete"
        

    def Update(self, address):
        #OPEN A FILE AND UPDATE USING REGEX4
        return self.current_listing + " Update"
    

    def Create(self, data):
        return self.current_listing + " Create"
    

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

    def update_state(self, value):
        self.state = value

    def Create(self, name):
        #CREATE A CITY FILE
        #OPEN UP FILE PATH
        return self.current_city + " Create"
    
    def Delete(self, name):
        #DELETE A CITY FILE
        #OPEN UP FILE PATH
        return self.current_city + " Delete"

    def Update(self, name):
        #OPEN UP FILE PATH
        return self.current_city + " Update"
    
    def Fetch(self, name):
        #SEARCH FOR THE FILE NAME
        #OPEN UP FILE PATH
        return self.current_city + " Fetch"

    def City(self, city):
        self.current_city = city
        self.listing_handler.update_city(self.state + ", " + city)
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
    
    def Fetch(self, name):
        #FETCH THE STATE
        #OPEN UP THE PATH
        return self.current_state + " Fetch"
    
    def Create(self, name):
        #CREATE FOLDER
        #OPEN UP THE PATH
        return self.current_state +  " Create"
    
    def Update(self, name):
        #UPDATE STATE
        #OPEN UP THE PATH
        return self.current_state + " Update"

    def Delete(self, name):
        #DELETE FOLDER 
        #OPEN UP THE PATH
        return self.current_state  + " Delete"
    
    def State(self, name):
        self.current_state = name
        self.city_handler.update_state(name)
        return self

    def City(self, name):
        self.city_handler.City(name)
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
    
    def get(self, type):
        try:
            return self._attributes[type]
        except Exception as error:
            pass
        pass

    def set(self):
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

    def directory(self):
        return self.state_handler
    


manager = ImagingLibraryManager()
value = manager.directory().State("California").City("San Diego").Listing("3045 Main St, san diego, CA 91912").Create("created")
print(value)
print(manager.directory().State("California").City("San Diego").Listing("2098 Mainst, Austin, TX").Create(""))

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