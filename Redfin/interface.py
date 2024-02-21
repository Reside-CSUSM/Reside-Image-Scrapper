from redfin_bot import RedfinBot


class RedfinInterface():

    BOT = RedfinBot()

    def search_images(value):
        response = RedfinInterface.BOT.location('specific').address(value)
        return response


