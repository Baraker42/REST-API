from flask import Flask, abort, jsonify
import mysql.connector
from flask_restful import Api, Resource, reqparse, marshal_with, fields
import json

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysql42dbpff",
    database="TestRest"
    )
app = Flask(__name__)
api = Api(app)
my_cursor = db.cursor()
#mycursor.execute("CREATE DATABASE TestRest")

#my_cursor.execute("CREATE TABLE Restaurants(id int PRIMARY KEY AUTO_INCREMENT,name VARCHAR(255) NOT NULL,contact VARCHAR(255) NOT NULL,opening_hours VARCHAR(255) NOT NULL, address VARCHAR(255) NOT NULL)")
#my_cursor.execute("CREATE TABLE Meals(id int PRIMARY KEY AUTO_INCREMENT, rest_id int NOT NULL, FOREIGN KEY (rest_id) REFERENCES Restaurants(id), name VARCHAR(255) NOT NULL, day VARCHAR(10) NOT NULL, price FLOAT(10) NOT NULL)")

#my_cursor.execute("INSERT INTO Restaurants(name,contact,opening_hours,address) VALUES(%s,%s,%s,%s)", ('Radev','79795346','10-22','Formanska'))
#my_cursor.execute("INSERT INTO Meals(rest_id,name,day,price) VALUES(%s,%s,%s,%s)",(1,"svickova","patek","200.00"))
#db.commit()

#my_cursor.execute("SELECT * FROM meals WHERE rest_id=1")

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


class AllRestaurants(Resource):
    def post(self):
        args = restaurant_put_args.parse_args()
        my_cursor.execute("INSERT INTO Restaurants(name,contact,opening_hours,address) VALUES(%s,%s,%s,%s)", (args["name"],args["contact"],args["opening_hours"],args["address"]))
        db.commit()
        return json.dumps({"name":args["name"], "contact":args["contact"], "opening_hours":args["opening_hours"], "address":args["address"]},ensure_ascii=False)

    def get(self):
        my_cursor.execute("SELECT id,name FROM Restaurants")
        restaurant_list=[]
        for i in my_cursor:
            restaurant={"id":i[0], "name":i[1]}
            restaurant_list.append(restaurant)
        if len(restaurant_list)==0:
            abort(404, description="There are no any restaurant yet")
        return json.dumps(restaurant_list,ensure_ascii=False)

class Restaurant(Resource):
    def get(self, restaurant_id):
        my_cursor.execute("SELECT * FROM Restaurants WHERE id="+str(restaurant_id))
        restaurant_detail=[]
        for i in my_cursor:
            restaurant={"id":i[0], "name":i[1],"contact":i[2],"opening_hours":i[3],"address":i[4]}
            restaurant_detail.append(restaurant)
        if len(restaurant_detail)==0:
            abort(404, description="Restaurant with this ID doesn´t exists")
        return json.dumps(restaurant_detail[0],ensure_ascii=False)

    def put(self, restaurant_id):
        args= restaurant_update_args.parse_args()
        if args["name"]:
            my_cursor.execute("UPDATE Restaurants SET name={0} WHERE id={1}".format(args["name"], restaurant_id))
        if args["contact"]:
            my_cursor.execute("UPDATE Restaurants SET contact={0} WHERE id={1}".format(args["contact"],restaurant_id))
        if args["opening_hours"]:
            my_cursor.execute("UPDATE Restaurants SET opening_hours={0} WHERE id={1}".format(args["opening_hours"],restaurant_id))
        if args["address"]:
            my_cursor.execute("UPDATE Restaurants SET address={0} WHERE id={1}".format(args["address"],restaurant_id))
        for i in args:
            print(i)
        db.commit()
        return json.dumps({"name":args["name"], "contact":args["contact"], "opening_hours":args["opening_hours"], "address":args["address"]},ensure_ascii=False)

    def delete(self, restaurant_id):
        my_cursor.execute("SELECT * FROM Meals WHERE rest_id={0}".format(restaurant_id))
        for i in my_cursor:
            meal_id=(i[1])
            my_cursor.execute("DELETE FROM Meals WHERE id="+str(meal_id))
            db.commit()
        my_cursor.execute("DELETE FROM Restaurants WHERE id="+str(restaurant_id))
        db.commit()
        return json.dumps({"message":"Restaurant was successfully deleted"})

api.add_resource(AllRestaurants,"/restaurants/")
api.add_resource(Restaurant,"/restaurant/<int:restaurant_id>")
#api.add_resource(RestaurantMenu,"/restaurant/<int:restaurant_id>/menu")

#api.add_resource(NewMeal,"/<int:restaurant_id>/new_meal")
#api.add_resource(PatchMeal, "/meal/<int:meal_id>")

if __name__ == "__main__":
    app.run(debug=True)