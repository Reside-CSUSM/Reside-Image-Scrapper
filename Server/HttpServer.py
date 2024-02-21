from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import requests
import copy
import json
from Redfin.launch import *


"""
Routes:
    - /library
         -/by general area:
         -/by specific area
    
    - /bot
         -/launch
            -/by specific address
            -/by general area
         
         -/cache
            -/by specific area
            -/by general area    

         -/others   
"""

EMPTY_URL = 'RoutingTable: set URL is empty'
ERROR_CODES = [EMPTY_URL]


class RoutingTable():
    def __init__(self):
        self.url = None
        self.table = {}

    def create_binding(self, url_pattern, handler):
        if((url_pattern in self.table.keys()) == True):
            self.table[url_pattern].append(handler)
        
        elif((url_pattern in self.table.keys()) == False):
            self.table[url_pattern] = []
            self.table[url_pattern].append(handler)
        return self
    
    def set_url(self, url):
        self.url = url
        return self

    def execute(self, url_pattern):
        unbound_patterns = "None"
        try:
            for each_handler in self.table[url_pattern]:
                each_handler()
        except Exception as error:
            unbound_patterns = url_pattern

        print("\x1b[31mUNBOUND:\x1b[0m", unbound_patterns)
        return self

    def process_url(self):
        if(self.url == None): return EMPTY_URL
        slash = "/"
        url_patterns = []

        url_patterns = copy.copy(self.url).split("/")
        url_patterns.pop(0)

        for i in range(0, len(url_patterns)):
            url_patterns[i] = "/" + url_patterns[i]
            self.execute(url_patterns[i])
        
        print("\x1b[31mREQUEST URL PATH\x1b[0m",  url_patterns, "\n\n\n")
        return self

    def print_bindings(self):
        for key, val in self.table.items():
            print("Binding: ", key, val)
        return self


class BotHandler():
    pass


class LibraryHandler():
    pass


class RequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):

        self.router = RoutingTable()
        self.router.create_binding("/", self.root)
        self.router.create_binding("/library", self.library)
        self.router.create_binding("/bot", self.bot)
        self.response_body = "None"

        super().__init__(*args, **kwargs)
        
    def library(self):        
        #Open up the library

        #Fetch the data

        #Send the data back
        pass

    def bot(self):
        
        #Open server.json to import bots
        server_file = open("server.json", "r")
        file_dict = json.load(server_file)        
        
        #Get the launch file path
        bot_path = file_dict["available_bots"]["redfin"]["interface_file"]


        #Pass in the appropriate params to bot

        #Launch the Bot
        pass
    
    def root(self):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "json")
        self.end_headers()

        response = self.router.process_url()

        if(response in ERROR_CODES):
            self.send_response(500)
            self.wfile.write(bytes("<h1>ERROR: " + response + "</h1>", "utf-8"))

        self.send_response(201)
        self.wfile.write(bytes("{MESSAGE:"+self.response_body+"}", "utf-8"))

    def do_POST(self):
        pass

    def do_PUT(self):
        pass

    def do_DELETE(self):
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


server = HttpServer('localhost', 9999)
server.run()