from flask import Flask, redirect, url_for, render_template, request, Response
from AutomationService import *
from ListingsService import *


app = Flask(__name__)


class ServerResponse():

    def __init__(self):
        
        self.payload = {
            'RecipientPayload':None,
            'Errors':False,
            'ErrorLog':[]
        }
    
    def put_payload(self, payload):
        self.payload['RecipientPayload'] = payload
    
    def get(self, field=None):
        if(field == None):
            return self.payload
        else:
            try:
                return self.payload[field]
            except Exception as error:
                return None
    
    def set_error(self, val):
        if(isinstance(val, bool) == False):
            raise "\x1b[31m ServerResponse: Error Flag Not Boolean!!\x1b[0m"
        self.payload['Errors'] = val
    
    def put_error_log(self, log):
        self.payload['ErrorLog'].append(log)


class FlaskServer():

    automation_service = AutomationService()
    listing_images_service = ListingService()
    _IP = "localhost"
    _PORT = 5000

    @app.route("/<value>")
    def root(value):
        return "Root"

    @app.route("/automations/query=<value>", methods=["POST","GET"])
    def SecondaryAutomationEndpoint(value):
        #Implement it using request body
        FlaskServer.automation_service.handle("/query="+value, 'POST')
        response = FlaskServer.automation_service.get_response()
        print("Automation route works")
        if(isinstance(response, str) == False):
            return str(response)    
        return response
    
    @app.route("/Automations", methods=["POST", "GET"])
    def PrimaryAutomationEndpoint():
        if(request.is_json == False):
            return "Data wasn't json"
        #RIGHT THERE IMPLEMENT ERROR PROPAGATION USING ERROR() OBJECTS
        response = FlaskServer.automation_service.handle2(request.get_json(), 'POST').get_response()
        #print("response==",response)
       
        return str(response)
        #return d


    @app.route("/ResideLibrary/Images", methods=["POST", "GET"])
    def ListingImagesEndpoint():
        #Implement it using request body
        responses = []
        response = ServerResponse()

        print("inside route")
        if(request.is_json == True):
            try:
                array = request.get_json()["Listings"]
                if(len(array) == 0):
                    response.set_error(True)
                    response.put_error_log('No Images when listings are not given')
                    return response.get()
                    #return "No Images when listings are not given"
            
            except KeyError as error:
                response.set_error(True)
                response.put_error_log("'Listing' key is  missing in json data")
                print("'Listing' key is  missing in json data")
                return response.get()
                #return "'Listing' key not found in recieved array"
            
            print(len(array), " length")
            for element in array:
                print("element array")
                responses.append(FlaskServer.listing_images_service.fetch(element))
            response.set_error(False)
            response.put_payload(responses)
    
            return response.get()
            #return str(responses)
        
        else:
                response.set_error(True)
                response.put_error_log('Data is not json')
                return response.get()
                #return "Data is not json"    
    
    @app.route("/endpoint", methods=["POST", "GET", "PUT"])
    def endpoint():
        try:
            object = "None"
            if(request.is_json == True):
                object = request.get_json()
            else:
                object = request.get_data()
            print(str(object))
        except Exception as error:
            print(error)
        return "this is endpoint"

    def host_with(self, IP, PORT):
        FlaskServer._IP = IP
        FlaskServer._PORT = PORT

    def run(self):
        IP = FlaskServer._IP
        PORT = FlaskServer._PORT
        app.run(IP, port=PORT, debug=False)



#Need to fix error checking from API
#Use good address parsing and searching techniques  almost done
#Use good searching techniques for fetching images  almost done

#Organize automation file
#Organize listing service file

#Solution for asynchronously launching services
#Maybe creating session objects for automation actions

#Then maybe creating plug and play based automation folder uploads. 
#Fix specific search feature


#TASKS NOW:
#1) Finish the /library    
#2) Finish and test error codes
#3) Fix the parsing problem


#Need to fix, source and destinatino file names area same DONE QUICK FIXED
#Need to fix the parsing problem in ListinService DONE GOOD FIXED 
#Need to make we collect all the cities required  


#Need to test /Library route    DONE EXCEPT real api calls
#Need to test /Automations      Done
#Jsonify response and maybe add listing identifiers Done
#FIXING Uneccesary nones from an array when doing specific search Don't care