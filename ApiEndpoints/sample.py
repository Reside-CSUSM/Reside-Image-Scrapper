
import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
from imagery import *
image_api = ImagingAPI()
image_api.initialize("38.56.138.77", 8888)
image_api.add_general_search_filter("For rent")
#image_api.add_areas("Otay Mesa, CA").add_areas("Poway, CA").add_areas("San Diego, CA").add_areas("La Mesa, CA").search_area()
#image_api.add_housings("13604 Caldwell Dr #36, Austin, TX").search_housings()



def search_area(area, webfilters):
    filters = webfilters
    for filter in filters:
        image_api.add_general_search_filter(filter)
    print("\n\nArea =", area, " Filters =", filters, "\x1b[32m processing....\x1b[0m")
    image_api.add_areas(area).search_area()
    print("\x1b[33mAdded area:\x1b[0m", area, "filters =", filters)


def console():
    while(True):

        print("Select Options: [add, search]")
        val = input()

        if(val == "add"):

            while(True):
                print("/add> ", end="")
                print("Enter the name of (City, State) ", end="")
                val = input()
                area = ""
                filter = ""
                if(val == "exit"):break
                elif(val == "none"):continue
                else: area = val

                print("\n Available Filters ['For rent', 'For sale']")
                print("Enter Filters: ", end="")
                filter = input()

                if(val == "exit"):break
                if(filter == "none"): continue
                else: filter = val
                image_api.add_general_search_filter(filter)
                image_api.add_areas(area)

        elif (val == "show areas"):
            image_api.print_areas()

        elif(val == "run search"):
            print("Posted request for searching all areas.......")
            image_api.search_area()

        elif(val == "exit"):
            break

       
    print("\n\n Program exited....")



console()