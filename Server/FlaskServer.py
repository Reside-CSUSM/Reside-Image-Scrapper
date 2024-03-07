from flask import Flask, redirect, url_for, render_template, request
from AutomationService import *
from ListingsService import *

app = Flask(__name__)

class FlaskServer():

    automation_service = AutomationService()
    listing_images_service = ListingService()
    
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
        response = FlaskServer.automation_service.handle2(request.get_json(), 'POST')
        return str(response)


    @app.route("/ResideLibrary/Images", methods=["POST", "GET"])
    def ListingImagesEndpoint():
        #Implement it using request body
        responses = []
        print("inside route")
        if(request.is_json == True):
            try:
                array = request.get_json()["Listings"]
                if(len(array) == 0):
                    return "No Images when listings are not given"
            except KeyError as error:
                print("'Listing' key is  missing in json data")
                return "'Listing' key not found in recieved array"
            
            print(len(array), " length")
            for element in array:
                print("element array")
                responses.append(FlaskServer.listing_images_service.fetch(element))
            return str(responses)
        
        else:
                return "Data is not json"    
    
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

    def run(self):
        app.run(debug=False)

server = FlaskServer()
server.run()




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


#Need to fix, source and destinatino file names area same
#Need to fix the parsing problem in ListinService,oy  half way there tbh
#Need to make we collect all the cities required


#Need to test /Library route
#Need to test /Automations
#Implement error codes finally