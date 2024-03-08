import sys, os
#sys.path.insert(0, r'C:\Users\yasha\Visual Studio Code Workspaces\SystemX\ResideImageScrapper')
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
from ImageLibrary.library import *

class ListingService():

    def __init__(self):
        self.storage = ImagingLibraryManager()
        self.response = "None"
        pass
    
    def get_response(self):
        return self.response
    
    def fetch(self, address):
        #Use good techniques to extract the State, City, and Listing values. 
        #Address must be formatted as "Street, City, State" For example "5500 Grand Lake Dr, San Antonio, TX 78244"
        global state_abbreviation, state
        state = ""
        first_list = address.split(",")
        second_list = address.split(", ")
        list = first_list
        address_line = ""
        city = ""

        if(len(first_list) >= 3):
            address_line = first_list[0]
            city = string_filter(first_list[-2])
            state_abbreviation = string_filter(first_list[-1])
            list = first_list

        elif(len(second_list) >= 3):
            address_line = second_list[0]
            city = string_filter(second_list[-2])
            state_abbreviation =  string_filter(copy.copy(second_list[-1]))
            list = second_list

        else:
            print("ERROR: State, City or Address component missing")
            return None


        if(len(list[2]) < 2):
            print("Invalid State Abbreviation Extracted: ", state_abbreviation)
            return None
        
        elif(len(list[2]) > 2):
            state_abbreviation  = state_abbreviation.replace(" ", "")

        try:
            state = STATE_ABBREVIATION[state_abbreviation]
            print("State Abbr   = ", state_abbreviation, "     len = " + str(len(state_abbreviation)))
            print("State        = ", state, "     len = " + str(len(state)))
            print("City         = ", city, "     len = " + str(len(city)))
            print("Address      = ", address_line, "     len = " + str(len(address_line)))
        except Exception as error:
            print("THERE'S NO SUCH STATE", state_abbreviation)


        else:
            val = self.storage.directory().State(state).City(city).Listing(address_line).Search()
            #print(val, " ListingService inside action path")
            if(val == False):
                return None
            else:
                self.response = {
                    'ListingIdentifier':address,
                    'MatchedWith':val['Address'],
                    'Images':val['Images']
                }
                #self.response = val["Images"]
                return self.response
            

        def fetch2(self, address):
            #Use good techniques to extract the State, City, and Listing values. 
            #Address must be formatted as "Street, City, State" For example "5500 Grand Lake Dr, San Antonio, TX 78244"
            global state_abbreviation, state
            state = ""
            first_list = address.split(", ")
            second_list = address.split(",")
            list = first_list
            address_line = ""
            city = ""

            if(len(first_list) >= 3):
                address_line = first_list[0]
                city = first_list[1]
                state_abbreviation = first_list[2]
                list = first_list

            elif(len(second_list) >= 3):
                address_line = second_list[0]
                city = second_list[1]
                state_abbreviation = copy.copy(second_list[2])
                list = second_list

            else:
                print("ERROR: State, City or Address component missing")
                return False


            if(len(list[2]) < 2):
                print("Invalid State Abbreviation Extracted: ", state_abbreviation)
                return False
            
            elif(len(list[2]) > 2):
                state_abbreviation  = state_abbreviation.replace(" ", "")

            try:
                state = STATE_ABBREVIATION[state_abbreviation]
                print("State Abbr   = ", state_abbreviation, "     len = " + str(len(state_abbreviation)))
                print("State        = ", state, "     len = " + str(len(state)))
                print("City         = ", city, "     len = " + str(len(city)))
                print("Address      = ", address_line, "     len = " + str(len(address_line)))
            except Exception as error:
                print("THERE'S NO SUCH STATE", state_abbreviation)

            else:
                val = self.storage.directory().State(state).City(city).Listing(address_line).Search()
                if(val == False):
                    return None
                else:
                    self.response = val["Images"]
                    return self.response


    

