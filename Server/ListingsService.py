import sys
sys.path.insert(0, r'C:\Users\yasha\Visual Studio Workspaces\SystemX\ResideImageScrapper')
from Router import RoutingTable


class ListingService():

    def __init__(self):
        self.router = RoutingTable()
        self.router.create_binding("/", self.root)
        self.router.create_binding("/search", self.search)

    def root(self):
        pass

    def search(self):
        pass

    def fetch(self, address):
        pass
    
    def handle(self, path):
        pass
