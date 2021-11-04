import requests
import json

BASE = "http://127.0.0.1:5000/"
#response = requests.post(BASE + "restaurants/",{"name":"Lokááál","contact":"7388124","opening_hours":"10-24","address":"Formanská 56"})
#response = requests.put(BASE + "restaurant/1",{"name":"lelek"})
#print(response.json())
#response = requests.post(BASE + "1/new_meal",{"name":"svickova","day":"pondeli","price":"200.00"})
#response = requests.post(BASE + "1/new_meal",{"name":"gulash","day":"utery","price":"200.00"})
#response = requests.post(BASE + "1/new_meal",{"name":"koprovka","day":"streda","price":"200.00"})
#response = requests.post(BASE + "1/new_meal",{"name":"rajska","day":"ctvrtek","price":"200.00"})
#response = requests.post(BASE + "1/new_meal",{"name":"spagety","day":"patek","price":"200.00"})
#response = requests.delete(BASE + "restaurant/1")
#print(response.json())
#response = requests.get(BASE + "meals")
#response = requests.put(BASE + "/meal/5",{"price":"150.00"})
#response = requests.delete(BASE + "meal/1")
#response = requests.get(BASE + "/restaurant/1/streda")
#print(response.json())

#response = requests.put(BASE + "/meal/1",{"name":"zelnacka"})
response = requests.get(BASE + "restaurants/")

#response = requests.get(BASE + "1/menu")
#response = requests.delete(BASE + "/meal/5")
#response = requests.get(BASE + "restaurants/")
print(response.json())

