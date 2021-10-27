import requests
import json

BASE = "http://127.0.0.1:5000/"
#response = requests.put(BASE + "restaurant/55",{"name":"Radekljv","contact":"7377124","opening_hours":"14-24"})
#response = requests.put(BASE + "restaurant/55/meal/97/",{"name":"svickova","day":"pondeli","price":"200.00"})
response = requests.get(BASE + "restaurant/55")
print(response.json())
#response = requests.get(BASE + "restaurant/6")
#response = requests.put(BASE + "restaurant/55/meal/96/",{"name":"zelnacka","day":"pondeli","price":"50.00"})
#response = requests.get(BASE + "restaurant/55")


