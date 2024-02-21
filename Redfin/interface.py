from .redfin_bot import RedfinBot


class RedfinInterface():

    BOT = None
    def search_images(value):
        RedfinInterface.BOT = RedfinBot()
        response = RedfinInterface.BOT.location('specific').address(value).get_response()
        RedfinInterface.BOT.close()
        return response


