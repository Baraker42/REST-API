# REST-API
## Description
Restaurant REST API allows management of information about restaurants and menu for the day.<br/>
You can add, update or delete restaurant or meal informations<br/>
This REST-API communicates with the MYSQL

## Use
For add or edit restaurants or meals you can use 'curl' or test.py. Script test.py allows you to run more commands suddenly.</br/>

### curl commands
For GET list of all restaurants on localhost use ```curl http://127.0.0.1:5000/restaurants```<br/>
GET all information about specific restaurant use ```curl http://127.0.0.1:5000/restaurant/+restaurant_id```<br/>
POST new restaurant use ```curl -X POST -d "name=restaurant_name&contact=contact&opening_hours=opening_hours&address=address" http://127.0.0.1:5000/restaurants/```<br/>
For update all information using PUT command EXAMPLE ```curl -X PUT -d "name=new_restaurant_name" http://127.0.0.1:5000/restaurant/+restaurant_id```<br/>
DELETE you can execute using command ```curl -X DELETE http://127.0.0.1:5000/restaurant/restaurant_id```<br/>
If you want to see all menu for restaurant ```curl http://127.0.0.1:5000/restaurant/+restaurant_id/menu```<br/>
For menu only for one day ```curl http://127.0.0.1:5000/restaurant/+restaurant id/day_you_want_to_check```<br/>
To add new meal to restaurant use command ```curl -X POST -d "name=meal_name&day=day&price=price" http://127.0.0.1:5000/restaurant/restaurant_id/new_meal```<br/>
If you want to update existing meal use PUT command ```curl -X PUT -d "name=new_meal_name" http://127.0.0.1:5000/meal/+meal_id```<br/>
And for DELETE you command ```curl -X DELETE -d http://127.0.0.1:5000/meal/+meal_id```<br/>
