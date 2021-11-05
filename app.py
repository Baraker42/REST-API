from flask import Flask, abort
import mysql.connector
from flask_restful import Api, Resource, reqparse
from secret import Password
import json


#There you have to define your connection with MYSQL
try:
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=Password.passwrd,
    database="Restaurants"
    )

except:
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=Password.passwrd,
    )

app = Flask(__name__)
api = Api(app)
my_cursor = db.cursor()

#Creating tables in database if not already created
try:
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS Restaurants")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS Restaurants(id int PRIMARY KEY AUTO_INCREMENT,name VARCHAR(255) NOT NULL,contact VARCHAR(255) NOT NULL,opening_hours VARCHAR(255) NOT NULL, address VARCHAR(255) NOT NULL)")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS Meals(id int PRIMARY KEY AUTO_INCREMENT, rest_id int NOT NULL, FOREIGN KEY (rest_id) REFERENCES Restaurants(id), name VARCHAR(255) NOT NULL, day VARCHAR(10) NOT NULL, price FLOAT(10) NOT NULL)")
except:
    print("Database you try connect, doesn't exist.")
    quit()

#Prepare getting arguments from used URL
restaurant_put_args = reqparse.RequestParser()
restaurant_put_args.add_argument("name", type=str, help="Name of the restaurant is required", required=True)
restaurant_put_args.add_argument("contact", type=str, help="Contact of the restaurant is required", required=True)
restaurant_put_args.add_argument("opening_hours", type=str, help="Opening hours of the restaurant is required", required=True)
restaurant_put_args.add_argument("address", type=str, help="Address of the restaurant is required", required=True)

restaurant_update_args = reqparse.RequestParser()
restaurant_update_args.add_argument("name", type=str, help="Name of the restaurant")
restaurant_update_args.add_argument("contact", type=str, help="Contact of the restaurant")
restaurant_update_args.add_argument("opening_hours", type=str, help="Opening hours of the restaurant")
restaurant_update_args.add_argument("address", type=str, help="Address of the restaurant")

meal_put_args = reqparse.RequestParser()
meal_put_args.add_argument("name", type=str, help="Name of the meal is required", required=True)
meal_put_args.add_argument("day", type=str, help="Day when is meal serve is required", required=True)
meal_put_args.add_argument("price", type=float, help="Price of the meal is required", required=True)

meal_update_args = reqparse.RequestParser()
meal_update_args.add_argument("name", type=str, help="Name of the meal")
meal_update_args.add_argument("day", type=str, help="Day when meal is serve")
meal_update_args.add_argument("price", type=float, help="Price of the meal")

#Class for creating new restaurant(post) or get list of all IDs and names restaurants(get)
class AllRestaurants(Resource):
    def post(self):
        args = restaurant_put_args.parse_args()
        my_cursor.execute("INSERT INTO Restaurants(name,contact,opening_hours,address) VALUES(%s,%s,%s,%s)", (args["name"],args["contact"],args["opening_hours"],args["address"]))
        db.commit()
        return json.dumps({"name":args["name"], "contact":args["contact"], "opening_hours":args["opening_hours"], "address":args["address"]},ensure_ascii=False)

    def get(self):
        my_cursor.execute("SELECT * FROM Restaurants")
        row=my_cursor.fetchall()
        if row is None:
            abort(404, description="There are no any restaurant yet")
        #my_cursor.execute("SELECT name FROM Restaurants")
        restaurant_list=[]
        for i in row:
            restaurant={"id":i[0], "name":i[1]}
            restaurant_list.append(restaurant)
        return json.dumps(restaurant_list,ensure_ascii=False)

#Class for getting details about specific restaurant(get), updating information(put) and delete restaurant(delete)
class Restaurant(Resource):
    def get(self, restaurant_id):
        my_cursor.execute("SELECT * FROM Restaurants WHERE id={0}".format(restaurant_id))
        restaurant_detail=[]
        for i in my_cursor:
            restaurant={"id":i[0], "name":i[1],"contact":i[2],"opening_hours":i[3],"address":i[4]}
            restaurant_detail.append(restaurant)
        if len(restaurant_detail)==0:
            abort(404, description="Restaurant with this ID doesn´t exists")
        return json.dumps(restaurant_detail[0],ensure_ascii=False)

    def put(self, restaurant_id):
        args= restaurant_update_args.parse_args()
        my_cursor.execute("SELECT * FROM Restaurants WHERE id={0}".format(restaurant_id))
        restaurant={}
        row=my_cursor.fetchall()
        if row is None:
            abort(404, description="Restaurant with this ID doesn´t exists")
        if args["name"]:
            my_cursor.execute("UPDATE Restaurants SET name='{0}' WHERE id={1}".format(args["name"], restaurant_id))
            restaurant={"name":args["name"]}
        if args["contact"]:
            my_cursor.execute("UPDATE Restaurants SET contact={0} WHERE id={1}".format(args["contact"],restaurant_id))
            restaurant={"contact":args["contact"]}
        if args["opening_hours"]:
            my_cursor.execute("UPDATE Restaurants SET opening_hours='{0}' WHERE id={1}".format(args["opening_hours"],restaurant_id))
            restaurant={"opening_hours":args["opening_hours"]}
        if args["address"]:
            my_cursor.execute("UPDATE Restaurants SET address='{0}' WHERE id={1}".format(args["address"],restaurant_id))
            restaurant={"address":args["address"]}
        db.commit()
        return json.dumps(restaurant,ensure_ascii=False)

    def delete(self, restaurant_id):
        my_cursor.execute("SELECT * FROM Restaurants WHERE id={0}".format(restaurant_id))
        row = my_cursor.fetchone()
        if row is None:
            abort(404, description="There is no restaurant with this ID")
        #if restaurant allready contains some meals this command delete meals first
        my_cursor.execute("SELECT * FROM Meals WHERE rest_id={0}".format(restaurant_id))
        for i in my_cursor:
            meal_id=(i[1])
            my_cursor.execute("DELETE FROM Meals WHERE id={0}".format(meal_id))
            db.commit()
        my_cursor.execute("DELETE FROM Restaurants WHERE id={0}".format(restaurant_id))
        db.commit()
        return json.dumps({"message":"Restaurant was successfully deleted"})
#Class for getting all menu of specific restaurant
class RestaurantMenu(Resource):
    def get(self, restaurant_id):
        my_cursor.execute("SELECT * FROM Restaurants WHERE id={0}".format(restaurant_id))
        row = my_cursor.fetchone()
        if row is None:
            abort(404, description="There is no restaurant with this ID")
        my_cursor.execute("SELECT * FROM Meals WHERE rest_id={0}".format(restaurant_id))
        restaurant_menu=[]
        for i in my_cursor:
            meal={"id":i[0],"name":i[2],"day":i[3],"price":i[4]}
            restaurant_menu.append(meal)
        if len(restaurant_menu)==0:
            abort(404, description="There are no meals in this restaurant yet")
        return json.dumps(restaurant_menu)

#Class for get menu for specific day
class RestaurantDaily(Resource):
    def get(self, restaurant_id, day):
        my_cursor.execute("SELECT * FROM Restaurants WHERE id={0}".format(restaurant_id))
        row = my_cursor.fetchone()
        if row is None:
            abort(404, description="There is no restaurant wit this ID")
        my_cursor.execute("SELECT * FROM Meals WHERE rest_id={0} AND day='{1}'".format(restaurant_id, day))
        daily_menu=[]
        for i in my_cursor:
            meal={"id":i[0],"name":i[2],"day":i[3],"price":i[4]}
            daily_menu.append(meal)
        if len(daily_menu)==0:
            abort(404, description="There are no meals of this day in restaurant yet")
        return json.dumps(daily_menu)

#Class for creating new meal object
class NewMeal(Resource):
    def post(self,restaurant_id):
        try:
            args = meal_put_args.parse_args()
            my_cursor.execute("INSERT INTO Meals(rest_id,name,day,price) VALUES(%s,%s,%s,%s)",(restaurant_id,args["name"],args["day"],args["price"]))
            db.commit()
            return json.dumps({"name":args["name"], "day":args["day"], "price":args["price"]})
        except:
            return json.dumps({"message":"There is no such restaurant with this id"})

#Class for updating meal(put) or delete it(delete)
class UpdateMeal(Resource):
    def put(self,meal_id):
        args = meal_update_args.parse_args()
        my_cursor.execute("SELECT * FROM Meals WHERE id={0}".format(meal_id))
        row = my_cursor.fetchone()
        if row is None:
            abort(404, description="There is no meal with this ID")
        update={}
        if args["name"]:
            my_cursor.execute("UPDATE Meals SET name='{0}' WHERE id={1}".format(args["name"],meal_id))
            update={"name":args["name"]}
        if args["day"]:
            my_cursor.execute("UPDATE Meals SET day='{0}' WHERE id={1}".format(args["day"],meal_id))
            update={"day":args["day"]}
        if args["price"]:
            my_cursor.execute("UPDATE Meals SET price={0} WHERE id={1}".format(args["price"],meal_id))
            update={"price":args["price"]}
        db.commit()
        return json.dumps(update,ensure_ascii=False)

    def delete(self,meal_id):
        my_cursor.execute("SELECT * FROM Meals WHERE id={0}".format(meal_id))
        row = my_cursor.fetchone()
        if row is None:
            abort(404, description="Meal with this ID doesn´t exists")
        my_cursor.execute("DELETE FROM Meals WHERE id={0}".format(meal_id))
        db.commit()
        return json.dumps({"message":"Meal was deleted successfully"})


api.add_resource(AllRestaurants,"/restaurants/") #create new restaurant(post)/get list(get)
api.add_resource(Restaurant,"/restaurant/<int:restaurant_id>")#GET detail/PUT change of restaurant/DELETE restaurant
api.add_resource(RestaurantMenu,"/restaurant/<int:restaurant_id>/menu")#GET all meal of specific restaurant of whole week
api.add_resource(RestaurantDaily,"/restaurant/<int:restaurant_id>/<string:day>")#GET menu for specific day

api.add_resource(NewMeal,"/restaurant/<int:restaurant_id>/new_meal")#create new meal
api.add_resource(UpdateMeal, "/meal/<int:meal_id>")#PUT change of meal/DELETE meal

if __name__ == "__main__":
    app.run(debug=True)