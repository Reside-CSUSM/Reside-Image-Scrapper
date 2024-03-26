
class City():

    def __init__(self):
        self.attributes = {
            'last_updated':None,
            'created':None
        }
        pass

    def last_updated(self):
        pass
    
    def created(self):
        pass

    def save(self):
        pass


class State():

    def __init__(self):

        self.attributes = {
            'name':"Default State",
            'last_updated':None,
            'created':None,
            'cities':None
        }

    def last_updated(self):
        pass

    def created(self):
        pass
    
    def save(self):
        pass


class LogSaver():

    def __init__(self):
        pass

    def update_file(self):
        pass




class UpdateLog():

    def __init__(self):
        pass


class Log():

    def __init__(self):
        self.state = ""
        self.city = ""
        self._data = ""
        self.time  = ""
        self.about = ""




