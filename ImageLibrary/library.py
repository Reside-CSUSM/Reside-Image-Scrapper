import json
import os


project_root = os.getcwd() 
project_root = r"C:\Users\yasha\Visual Studio Workspaces\SystemX\ResideImageScrapper"
CACHE_ROOT_DIRECTORY = project_root + r"\ImageLibrary\States"
STATE_ABBREVIATION = {
    'AL':'Alabama',
    'AK':'Alaska',
    'AZ':'Arizona',
    'AR':'Arkansas',
    'AS':'American Samoa',
    'CA':'California',
    'CO':'Colorado',
    'CT':'Connecticut',
    'DE':'Delaware',
    'DC':'District of Columbia',
    'FL':'Florida',
    'GA':'Georgia',
    'GU':'Guam',
    'HI':'Hawaii',
    'IL':'Illinois',
    'IN':'Indiana',
    'IA':'Iowa',
    'KS':'Kansas',
    'KY':'Kentucky',
    'LA':'Louisiana',
    'ME':'Maine',
    'MD':'Maryland',
    'MA':'Massachusetts',
    'MI':'Michigan',
    'MN':'Minnesota',
    'MS':'Mississippi',
    'MO':'Missouri',
    'MT':'Montana',
    'NE':'Nebraska',
    'NV':'Nevada',
    'NH':'New Hampshire',
    'NJ':'New Jersey',
    'NM':'New Mexico',
    'NY':'New York',
    'NC':'North Carolina',
    'ND':'North Dakota',
    'MP':'Northern Mariana Islands',
    'OH':'Ohio',
    'OK':'Oklahoma',
    'OR':'Oregon',
    'PA':'Pennsylvania',
    'PR':'Puerto Rico',
    'RI':'Rhode Island',
    'SD':'South Dakota',
    'SC':'South Carolina',
    'TN':'Tennessee',
    'TX':'Texas',
    'TT':'Territories',
    'UT':'Utah',
    'VT':'Vermont',
    'VA':'Virginia',
    'VI':'Virgin Islands',
    'WA':'Washington',
    'WV':'West Virginia',
    'WI':'Wisconsin',
    'WY':'Wyoming'
}

class ListingHandler():

    def __init__(self):
        self.file_path = ""
        self.city = ""
        self.current_listing = ""
        self.listing_path = ""
    
    def update_city(self, city):
        self.city = city

    def update_path(self, path):
        if(self.current_listing != ""): self.listing_path = path + "\\" + self.current_listing
        else: self.listing_path = path + "\\"
        print("Listing Path: ", self.listing_path)

    def Fetch(self):
        try:
            file = open(self.listing_path, "r+")
            map = json.load(file)
            file.close()
            return map["image_urls"]
        except FileNotFoundError as error:
            return False
    
    def Delete(self):
        #OPEN A FILE AND DELETE USING REGEX
        #NEED TO FIX THIS, [PERMISSION ERROR]
        try:
            file = open(self.listing_path, "r")
            os.remove(self.listing_path)
            file.close()
            return True
        except FileNotFoundError as error:
            print(error)
            return False


    def Search(self):
        print("INSIDE SEARCH")
        if(self.current_listing == ""): return False
        try:
            index = self.listing_path.rfind("\\")
            string = self.listing_path[index+1:len(self.listing_path)]
            dirs = os.listdir(self.listing_path[0:index])
            if(string in dirs):
                return True
            else:
                return False
        except Exception as error:
            print(error)
            return False

    def PutData(self, content):
        try:
            file = open(self.listing_path, "w")
            file.write(json.dumps(content, indent=4))
            return True
        except Exception as error:
            return False
    
    def Create(self, json_data=None):
        #NEED TO CHECK IF THE FILE ALREADY EXISTS
        #IF IT DOES THEN DON'T CREATE IT
        try:
            #If file already exists then return false
            file = open(self.listing_path+".json", "w")
            file = open(self.listing_path+".json", "w")
            if(json_data != None):file.write(json.dumps(json_data, indent=4))
            file.close()
            return True
        except Exception as error:
            #If the file doesn't exist then we have to create it
            return False
        
    def Listing(self, name=None):
        if(name == None):
            self.current_listing = ""
            pass
        else:
            self.current_listing = name
        return self

    def GetAll(self):
        if(self.current_listing != ""): return False
        try:
            string = self.listing_path[0:len(self.listing_path)-1]
            print(string)
            dirs = os.listdir(string)
            return dirs
        except Exception as error:
            print(error)
            return False

class CityHandler():

    def __init__(self):
        self.folder_address = ""
        self.city_file = ""
        self.city_path = ""
        self.state = ""
        self.current_city = ""
        self.listing_handler = ListingHandler()

    def update_state(self, value):
        self.state = value

    def update_path(self, path):
        if(self.current_city != ""):self.city_path = path + "\\"  + self.current_city
        elif(self.current_city == ""): self.city_path = path + "\\"
        print("City Path:", self.city_path)

    def Create(self):
        #CREATE A CITY FOLDER
        #OPEN UP FILE PATH
        try:
            os.mkdir(self.city_path)
            return True
        except Exception as error:
            return False
    
    def Search(self):
        try:
            index = self.city_path.rfind("\\")
            string = self.city_path[index+1:len(self.city_path)]
            dirs = os.listdir(self.city_path[0:index])
            if(string in dirs):
                return True
            else: return False
        except Exception as error:
            return False

    def Delete(self):
        #DELETE A CITY FOLDER
        #OPEN UP FILE PATH
        try:
            dir = os.remove(self.city_path)
            return True
        except Exception as error:
            return False
    
    def Fetch(self):
        #SEARCH FOR THE FILE NAME
        #OPEN UP FILE PATH
        return self.current_city + " Fetch"

    def City(self, city=None):
        if(city == None):
            self.current_city = ""
        else:
            self.current_city = city
        print("VALL", self.current_city)
        return self
    
    def Listing(self, name=None):
        self.listing_handler.Listing(name)
        self.listing_handler.update_city(self.current_city)
        self.listing_handler.update_path(self.city_path)
        return self.listing_handler

    def GetAll(self):
        if(self.current_city != ""): return False
        try:
            string = self.city_path[0:len(self.city_path)-1]
            print(string)
            dirs = os.listdir(string)
            return dirs
        except Exception as error:
            print(error)
            return False
        
class StateHandler():

    def __init__(self):
        self.folder_address = ""
        self.folder_name = ""
        self.city_handler = CityHandler()
        self.current_state = ""
        self.state_path = CACHE_ROOT_DIRECTORY + "\\" + self.current_state
    
    def update_path(self):
        if(self.current_state != ""): self.state_path = CACHE_ROOT_DIRECTORY + "\\" + self.current_state
        elif(self.current_state == ""): self.state_path = CACHE_ROOT_DIRECTORY + "\\"
        print("State Path:", self.state_path)

    def Fetch(self, name=None):
        #OPEN UP THE PATH
        #FETCH THE STATE
        try:
            city_folders = os.listdir(self.state_path)
            pass
        except Exception as error:
            pass
        return self.current_state + " Fetch"
    
    def Create(self):
        #CREATE FOLDER
        #OPEN UP THE PATH
        try:
            os.mkdir(self.state_path)
            return True
        except Exception as error:
            return False
        

    def Search(self):
        if(self.current_state == ""): return
        try:
            index = self.state_path.rfind("\\")
            string = self.state_path[index+1:len(self.state_path)]
            dirs = os.listdir(self.state_path[0:index])
            if(string in dirs):
                return True
            else: return False
        except Exception as error:
            return False

    def Delete(self):
        #DELETE FOLDER 
        #OPEN UP THE PATH
        try:
            value = os.remove(self.state_path)
            print("deleting:", value)
            return True
        except Exception as error:
            print(error)
            return False
            pass
    
    def State(self, name=None):
        if(name == None):
            self.current_state = ""
        else:
            self.current_state = name
        
        self.update_path()
        return self

    def City(self, name=None):
        self.city_handler.City(name)
        self.city_handler.update_state(self.current_state)
        self.city_handler.update_path(self.state_path)
        return self.city_handler

    def GetAll(self):
        if(self.current_state != ""): return False
        try:
            string = self.state_path[0:len(self.state_path)-1]
            print(string)
            dirs = os.listdir(string)
            return dirs
        except Exception as error:
            print(error)
            return False
        
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

    def set(self, type, value):
        try:
            self._attributes[type] = value
            return True
        except Exception as error:
            return False



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


#api = ImagingLibraryManager()
#print(api.directory().State("California").City("San Diego").Listing().Create("13607 Caldwell Dr #36, Austin, TX", json.dumps(data, indent=4)))
#"13607 Caldwell Dr #36, Austin, TX"

#print(api.directory().State("California").City("San Diego").Listing("13604 Caldwell Dr #36, Austin, TX").Fetch())
#print(api.directory().State("California").City("San Diego").Listing("13604 Caldwell Dr #36, Austin, TX").Search())
#print(api.directory().State("California").City("Los Alamos").Create())
#print(api.directory().State("California").City("San Diego").Listing().GetAll())


""" 
GENERAL IDEA:
Directory():
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