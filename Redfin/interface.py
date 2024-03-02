from .redfin_bot import RedfinBot


class RedfinInterface():

    BOT  = None
    TYPE = 'specific'

    def create_bot():
        RedfinInterface.BOT = RedfinBot()

    def close_bot():
        RedfinInterface.BOT.close()

    def activate():
        RedfinInterface.BOT.activate()

    def search_images(value):
        #RedfinInterface.BOT.activate()
        type = RedfinInterface.TYPE
        response = RedfinInterface.BOT.location(RedfinInterface.TYPE).address(value, type).get_response()
        #RedfinInterface.BOT.close()
        return response
    
    def type(value):
        RedfinInterface.TYPE = value

    def apply_filters(filters):
        RedfinInterface.BOT.save_filters(filters)

"""
    Note:
        - For rent
        - For sale
        - town_house
        - condo
        - land
        - multi_family
        - mobile
        - co_op
        - other
        - price=(1,3)
    """
