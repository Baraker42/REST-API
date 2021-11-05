import requests
import json

BASE = "http://127.0.0.1:5000/"
#response = requests.post(BASE + "restaurants/",{"name":"name","contact":"contact","opening_hours":"opening_hours","address":"address"}) Add new restaurant to the database, every parameter is required
#response = requests.get(BASE + "restaurants/") Show the list of all restaurant
#response = requests.put(BASE + "restaurant/1",{"name":"newname"}) Change name of the restaurant with id 1 (You can use it for change every parameter)
#response = requests.delete(BASE + "restaurant/1") Delete restaurant with id 1 from database
#response = requests.get(BASE + "restaurant/1/menu") Show all meals in restaurant
#response = requests.get(BASE + "restaurant/1/day") Show all meals in restaurant served in set day
#response = requests.post(BASE + "1/new_meal",{"name":"name","day":"day","price":"price"}) Add new meal to the database connected with restaurant with id 1, every parameter is required
#response = requests.put(BASE + "/meal/1",{"price":"new_price"})Change price of the meal with id 1 (You can use it for change every parameter)
#response = requests.delete(BASE + "meal/1") Delete meal with id 1 from the database


#print(response.json())


