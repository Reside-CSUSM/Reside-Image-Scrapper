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
    def AutomationEndpoint(value):
        FlaskServer.automation_service.handle("/query="+value, 'POST')
        response = FlaskServer.automation_service.get_response()
        print("Automation route works")
        if(isinstance(response, str) == False):
            return str(response)    
        return response
    
    @app.route("/ListingImages", methods=["POST", "GET"])
    def ListingImagesEndpoint():
        responses = []
        
        array = request.get_json()["Listing"]
        print(len(array), " length")
        for element in array:
            responses.append(FlaskServer.listing_images_service.fetch(element))
            #response = FlaskServer.listing_images_service.fetch(request.get_json()["Listing"])
       
        if(len(responses) == 0):
            return "None"
        else:
            return str(responses)
    
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