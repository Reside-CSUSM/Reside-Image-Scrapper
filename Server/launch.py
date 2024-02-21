import requests
import time


"""
Routes:
    - /library
         -/by general area:
         -/by specific area
    
    - /bot
         -/launch
            -/by specific address
            -/by general area
         
         -/cache
            -/by specific area
            -/by general area    

         -/others   
"""


for i in range(0, 4):
    value = requests.get('http://127.0.0.1:9999/jk')
    print(value.text)
    time.sleep(0.1)