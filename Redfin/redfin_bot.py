from Utility.bot import Bot
from selenium import webdriver
from Utility.utility import _ID, Flag
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys

"""
Tasks based:
    - Search and load location
    - Managing Filters
    - Finding Images and Text data
    
"""

"""
Part based:
    - Search Component
    - Filter component
    - Image Component
    - Text Component
"""


"""
Tasks based:
    - Search and load location
    - Managing Filters
    - Finding Images and Text data
    
"""

"""
Part based:
    - Search Component
    - Filter component
    - Image Component
    - Text Component
"""


INIT_URL = 'https://www.redfin.com/'
WEB_DRIVER = None
LOGIN_ERROR_CODE = 'scrapper login error'
SEARCHING_ERROR_CODE = 'scrapper address error'
DATA_FETCHING_ERROR_CODE = 'scrapper image fetching error'


#In future, elements references can be chained kind of like action chains
class ElementReference():

    def __init__(self, tag, value):
        self.tag = tag
        self.tag_value = value
    
    def set_reference(self, tag, value):
        self.tag=tag
        self.tag_value = value

    def find_self(self):
        pass

    def define_action(self):
        pass

    def get_reference(self, name):
        if(name == 'By'):
            return self.tag
        
        elif(name == 'value'):
            return self.tag_value
        
        return False
    
    def by(self):
        return self.tag
    
    def value(self):
        return self.tag_value

#---------------------------------------- DATA COLLECTION MODULES---------------------------------------------
class Listing():

    def __init__(self):
        self.address = None
        self.image_urls = []
        self.price = None
        self.property_stats = None
    
    def get_images(self):
        return self.image_urls

    def get_price(self):
        return self.price
    
    def get_stats(self):
        return self.property_stats
    
    def get_address(self):
        return self.address
    
    def export(self):
        pass


class FetchListings():

    def __init__(self):
        self.house_listings = []
        pass

    def fetch(self):

        pass

#-----------------------------------------FILTER MODULES---------------------------------------------------
class HouseType():

    def __init__(self):
        self.main_button = ElementReference(By.XPATH, '/html/body/div[1]/div[8]/div[2]/div[1]/div[2]/div/div/div/div[1]/form/div[1]/div')
        self.for_rent = ElementReference(By.ID, 'forRent')
        self.for_sale = ElementReference(By.ID, 'for-sale')
        self.done_button = ElementReference(By.XPATH, '/html/body/div[1]/div[8]/div[2]/div[1]/div[2]/div/div/div/div[1]/form/div[1]/div/div[2]/div/div[2]/button')

    def get_main(self):
        return self.main_button

    def get_sub_filter(self, choice):
        if(choice == 'for sale'):
            return self.for_sale
        elif(choice == 'for rent'):
            return self.for_rent
        

class PriceRange():
    def __init__(self):
        pass


class HomeTyoe():
    pass


#--------------------------------------------ADDRESS SEARCH MODULES------------------------------------------------
class RedfinSearch():

    def __init__(self, bot):
        self.bot = bot
        self._id = _ID('redfin search', 2000)
        self.status = Flag()
        self.location_address = None
        self.search_element = ElementReference(By.CLASS_NAME, 'search-input-box')
        self.property_type = HouseType()
        self.filter = None

    def __task(self):
        #Search for the address and click okay

        try:
            element = self.bot.wait(1).search_element(self.search_element.get_reference('By'), self.search_element.get_reference('value')).get_element()
            element.send_keys(self.location_address)
            element.send_keys(Keys.ENTER)
            self.bot.wait(4)
            
            #"""
            if(self.filter != None):
                #Apply the filters
                #Click on house filter
                path = '/html/body/div[1]/div[8]/div[2]/div[1]/div[2]/div/div/div/div[1]/form/div[1]/div'
                main = self.property_type.get_main()
                self.bot.search_element(main.get_reference('By'), main.get_reference('value')).get_element().click()

                if(self.filter == 'for rent'):
                    #Select the rent option
                    button = self.property_type.get_sub_filter('for rent')
                    self.bot.wait(0.5).search_element(button.get_reference('By'), button.get_reference('value')).get_element().click()
                
                elif(self.filter == 'for sale'):
                    #Select the rent option
                    button = self.property_type.get_sub_filter('for sale')
                    self.bot.wait(0.5).search_element(button.get_reference('By'), button.get_reference('value')).get_element().click()

                #Click on done
                path = '/html/body/div[1]/div[8]/div[2]/div[1]/div[2]/div/div/div/div[1]/form/div[1]/div/div[2]/div/div[2]/button'
                self.bot.search_element(By.XPATH, path).get_element().click()
                self.bot.wait(3)
                #"""
        except Exception as error:
            return SEARCHING_ERROR_CODE
    

    def __exception_guard(self):
        try:
            self.__task()
        except Exception as error:
            return error
        
    def set_location_address(self, address):
        if(isinstance(address, str)):
            self.location_address = address
    
    def apply_filter(self, filter):
        self.filter = filter

    def perform(self):
        return self.__task()

    def id(self):
        return self._id


class Tasks():

    def __init__(self):
        self.task_list = []

    def get(self, index):
        try:
            return self.task_list[index]
        except Exception as error:
            return False


    def search(self, id):
        for task in self.task_list:
            if(task.id().get('name') == id):
                return task       
        return False


    def add(self, task):
        self.task_list.append(task)
    
    def pop(self, index):
        self.task_list.pop(index)
    
    def get_total_tasks(self):
        return len(self.task_list)
        
    def run(self, tag):
        if(tag == 'all'):
            for task in self.task_list:
                task.perform()
            return 
        
        elif(isinstance(tag, int) == True):
            try:
                self.task_list[tag].perform()
                return True
            except Exception as error:
                return False


class GeneralLocation():

    def __init__(self, bot):
        self.bot = bot
        self.location_address = None
        self.search_element = ElementReference(By.CLASS_NAME, 'search-input-box')

    def address(self, address):
        self.location_address = address

    def fetch_listing_data(self):
        #Putting address in search bar
        element = self.bot.search_element(self.search_element.by(), self.search_element.value()).get_element()
        element.send_keys(self.location_address)
        element.send_keys(Keys.ENTER)
        self.bot.wait(1)

        
        pass

    def apply_filters(self):
        pass


class SpecificLocation():

    def __init__(self, bot):
        self.bot = bot
        self.location_address = None
        self.image_urls = []
        self.price = None
        self.amenities = []
        self.response = None
    
    def address(self, address):
        self.location_address = address
    
    def fetch_listing_data(self):
        try:
            #GETTING IMAGE URLS
            
            try:
                image_button = '/html/body/div[1]/div[11]/div[1]/div[3]/div/div[5]/div/button'
                image_button = '/html/body/div[1]/div[11]/div[1]/div[2]/div/div[5]/div/button'
                self.bot.search_element(By.XPATH, image_button).get_element().click()

                image_class1 = 'inline-block selected'
                image_class2 = 'inline-block'
                
                #self.bot.explicit_wait(1)
                element_list1 = self.bot.wait(0.5).search_elements(By.CLASS_NAME, image_class1).get_element()
                element_list2 = self.bot.wait(0.5).search_elements(By.CLASS_NAME, image_class2).get_element()
                #https://ssl.cdn-redfin.com/photo

                for element in element_list1:
                    self.image_urls.append(element.get_attribute('src'))
                
                for element in element_list2:
                    self.image_urls.append(element.get_attribute('src'))

                for i in range(len(self.image_urls) - 1, -1, -1):
                    if self.image_urls[i] is None or self.image_urls[i] == 'None':
                        self.image_urls.pop(i)

            except Exception as error:
                     print("SOME IMAGES WERE NOT FOUND", error)
                     return DATA_FETCHING_ERROR_CODE

            try:
                close_button = '//*[@id="bp-dialog-container"]/div[1]/button'
                self.bot.search_element(By.XPATH, close_button).get_element().click()
            except Exception as error:
                print("CLOSE BUTTON NOT FOUND")
            
            
            #GET PRICE
            self.price = self.bot.search_element(By.CLASS_NAME, 'statsValue').get_element()
            self.price = self.price.text

            #GET AMENITIES
            var = '/html/body/div[1]/div[11]/div[2]/div[6]/section/div/div[2]/div/div[1]/div[2]/div[1]/div/ul/li[1]'
            end = ']'
            
            self.amenities.append(self.bot.wait(0.5).search_element(By.XPATH, var).get_element().text)

        except Exception as error:
            self.response = {
            'image_urls':self.image_urls, 
            'price':self.price, 
            'amenities':self.amenities
            }
            return self.response


        self.response = {
            'image_urls':self.image_urls, 
            'price':self.price, 
            'amenities':self.amenities
        }

        return self.response



#-----------------------------------------------------INTERFACE MODULES-------------------------------------------------------
#Interface that other services will interact with


class RedfinBot():

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'
        self.driver = webdriver.Chrome(options=options)
        self.bot = Bot(INIT_URL, self.driver)
        self.tasks = Tasks()
        self.redfin_search = RedfinSearch(self.bot)
        self.specific_fetcher = SpecificLocation(self.bot)
        self.general_fetcher = GeneralLocation(self.bot)
        self._address = None
        self.listing_response = None
        self.listing_type = 'specific'
        self.bot.activate()

    def login_to_website(self, credentials):
        try:
            try:
                val = '/html/body/div[1]/div[2]/div/div/header[2]/div[2]/div[7]/button'
                el = self.bot.wait(1).search_element(By.XPATH, val).get_element()
                el.click()
                self.bot.wait(1)
            except Exception as error:
                val = '/html/body/div[1]/div[2]/div/div/header[2]/div[2]/div[7]/button'
                el = self.bot.wait(1).search_element(By.XPATH, val).get_element()
                el.click()
                self.bot.wait(1)
                pass
           
            val = '/html/body/div[5]/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/div/form/div/div[1]/div/span/span/div/input'
            el = self.bot.search_element(By.XPATH, val).get_element()
            el.send_keys(credentials[0])
            el.send_keys(Keys.ENTER)
            self.bot.wait(0.3)
 
            vars = '/html/body/div[5]/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/div/div[3]/button'
            el = self.bot.search_element(By.XPATH, vars).get_element()
            el.click()

            var1 = '/html/body/div[5]/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/div/form/div/div[2]/span/span/div/input'
            el = self.bot.search_element(By.XPATH, var1).get_element()
            el.send_keys(credentials[1])
            el.send_keys(Keys.ENTER)

        except Exception as error:
            print("Error= ", error)
            return LOGIN_ERROR_CODE

    def get_images_on_address(self, address, filter=None):
        #LOGIN
        value = self.login_to_website(credentials=('yashaswi.kul@gmail.com', 'yashema@E494murlipura2'))
        #SEARCHING
        self.redfin_search.set_location_address(address)
        if(filter != None): self.redfin_search.apply_filter(filter)
        self.redfin_search.perform()


    def get_response(self):
        #LOGIN
        value = self.login_to_website(credentials=('yashaswi.kul@gmail.com', 'yashema@E494murlipura2'))
        if(value == LOGIN_ERROR_CODE): return LOGIN_ERROR_CODE
        
        #SEARCHING
        self.redfin_search.set_location_address(self._address)
        value = self.redfin_search.perform()
        if(value == SEARCHING_ERROR_CODE): return SEARCHING_ERROR_CODE

        #FETCHING
        if(self.listing_type == 'general'):
            self.listing_response = self.general_fetcher.fetch_listing_data()
            if(self.listing_response == DATA_FETCHING_ERROR_CODE): return DATA_FETCHING_ERROR_CODE
        
        elif(self.listing_type == 'specific'):
            self.listing_response = self.specific_fetcher.fetch_listing_data()
            if(self.listing_response == DATA_FETCHING_ERROR_CODE): return DATA_FETCHING_ERROR_CODE

        return self.listing_response

    def address(self, address):
        self._address = address
        return self
    
    def location(self, type):
        self.listing_type = type
        return self
    
    def close(self):
        self.bot.close()

#bot = RedfinBot()
#bot.get_images_on_address('512 Valley St, San Marcos, TX', 'for sale')


#NOTE:
"""
TODO:
    - Set user agent etc
    - Identify lang specific endpoints Java/python
Apply Filters:
    - Manipulate settings buttons

Specific Address
    - Parse the single page
        - Get the images
        - Get other text data
    

General Address
    - Search x amount of listing and get
        - Get all the text/image data

    - Search all amount of listing and get
        - Get all the text/image data

"""