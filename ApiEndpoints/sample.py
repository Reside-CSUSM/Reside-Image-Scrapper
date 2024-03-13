
import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
#from imagery import *
from ImageryAdapter import ResideImageryAdapter
image_api = ResideImageryAdapter()
#image_api = ImagingAPI()
image_api.initialize('38.56.138.77', 8888)
#image_api.add_areas("Otay Mesa, CA").add_areas("Poway, CA").add_areas("San Diego, CA").add_areas("La Mesa, CA").search_area()
#image_api.add_housings("13604 Caldwell Dr #36, Austin, TX").search_housings()

image_api.add_general_search_filter('For rent')
image_api.add_general_search_filter('For rent')

def search_area(area, webfilters):
    filters = webfilters
    for filter in filters:
        image_api.add_general_search_filter(filter)
    print("\n\nArea =", area, " Filters =", filters, "\x1b[32m processing....\x1b[0m")
    image_api.add_areas(area).search_area()
    print("\x1b[33mAdded area:\x1b[0m", area, "filters =", filters)



class AreaUpdate(ResideImageryAdapter):

    def __init__(self, city, state):
        self._city = city
        self._state = state
        self.filter1 = 'For rent'
        self.filter2 = 'For sale'

    def run(self):
        print("["+self._city+", " + self._state +"]", "\x1b[32mUPDATING.....\x1b[0m")
        self.add_general_search_filter(self.filter2)
        self.add_areas(self._city + ", " + self._state)
        try:
            val = self.search_area()
            print(val)
        except Exception as error:
            print("\x1b[31m Update 'For sale' Failed!\x1b[0m")
            #print(error)
            #print("\x1b[31mConnection closed or host in correct,  use 'set host' to set ip and port\x1b[0m")

        self.add_general_search_filter(self.filter1)
        self.add_areas(self._city + ", " + self._state)

        try:
            val = self.search_area()
            print(val)
        except Exception as error:
            print("\x1b[31m Update 'For rent' Failed!\x1b[0m")
            #print(error)
            #print("\x1b[31mConnection closed or host in correct,  use 'set host' to set ip and port\x1b[0m")
        
        print("Update Finished.....\n\n\n")

class CacheUpdates():

    def __init__(self):
        self.list = []

    def run(self):
        for list in self.list:
            list.run()
    
    def append(self, update):
        if(isinstance(update, AreaUpdate) == False):
            return False
        self.list.append(update)
    
def console():
    cache_updates = CacheUpdates()
    while(True):
        os.system('cls')
        print("Select Options: [add, set host, run search, exit, show areas, delete, update areas]")
        val = input()

        if(val == "update areas"):
            while(True):
                print("\n/update> ", end="")
                print("Enter the name of (State) ", end="")
                state = input()
                
                if(state == "exit"):break
                elif(state == "none"):continue

                print("Enter the name of (City) ", end="")
                city = input()
                if(city == "exit"):break
                elif(city == "none"):continue
                cache_updates.append(AreaUpdate(city, state))

        if(val == "start updates"):
            cache_updates.run()

        if(val == "add"):

            while(True):
                print("\n/add> ", end="")
                print("Enter the name of (City, State) ", end="")
                val = input()
                area = ""
                filter = ""
                if(val == "exit"):break
                elif(val == "none"):continue
                else: area = val

                print("['For rent', 'For sale']", end="")
                print("  Enter Filters: ", end="")
                filter = input()

                if(filter == "exit"):break
                if(filter == "none"): continue

                image_api.add_general_search_filter(filter)
                image_api.add_areas(area)
        
        elif (val == 'delete'):
            print("\n\n/delete> choose area: ", end="")
            val = input()
            image_api.delete_area(val)

        elif(val == "set host"):
            print("\n\n/set host> ", end="")
            print("Enter host server ip: ", end="")
            ip = input()

            print("\nEnter host server port: ", end="")
            port = input()
            image_api.initialize(ip, port)
            pass

        elif (val == "show areas"):
            print("\n\n/show areas> ", end="")
            image_api.print_areas()
            input()

        elif(val == "run search"):
            print("\n\n/run search> ", end="")
            print("Posted request for searching all areas.......")
            try:
                val = image_api.search_area()
                print(val)
            except Exception as error:
                print(error)
                print("\x1b[31mConnection closed or host in correct,  use 'set host' to set ip and port\x1b[0m")

            val = input()
        elif(val == "exit"):
            break

       
    print("\n\n Program exited....")



console()

#Carlsbad
#San Marcos
#Escondido
#Poway
#San Diego