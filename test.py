import requests
import json

BASE = "http://127.0.0.1:5000/"
#response = requests.post(BASE + "restaurants/",{"name":"Vendys","contact":"7388124","opening_hours":"10-24","address":"Formanská 56"})
#response = requests.put(BASE + "restaurant/1",{"contact":"73722271214"})
#print(response.json())
#response = requests.post(BASE + "1/new_meal",{"name":"svickova","day":"pondeli","price":"200.00"})
#response = requests.post(BASE + "1/new_meal",{"name":"gulash","day":"pondeli","price":"200.00"})
#response = requests.post(BASE + "1/new_meal",{"name":"koprovka","day":"pondeli","price":"200.00"})
#response = requests.get(BASE + "restaurant/15")
#print(response.json())
#response = requests.get(BASE + "meals")
#response = requests.patch(BASE + "meal/1",{"name":"koprovka"})
#response = requests.delete(BASE + "meal/1")
response = requests.delete(BASE + "restaurant/12")
#print(response.json())

#response = requests.put(BASE + "2/new_meal",{"name":"zelnacka","day":"pondeli","price":"50.00"})
#response = requests.get(BASE + "restaurant/15")

#response = requests.get(BASE + "1/menu")
#response = requests.delete(BASE + "/meal/1")
#response = requests.get(BASE + "restaurants/")
print(response.json())

