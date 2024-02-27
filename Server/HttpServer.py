import sys
sys.path.insert(0, r'C:\Visual Studio Code Workspaces\SystemX\ResideImageScrapper')
from http.server import HTTPServer, BaseHTTPRequestHandler
import copy
from Redfin.interface import *
from Router import *
from AutomationService import *
from ListingsService import *


class RequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.router = RoutingTable()
        self.router.create_binding("/", self.root)
        self.router.create_binding("/library", self.library)
        self.router.create_binding("/automations", self.automation_controller)
        self.response_body = "None"
        self.current_request_type = 'None'

        self.automation_handler = AutomationService()
        self.library_handler = ListingService()

        super().__init__(*args, **kwargs)

    def root(self):
        value = {
            'response:':"<h3>Root Endpoint Not available</h3>"
        }
        self.send_response(200)
        self.send_header("Cotent-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(value['response:'], "utf-8"))

    def library(self):    
        value = "<h3>Library Service Not available</h3>"

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(value), "utf-8")    

    
    def automation_controller(self):
        url = copy.copy(self.router.get_url()).replace("/automations", "")
        self.automation_handler.handle(url, copy.copy(self.current_request_type))
        response = self.automation_handler.get_response()
        self.wfile.write(bytes("The POST request for automation service has been fullfilled", "utf-8"))

        print("\x1b[35mFINAL RESPONSE:\x1b[0m", response)

    def bot_controller1(self):
        url = self.router.get_url()
        index = url.find("/address")
        string = ""

        for i in range(index+1, len(url)):
            if(url[i] == "/"):
                break
            string += url[i]


        string = string.replace("%20", " ")
        string = string.replace("address=", "")
        print("After Filtering:", string)

        RedfinInterface.type('general')
        RedfinInterface.apply_filters(['For rent'])
        #RedfinInterface.type('specific')
        response = RedfinInterface.search_images(string)
        self.response_body = str(response)
    

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "json")
        self.end_headers()

        print("do_GET:", self.path)
        response = self.router.set_url(copy.copy(self.path)).process_url()

        if(response in ERROR_CODES):
            self.send_response(500)
            self.wfile.write(bytes("<h1>ERROR: " + response + "</h1>", "utf-8"))

        self.send_response(201)
        self.wfile.write(bytes("{MESSAGE:"+self.response_body+"}", "utf-8"))


    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.current_request_type = 'POST'
        print("PATH do_POST():", self.path)
        response = self.router.set_url(copy.copy(self.path)).process_url()
    
    def do_PUT(self):
        #UPDAT
        pass

    def do_DELETE(self):
        #DELETING SPECIFIC LISTINGS OR DELETING ENTIRE CITIES
        pass

class HttpServer():

    def __init__(self, IP, PORT):
        self.ip = IP
        self.port = PORT
        self.server = HTTPServer((IP, PORT), RequestHandler)
    
    def run(self):
        print("Server:  http://"+self.ip + ":" + str(self.port), "started.....")
        self.server.serve_forever()
    
    def hosted_on(self):
        return (self.ip, self.port)

    def close(self):
        self.server.server_close()


#server = HttpServer('localhost', 9999)
server = HttpServer('172.25.177.82', 9999)
server.run()