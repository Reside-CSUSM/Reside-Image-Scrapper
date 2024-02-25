import sys
sys.path.insert(0, r'C:\Users\yasha\Visual Studio Workspaces\SystemX\ResideImageScrapper')
from Utility.bot import Bot
from selenium import webdriver
from Utility.utility import _ID, Flag
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import copy
import time
import re


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

class ElementPointer():
    def __init__(self, tag, value, bot):
        self.bot = bot
        self.tag = tag
        self.tag_value = value
        self._element = None
        self.flag = Flag()

    def create_pointer(self):
        try:
            self._element = self.bot.search_element(self.tag, self.tag_value).get_element()
            self.flag.set_true()
        except Exception as error:
            self.flag.set_false()
            print("ElementPointer Error: ", error)
    
    def get_status(self):
        return self.flag.check()
    
    def set_reference(self, tag, value):
        self.tag=tag
        self.tag_value = value

        try:
            self._element = self.bot.search_element(self.tag, self.tag_value).get_element()
        except Exception as error:
            print("ElementPointer Error:", error)
            self._element = None


    def element(self):
        return self._element
    
    def by(self):
        return self.tag
    
    def value(self):
        return self.tag_value

#---------------------------------------- DATA COLLECTION MODULES---------------------------------------------


class Listing():

    def __init__(self, bot, el_ptr):
        self.bot = bot
        self.element_ptr = el_ptr
        self.price = "No price"
        self.address = "No address"
        self.stats = "No stats"
        self.image_urls = []
        self.processed_flag = Flag()
        self.processed_flag.set_true()
        self.print_flag = Flag()
        self.print_flag.set_true()
        self.detail_flag = Flag()
        self.detail_flag.set_true()

    def print_meta_data(self, value):
        if(value == 'off'):
            self.print_flag.set_false()
        elif(value == 'on'):
            self.print_flag.set_true()
    
    def print_details(self, value):
        if(value == 'off'):
            self.print_flag.set_false()
        elif(value == 'on'):
            self.print_flag.set_true()
            
    def process(self):
        #IMAGES
        has_images = Flag()
        has_images.set_true()

        has_address = Flag()
        has_address.set_true()

        has_stats = Flag()
        has_stats.set_true()
        images = ""
        try:
            image_class_name = 'bp-Carousel__cell'
            images = self.element_ptr.find_elements(By.CLASS_NAME, image_class_name)
        except Exception as error:
            print("Processing() Error: ")
            if((len(images) > 5) == False):
                self.processed_flag.set_false()
            return False

        if(self.print_flag.check()):
            print("\n\n\x1b[32mLISTING INFO:\x1b[0m")
            print("Getting images....")

        global image_url
        for image in images:
            try:
                image_url = image.find_element(By.CLASS_NAME, 'bp-Homecard__Photo--image').get_attribute('src')
                if("https" in image_url):
                    self.image_urls.append(image_url)
                    if(self.print_flag.check()):
                        print("\x1b[34mSuccessful IMAGE URL:\x1b[0m", image_url)
            except Exception as error:
                if(self.print_flag.check()):print("\x1b[31mUnsuccessful IMAGE URL:\x1b[0m", image_url)
                #print(error)
    
        try: 
            address_el = self.element_ptr.find_element(By.CLASS_NAME, 'bp-Homecard__Content')
            string = copy.copy(address_el.text)
            string = string.split("\n")
            #self.address = string[-1]
            self.stats = []

            for str in string:
                str.replace("\n", "")
                self.stats.append(str)

            self.price = self.stats[0]
            regex = r"^(.*?),\s*(.*?),\s*(.*?)\s+(\d{5})$"
            for item in self.stats:
                matches = re.match(regex, item)
                if(matches != None):
                    self.address = ""
                    for i in range(1, matches.re.groups+1):
                        if(i == matches.re.groups):
                            self.address += matches.group(i)
                        else:
                            self.address += matches.group(i)+", "
                    break
            
            if(self.detail_flag.check()):
                print("ADDRESS:", self.address)
                print("STATS:", self.stats)
                print("PRICE:", self.price)
            #print("innerHTML:", address_el.text)

        except Exception as error:
            has_address.set_false()
            if(self.detail_flag.check()):
                print("Couldn't find address element")


        #return false when either the li element that contains all the images is not found
        #or return false when the addres is not found. Rn nothing is setup to detech image
        if(has_address.check() == False):
            self.processed_flag.set_false()
        
        return self.processed_flag.check()

    def get_status(self):
        return self.processed_flag.check()
    
    def get_images(self):
        return self.image_urls

    def export(self, type='json'):
        payload = None
        if(type == 'json'):
            payload = {
                'address':self.address,
                'price':self.price,
                'stats':self.stats,
                'images':[]
            }
            payload['images'] = self.image_urls
            return payload

        else:
            return payload
    


class ListingPageBar():

    def __init__(self, bot):
        self.bot = bot
        self.total_pages = 15
        self.current_page = 1
        self.next_button = ElementPointer(By.XPATH, '//*[@id="results-display"]/div[5]/div/div[3]/button[2]', self.bot)
        #self.next_button = ElementPointer(By.CLASS_NAME, 'bp-Button PageArrow clickable Pagination__button PageArrow__direction--next bp-Button__type--ghost bp-Button__size--compact bp-Button__icon-only', self.bot)
        self.previous_button = ElementPointer(By.XPATH, '//*[@id="results-display"]/div[5]/div/div[3]/button[1]', self.bot)
    
    def create_pointer(self):
        self.next_button.create_pointer()
        self.previous_button.create_pointer()
    
    def get_pages(self):
        return self.total_pages
    
    def get_current_page(self):
        return self.current_page
    
    def next(self):
        try:
            self.current_page += 1
            self.next_button.element().click()
            self.bot.wait(1)
            return True
        except Exception as error:
            return False
           
    
    def previous(self):
        try:
            self.current_page -= 1
            self.previous_button.element().click()
            self.bot.wait(1)
            return True
        except Exception as error:
            return False
           


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


class BedsAndBath():
    def __init__(self, bot):
        self.bot = bot
        self.bed_bath_button = ElementPointer(By.XPATH, '', self.bot)
        self._click_done_button = ElementPointer(By.CLASS_NAME, "", self.bot)

        self.bed_bar = {
            'studio':None, 
            '1':None, 
            '2':None, 
            '3':None, 
            '4':None, 
            '5':None,
        }
        self.bath_bar = {
            '1':None, 
            '1.5':None, 
            '2':None,
            '2.5':None, 
            '3':None, 
            '4':None 
        }

    def click_bed_bath_button(self):
        pass
    def click_done_button(self):
        try:
            self._click_done_button.element().click()
        except Exception as error:pass



class HomeType():

    def __init__(self, bot):
        self.bot = bot
        #class_name for main_button = bp-ItemPicker PropertyTypes__items
        self.main_button = ElementPointer(By.XPATH, '/html/body/div[1]/div[8]/div[2]/div[1]/div[2]/div/div/div/div[1]/form/div[1]/div', self.bot)
        self.done_button = ElementPointer(By.XPATH, '/html/body/div[1]/div[8]/div[2]/div[1]/div[2]/div/div/div/div[1]/form/div[1]/div/div[2]/div/div[2]/button', self.bot)
        self.options = {
            'house':ElementPointer(By.CLASS_NAME, '//*[@id="sidepane-header"]/div/div/div[1]/form/div[3]/div/div[2]/div/div[1]/div[2]/div/div[1]', self.bot),
            'town_house':ElementPointer(By.CLASS_NAME, '//*[@id="sidepane-header"]/div/div/div[1]/form/div[3]/div/div[2]/div/div[1]/div[2]/div/div[2]', self.bot),
            'condo':ElementPointer(By.CLASS_NAME, '//*[@id="sidepane-header"]/div/div/div[1]/form/div[3]/div/div[2]/div/div[1]/div[2]/div/div[3]', self.bot),
            'land':ElementPointer(By.CLASS_NAME, '//*[@id="sidepane-header"]/div/div/div[1]/form/div[3]/div/div[2]/div/div[1]/div[2]/div/div[4]', self.bot),
            'multi_family':ElementPointer(By.CLASS_NAME, '//*[@id="sidepane-header"]/div/div/div[1]/form/div[3]/div/div[2]/div/div[1]/div[2]/div/div[5]', self.bot),
            'mobile':ElementPointer(By.CLASS_NAME, '//*[@id="sidepane-header"]/div/div/div[1]/form/div[3]/div/div[2]/div/div[1]/div[2]/div/div[6]', self.bot),
            'co_op':ElementPointer(By.CLASS_NAME, '//*[@id="sidepane-header"]/div/div/div[1]/form/div[3]/div/div[2]/div/div[1]/div[2]/div/div[7]', self.bot),
            'other':ElementPointer(By.CLASS_NAME, '//*[@id="sidepane-header"]/div/div/div[1]/form/div[3]/div/div[2]/div/div[1]/div[2]/div/div[8]', self.bot)
        }
                                                   
    def click_home_button(self):
        try:
            self.main_button.create_pointer()
            self.main_button.element().click()
            pass
        except Exception as error:
            print("HomeType Error click_home_button():", error)
        return self
    
    def choose_home_type(self, type):
        try:
            self.options[type].create_pointer()
            self.options[type].element().click()
        except Exception as error:
            print("HomeType Choosing Error choose_home_type():", error)
        return self
    
    def click_done(self):
        try:
            self.done_button.create_pointer()
            self.done_button.element().click()
        except Exception as error:
            print("HomeType Error click_done():", error)
        return self


class PaymentType():

    def __init__(self, bot):
        self.bot = bot
        self.bot_flag = Flag()
        self.main_payment_button = ElementPointer(By.XPATH, '/html/body/div[1]/div[8]/div[2]/div[1]/div[2]/div/div/div/div[1]/form/div[1]/div', self.bot)
        self.for_rent = ElementPointer(By.ID, 'forRent', self.bot)
        self.for_sale = ElementPointer(By.ID, 'for-sale', self.bot)
        self.done_button = ElementPointer(By.XPATH, '/html/body/div[1]/div[8]/div[2]/div[1]/div[2]/div/div/div/div[1]/form/div[1]/div/div[2]/div/div[2]/button', self.bot)
        if(self.bot == None):
            self.bot_flag.set_false()
        
        else:
            self.bot_flag.set_true()
    

    def click_payment_type_button(self):
        try:
            self.main_payment_button.create_pointer()
            self.main_payment_button.element().click()
        except Exception as error:
            print("PaymentType Error:", error)
            raise error
        return self
    
    def click_for_rent_button(self):
        try:
            self.for_rent.create_pointer()
            self.for_rent.element().click()
        except Exception as error:
            print("PaymentType Error:", error)
            raise error
        return self
    
    def click_for_sale_button(self):
        try:
            self.for_sale.create_pointer()
            self.for_sale.element().click()
        except Exception as error:
            print("PaymentType Error:", error)
            raise error
        
        return self

    def click_done(self):
        try:
            self.done_button.create_pointer()
            self.done_button.element().click()
        except Exception as error:
            print("PaymentType Error:", error)
            raise error
        return self


class PriceRange():
    def __init__(self, bot=None):
        self.bot_flag = Flag()
        self.bot = bot
        self.main_price_button = None
        self.enter_min_field = None
        self.minimum_amount = 1
        self.maximum_amount = 100000
        self.enter_max_field = None
        self.done_button = None
        if(bot == None):self.bot_flag.set_false()

        else:
            self.main_price_button = ElementPointer(By.XPATH, '/html/body/div[1]/div[8]/div[2]/div[1]/div[2]/div/div/div/div[1]/form/div[2]/div', self.bot)
            self.enter_min_field = ElementPointer(By.CSS_SELECTOR, "input[placeholder='Enter min']", self.bot)
            self.enter_max_field = ElementPointer(By.CSS_SELECTOR, "input[placeholder='Enter max']", self.bot)
            self.done_button = ElementPointer(By.XPATH, '//*[@id="sidepane-header"]/div/div/div[1]/form/div[2]/div/div[2]/div/div[2]/button[2]', self.bot)
            self.bot_flag.set_true()

    def click_price_button(self):
        if(self.bot_flag.check() == False):return
        try:
            self.main_price_button.create_pointer()
            self.main_price_button.element().click()
            return self
        except Exception as error:
            print("PriceRange: click_price_button() Error:", error)
    
    def send_minimum(self, amount):
        if(self.bot_flag.check() == False):return
        try:
            self.enter_min_field.create_pointer()
            self.enter_min_field.element().send_keys(amount)
            return self
        except Exception as error:
            print("PriceRange send_minimum() Error:", error)

    def send_maximum(self, amount):
        if(self.bot_flag.check() == False):return
        try:
            self.enter_max_field.create_pointer()
            self.enter_max_field.element().send_keys(amount)
            return self
        except Exception as error:
            print("PriceRange send_maximum() Error:", error)
    
    def click_done(self):
        if(self.bot_flag.check() == False):return
        try:
            self.done_button.create_pointer()
            self.done_button.element().click()
            return self
        except Exception as error:
            print("PriceRange click_done() Error", error)
    


class RedfinSearchFilter():
    def __init__(self, bot):
        self._house_type = PaymentType(bot)
        self._price_range = PriceRange(bot)
        self._home_type = HomeType(bot)
        self._bed_and_bath = BedsAndBath(bot)
    
    def payment_type(self):
        return self._house_type
    
    def price_range(self):
        return self._price_range

    def home_type(self):
        return self._home_type
    
    def bed_bath_type(self):
        return self._bed_and_bath
    

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
            print(error)
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
        #self.search_filter = RedfinSearchFilter(self.bot)
        self.listing_page_bar = ListingPageBar(self.bot)
        self.listings = []
        self.jsonified_listings = []
        self.listing_limit = 350
        #This is for the listing object
        #root = ElementPointer(By.CLASS_NAME, 'HomeCardContainer flex justify-center', self.bot)

    def address(self, address):
        self.location_address = address
    
    def fetch_listing_data(self):
        #APPLY FILTERS
        self.apply_filters()
        
        #FETCH THE LISTINGS
        self.listing_page_bar.create_pointer()
        try:
            for i in range(0, self.listing_page_bar.get_pages()):
                self.get_listings_on_page()
                self.bot.wait(2)
                status = self.listing_page_bar.next()
                if(status == False):
                    break
        except Exception as error:
            print(error)


        #EXPORT THE LISTINGS TO A JSON FILE
        #self.export_to_file(r"C:\Users\yasha\Visual Studio Workspaces\SystemX\ResideImageScrapper\ImageLibrary\san_diego.json")

    def get_listings_on_page(self):
         #NOTE:
            # - Need to make sure everything is error proof
            # - Need to figure out the file data saving problem
            # - Setup launch routes
            # - Setup the storage library

        try:
            for i in range(1, 39):
                element = self.bot.search_element(By.XPATH, '//*[@id="results-display"]/div[5]/div/div[1]/div/div['+ str(i) + ']').get_element()
                listing = Listing(self.bot, element)
                listing.print_meta_data('off')
                status = listing.process()
                if(status == True):
                    #self.listings.append(listing)
                    self.jsonified_listings.append((listing.export('json')))
                    print("Collected element: ", element.get_attribute('id'))
                else:print("\x1b[31mCouldn't collect element\x1b[0m", element.get_attribute('id'))
        except Exception as error:
            print("Element not found", error)


    def export_to_file(self, file_path):
        global export_file
        export_file = open(file_path, "w")
        json.dump(self.jsonified_listings, export_file, indent=4)
        export_file.close()


    def apply_filters(self):
        #self.search_filter.payment_type().click_payment_type_button().click_for_rent_button().click_done()
        #self.search_filter.price_range().click_price_button().send_minimum(10).send_maximum(60000).click_done()
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
        options.page_load_strategy = 'normal'
        self.driver = webdriver.Chrome(options=options)
        self.bot = Bot(INIT_URL, self.driver)
        self.tasks = Tasks()
        self.redfin_search = RedfinSearch(self.bot)
        self.redfin_filter = RedfinSearchFilter(self.bot)
        self.specific_fetcher = SpecificLocation(self.bot)
        self.general_fetcher = GeneralLocation(self.bot)
        self._address = None
        self.listing_response = None
        self.listing_type = 'specific'
        self._filter = None
        #self.bot.activate()

    def activate(self):
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
            
            close_val = '/html/body/div[2]/div[2]/div/div[2]/button'
            close_cookies = self.bot.search_element(By.XPATH, close_val).get_element()
            close_cookies.click()
            
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


    def get_response(self):
        #LOGIN
        value = self.login_to_website(credentials=('yashaswi.kul@gmail.com', 'yashema@E494murlipura2'))
        if(value == LOGIN_ERROR_CODE): return LOGIN_ERROR_CODE
        
        #SEARCHING
        self.redfin_search.set_location_address(self._address)
        value = self.redfin_search.perform()
        if(value == SEARCHING_ERROR_CODE): return SEARCHING_ERROR_CODE


        #APPLYING FILTERS
        try:
            self.__apply_filters()
            self.bot.wait(2)
        except Exception as error:
            print("\x1b[FILTERS!! ERROR\x1b[0m", error)


        #FETCHING
        if(self.listing_type == 'general'):
            self.listing_response = self.general_fetcher.fetch_listing_data()
            if(self.listing_response == DATA_FETCHING_ERROR_CODE): return DATA_FETCHING_ERROR_CODE
        
        elif(self.listing_type == 'specific'):
            self.listing_response = self.specific_fetcher.fetch_listing_data()
            if(self.listing_response == DATA_FETCHING_ERROR_CODE): return DATA_FETCHING_ERROR_CODE

        return self.listing_response
    
    def save_filters(self, filters):
        self._filter = filters

    def __apply_filters(self):
        if(self._filter == None):
            print("FILTER NONE!!!")
            return
        for filter in self._filter:
            print("____Processing filters in list______")
            self.__apply_filter(filter)

    def __apply_filter(self, value):
        print("*****Entered single filter*****")
        home_types = ['town_house', 'condo', 'land', 'multi_family', 'mobile', 'co_op', 'other']
        if(value == 'For rent'):
            print("Entered to apply rent filter")
            self.filters().payment_type().click_payment_type_button().click_for_rent_button().click_done()
        
        elif(value == 'For sale'):

            self.filters().payment_type().click_payment_type_button().click_for_sale_button().click_done()
        
        elif(value in home_types):
            self.filters().home_type().choose_home_type(value).click_done()
        
        elif('price=' in value):
            index = value.find("(")+1
            min = int(value[index])
            max = int(value[value.find(",")+1])
            self.filters().price_range().click_price_button().send_minimum(min).send_maximum(max).click_done()


    def filters(self):
        return self.redfin_filter
    
    def address(self, address):
        self._address = address
        return self
    
    def location(self, type):
        self.listing_type = type
        return self
    
    def close(self):
        self.bot.close()


bot = RedfinBot()
bot.activate()
bot.save_filters(['For rent'])
bot.address('san diego').location('general').get_response()

"""
TODO:
    - Finish everything about the bot
       - Filters
       - Finish all the tests

     - Next Step:
        - Setup library routes
            - Library:
                - How do we wanna fetch one listing out of hundreds efficiently?
                    - Maybe some sorta direct mapping instead of just one single large file
    
        - Setup bots routes

     - Next Step:
        - Make Java endpoint

     - Future Step:
        - Server:
            - Ability to server very fast from anywhere
            - Supports auto routes for new bots

     - Automation Step:
            - Bot organization:
                 - Ability to create just one folder
                   And the rest of the code auto integrates
                   this new bot with a config.json file

        
"""