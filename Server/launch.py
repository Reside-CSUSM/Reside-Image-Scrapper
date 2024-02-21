import requests
import time


for i in range(0, 4):
    value = requests.get('http://127.0.0.1:9999/jk')
    print(value.text)
    time.sleep(0.1)