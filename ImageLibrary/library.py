import json
import os
import copy

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

class CharGradient():
    def __init__(self, string, character, gradient_number=1):
        #NOTE: A gradient is particular section in string that is made up of single character
        #Example:  'Yaaashaswiiiiaaaaaa' here the gradient is 'aaaa' which can be manipulated in original string
        #Gradient number is a number that represents different section of gradient in same string
        self.string = string
        self.character = character
        self.gradient_number = gradient_number
        self.gradient = ""
        self.first_index = 0
        self.last_index = 0
        
        for j in range(0, self.gradient_number):
            #These two lines below only repeat if gradient_number > 1
            self.first_index = self.last_index

            self.gradient = ""

            #First index of gradient
            self.first_index = self.string[self.first_index:].find(self.character)
            self.last_index = None

            #Get the last index where the gradient ends
            for i in range(self.first_index, len(self.string)):
                if(self.string[i] != self.character):
                    self.last_index = i
                    break 
                self.gradient += self.character
            
            print("First i = ", self.first_index)
            print("Second i = ", self.last_index)


            #It kinda works for the first gradient but when number is set to 2 or higher it doesn't work
            #Need to fix it
    def set_length(self, amount):
        newstr = ""
        for i in range(0, amount):
            newstr += self.character
        self.string = self.string.replace(self.gradient, newstr)

    def get_length(self):
        return len(self.gradient)

    def get(self):
        return self.gradient

def string_filter(name_org):
        name = copy.copy(name_org)
        unwanted_characters = ["#", "|", "*", "(", ")", "&", "^", "%", "$", "@", "!", "[", "]", "{", "}", ";", ">", "<", "?", "/", "\\", "'", "~", "-", "+", "."]
        for character in unwanted_characters:
            if(character in name):
                print("Replaced Unwanted Charcter:", character)
                name = name.replace(character, " ")
                    

        #Try to look for white spaces on the ends
        rindex = name.rfind(" ")
        lindex = name.find(" ")

        #Find where do text characters appear
        global Ralphaindex, Lalphaindex
        if(lindex != -1):
            for i in range(0, len(name)):
                if((name[i] >= "A" and name[i] <= "z") or (name[i] >= "1" and name[i] <= "9")):
                    Lalphaindex = i
                    print("Alphabet found from Left at:", Lalphaindex)
                    break
            

            for i in range(len(name)-1, 0, -1):
                print("ralpa index itr:", i)
                if((name[i] >= "A" and name[i] <= "z") or (name[i] >= "1" and name[i] <= "9")):
                    Ralphaindex = i
                    print("Alphabet found from Right at:", Ralphaindex)
                    break
                
            #Ralpa > rindex   (should be ideally)   if opposite then there's a white space between 0th index and nth text chharcter
            #Lalpha < lindex   (should be ideally)  if opposite then there's a white space between last index and nth text chharcter

            Rspace = (Ralphaindex < rindex)
            Lspace = (Lalphaindex > lindex)

            if(Rspace == True):
                print("(" + name + ") There's white space in the back, BAD FORMAT WARNING")
                name = name[0:Ralphaindex+1]
                print("After popping the right space (" + name + ")")

            if(Lspace == True):
                print("(" + name + ") There's a white space infront, BAD FORMAT WARNING")
                name = name[Lalphaindex:]
                print("After popping the left space (" + name + ")")
                print("Final content of Name (" + name + ")")

            #Now reduce the spaces in between of properly formatter address line
            #gradient = CharGradient(name, " ", 2)
            #gradient.set_length(1)
            #print("Gradient: '" +  gradient.get() + "'")
            #print(" Modified string", name)

        return name


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


    def Search2(self):
        print("INSIDE SEARCH")
        if(self.current_listing == ""): return False
        try:
            index = self.listing_path.rfind("\\")
            string = self.listing_path[index+1:len(self.listing_path)]
            string += ".json"
            dirs = os.listdir(self.listing_path[0:index])

            if(string in dirs):
                city_path = self.listing_path[0:index] + "\\" + self.current_listing + ".json"
                print("CITY PATH: ", city_path)
                try:
                    file = open(city_path)
                    value = json.load(file)
                    print("Found data")
                    return value
                except Exception as error:
                    print("Search() Not found!")
                    return False
            else:
                return False
        except Exception as error:
            print(error)
            return False

    def Search(self):
        print("INSIDE SEARCH")
        if(self.current_listing == ""): return False
        try:
            index = self.listing_path.rfind("\\")
            string = self.listing_path[index+1:len(self.listing_path)]
            string += ".json"
            #dirs = os.listdir(self.listing_path[0:index])

            city_path = self.listing_path[0:index] + "\\" + self.current_listing + ".json"
            print("CITY PATH: ", city_path)
            try:
                file = open(city_path)
                value = json.load(file)
                print("Found data")
                return value
            except Exception as error:
                print("Search() Not found!")
                try:
                    city_path = self.listing_path[0:index] + "\\" + " " + self.current_listing + ".json"
                    file = open(city_path)
                    value = json.load(file)
                    print("Found data")
                    return value
                except Exception as error:
                    return False
                return False
            else:
                return False
        except Exception as error:
            print(error)
            return False
        pass
    def PutData(self, content):
        try:
            file = open(self.listing_path, "w")
            file.write(json.dumps(content, indent=4))
            file.close()
            return True
        except Exception as error:
            print(error, " putData() library.py")
            return False
    
    def Create(self, data=None):
        #NEED TO CHECK IF THE FILE ALREADY EXISTS
        #IF IT DOES THEN DON'T CREATE IT
        try:
            #If file already exists then update it and return true or else create it
            file = open(self.listing_path+".json", "w")
            if(data != None):file.write(json.dumps(data, indent=4))
            file.close()
            return True
        except Exception as error:
            print(error)
            #If some exceptino occurs return false
            return False
        
    def Listing(self, name=None):

        if(name == None):
            self.current_listing = ""
            pass
        else:
            name = string_filter(name)
            self.current_listing = name
            pass
       
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
        unwanted_characters = ["#", "|", "*", "(", ")", "&", "^", "%", "$", "@", "!", "[", "]", "{", "}", ";", ">", "<", "?", "/", "\\", "'", "~", "-", "+", "."]
        
        for character in unwanted_characters:
            if(character in self.current_city):
                self.current_city.replace(character, "")
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
            self.current_city = string_filter(city)
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
        unwanted_characters = ["#", "|", "*", "(", ")", "&", "^", "%", "$", "@", "!", "[", "]", "{", "}", ";", ">", "<", "?", "/", "\\", "'", "~", "-", "+", "."]
        for character in unwanted_characters:
            if(character in self.current_state):
                self.current_state.replace(character, "")
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
            self.current_state = string_filter(name)
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




#storage = ImagingLibraryManager()
#val = storage.directory().State("California").City("El Cajon").Listing(" Vista Valley Rim Pl").Search()
#print(val)
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