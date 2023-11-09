import pandas as pd
import requests
import json

payload = {'item': "ram"}
#url = 'UEL?name=rai'
#url = 'URL?account_id=rsisvdngqvkm'

response = requests.post(url, json = payload, headers = {'Content-Type': 'application/json'})
print(response.json())
