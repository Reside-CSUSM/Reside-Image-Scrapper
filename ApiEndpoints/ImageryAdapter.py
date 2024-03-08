import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from ResideImagery import *
class ResideImageryAdapter(ResideImageryAPI):
    
    def __init__(self):
        ResideImageryAPI.__init__(self)
    
    def initialize(self, IP, PORT):
        IP = IP
        PORT = PORT
        self.set_host(IP, PORT)

    def add_areas(self, area):
        self.area().add_area(area)

    def delete_area(self, area):
        self.area().delete_area(area)

    def print_areas(self):
        self.area().print_area('all')

    def search_area(self):
        self.area().send_calls()

    def add_general_search_filter(self, filter):
        self.area().add_filters(filter)

    def remove_general_search_filter(self, filter):
        self.area().remove_filter(filter)
