from flask import Flask
from AutomationService import *
from ListingsService import *

app = Flask(__name__)

class FlaskServer():

    automation_service = AutomationService()
    listing_images_service = ListingService()
    
    @app.route("/<value>")
    def root(value):
        return "Root"

    @app.route("/automations/<value>")
    def AutomationEndpoint(value):
        FlaskServer.automation_service.handle(value, 'POST')
        response = FlaskServer.automation_service.get_response()
        print("Automation route works")
        return response
    
    @app.route("/ListingImages/<value>")
    def ListingImagesEndpoint(value):
        FlaskServer.listing_images_service.handle()
    
        print("Listing Image route works")
        return "Yes"
    
    
    def run(self):
        app.run()


server = FlaskServer()
server.run()
