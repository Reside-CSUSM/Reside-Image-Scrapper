import sys
sys.path.insert(0, r'C:\Users\yasha\Visual Studio Workspaces\SystemX\ResideImageScrapper')
from Utility.bot import Bot
from selenium import webdriver
from Utility.utility import _ID, Flag
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



image_urls = [
    "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_57.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_54.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_55.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_56.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_49.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_1.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_50.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_51.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_60.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_52.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_53.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_59.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_2.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_48.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_4.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_3.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_5.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_11.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_12.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_8.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_7.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_9.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_6.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_10.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_23.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_14.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_19.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_20.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_16.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_18.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_21.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_22.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_25.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_46.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_45.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_47.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_41.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_35.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_43.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_26.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_27.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_28.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_29.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_30.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_40.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_38.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_36.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_37.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_39.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_61.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_57.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_54.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_55.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_56.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_49.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_1.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_50.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_51.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_60.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_52.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_53.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_59.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_2.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_48.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_4.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_3.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_5.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_11.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_12.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_8.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_7.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_9.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_6.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_10.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_23.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_14.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_19.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_20.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_16.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_18.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_21.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_22.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_25.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_46.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_45.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_47.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_41.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_35.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_43.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_26.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_27.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_28.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_29.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_30.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_40.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_38.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_36.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_37.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_39.jpg",
            "https://ssl.cdn-redfin.com/system_files/media/893195_JPG/genDesktopMapHomeCardUrl/item_61.jpg"
]

bot = Bot('http://google.com', webdriver.Chrome())
bot.activate()


for url in image_urls:
    bot.next_page(url)
    bot.wait(1.5)