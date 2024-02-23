from .redfin_bot import RedfinBot


class RedfinInterface():

    BOT = None
    TYPE = 'specific'
    def search_images(value):
        RedfinInterface.BOT = RedfinBot()
        RedfinInterface.BOT.activate()
        response = RedfinInterface.BOT.location(RedfinInterface.TYPE).address(value).get_response()
        RedfinInterface.BOT.close()
        return response
    
    def type(value):
        RedfinInterface.TYPE = value

        


