import copy



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
    
    def create_binding_2(self, url_pattern, handler, args=None):
        if((url_pattern in self.table.keys()) == True):
            self.table[url_pattern].append((handler, args))
        
        elif((url_pattern in self.table.keys()) == False):
            self.table[url_pattern] = []
            self.table[url_pattern].append((handler, args))
        return self
    
    def execute_2(self, url_pattern):
        unbound_patterns = "None"
        Error = None
        try:
            for each_handler in self.table[url_pattern]:
                url = copy.copy(self.url)
                url.find("")
                each_handler[0](each_handler[1])
        except Exception as error:
            unbound_patterns = url_pattern
            Error = error

        print("\x1b[31mUNBOUND:\x1b[0m", unbound_patterns, Error)
        return self
    
    def set_url(self, url):
        self.url = url
        return self

    def get_url(self):
        return self.url
    
    def execute(self, url_pattern):
        unbound_patterns = "None"
        Error = None
        flag = True

        if(flag == True):
            try:
                for each_handler in self.table[url_pattern]:
                    each_handler()
            except Exception as error:
                unbound_patterns = url_pattern
                Error = error
        else:
            for each_handler in self.table[url_pattern]:
                    each_handler()
        #print("\x1b[31mUNBOUND:\x1b[0m", unbound_patterns, Error)
        print("\x1b[31mUNBOUND:\x1b[0m")
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