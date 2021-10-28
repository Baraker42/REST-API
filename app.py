#import modules
from flask import abort, Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import json

#set basic interface
app = Flask(__name__)
api = Api(app)
#app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:myslq42dbpff@localhost/testor"#"sqlite:///database.db" #
app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///database.db"


db = SQLAlchemy(app)

#model for restaurant
class Restaurant_model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    opening_hours = db.Column(db.String(12),nullable=False)
    address = db.Column(db.String(100), nullable=False)
    menu = db.relationship("Menu_model", backref="restaurant",lazy=True)

    def __repr__(self):
        return "Restaurant(id={id}, name={name})"

#model for meals/menu
class Menu_model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    day = db.Column(db.String(10),nullable=False)
    price = db.Column(db.Float,nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant_model.id"),nullable=False)

    def __repr__(self):
        return "Meal(name={name}, day={day},price={price},restaurant_id{})"

#CREATE DATABASE (only for first run)
db.create_all()

#arguments for add new restaurant
restaurant_put_args = reqparse.RequestParser()
restaurant_put_args.add_argument("name", type=str, help="Name of the restaurant is required", required=True)
restaurant_put_args.add_argument("contact", type=str, help="Contact of the restaurant is required", required=True)
restaurant_put_args.add_argument("opening_hours", type=str, help="Opening hours of the restaurant is required", required=True)
restaurant_put_args.add_argument("address", type=str, help="Address of the restaurant is required", required=True)

#arguments for update restaurant
restaurant_update_args = reqparse.RequestParser()
restaurant_update_args.add_argument("name", type=str, help="Name of the restaurant")
restaurant_update_args.add_argument("contact", type=str, help="Contact of the restaurant")
restaurant_update_args.add_argument("opening_hours", type=str, help="Opening hours of the restaurant")
restaurant_update_args.add_argument("address", type=str, help="Address of the restaurant")

#arguments for add new meal
meal_put_args = reqparse.RequestParser()
meal_put_args.add_argument("name", type=str, help="Name of the meal is required", required=True)
meal_put_args.add_argument("day", type=str, help="Day is required", required=True)
meal_put_args.add_argument("price",type=float, help="Price of the meal is required",required=True)

#arguments for update meal
meal_patch_args = reqparse.RequestParser()
meal_patch_args.add_argument("name", type=str, help="Name of the meal")
meal_patch_args.add_argument("day", type=str, help="Day")
meal_patch_args.add_argument("price",type=float, help="Price of the meal")

#create resource fields
resource_fields_restaurant = {
    "id":fields.Integer,
    "name":fields.String,
    "contact":fields.String,
    "opening_hours":fields.String,
    "address":fields.String,
}
#create resource for short description
resource_fields_restaurant_short = {
    "id":fields.Integer,
    "name":fields.String,
}

resource_fields_menu = {
    "id":fields.Integer,
    "name":fields.String,
    "day":fields.String,
    "price":fields.Float,
    "restaurant_id":fields.Integer,
}


class AllRestaurants(Resource):
    #class for request all restaurants
    @marshal_with(resource_fields_restaurant_short)
    def get(self):
        result = Restaurant_model.query.order_by(Restaurant_model.id).all()
        if not result:
            abort(404, description="No restaurant found")
        return result

    #create new restaurant
    @marshal_with(resource_fields_restaurant)
    def post(self):
        args = restaurant_put_args.parse_args()
        all_restaurants = Restaurant_model.query.order_by(Restaurant_model.id).all()
        if len(all_restaurants) != 0:
            restaurant_id = all_restaurants[(len(all_restaurants))-1].id
            restaurant_id += 1
        else:
            restaurant_id = 1
        restaurant = Restaurant_model(id=restaurant_id, name=args["name"],contact=args["contact"],opening_hours=args["opening_hours"],address=args["address"])
        db.session.add(restaurant)
        db.session.commit()
        return restaurant, 201


#class for request specific restaurant information
class Restaurant(Resource):
    @marshal_with(resource_fields_restaurant)
    def get(self, restaurant_id):
        result = Restaurant_model.query.filter_by(id=restaurant_id).first()
        if not result:
            abort(404, description="Restaurant ID not found")
        return result


    @marshal_with(resource_fields_restaurant)
    def put(self, restaurant_id):
        args = restaurant_update_args.parse_args()
        result = Restaurant_model.query.filter_by(id=restaurant_id).first()

        if not result:
            abort(404, description="Restaurant with this ID doesn´t exists")
        if args["name"]:
            result.name = args["name"]
        if args["contact"]:
            result.contact = args["contact"]
        if args["opening_hours"]:
            result.opening_hours = args["opening_hours"]
        if args["address"]:
            result.address = args["address"]

        db.session.commit()
        return result


    def delete(self, restaurant_id):
        result = Restaurant_model.query.filter_by(id=restaurant_id).first()
        for i in result.menu:
            db.session.delete(i)
        if not result:
            abort(404, description="Restaurant ID not found")

        db.session.delete(result)

        db.session.commit()
        return {"message": "Restaurant was successfully deleted"}

#class for request all meals in specific restaurant
class RestaurantMenu(Resource):
    @marshal_with(resource_fields_menu)
    def get(self, restaurant_id):
        result = Restaurant_model.query.filter_by(id=restaurant_id).first()
        if not result:
            abort(404, description="Restaurant ID not found")
        if(len(result.menu))==0:
            abort(404, description="This restaurant has no menu yet.")

        return result.menu

class NewMeal(Resource):
    @marshal_with(resource_fields_menu)
    def post(self, restaurant_id):
        args = meal_put_args.parse_args()
        all_meals = Menu_model.query.order_by(Menu_model.id).all()
        if len(all_meals) != 0:
            menu_id = all_meals[(len(all_meals))-1].id
            menu_id += 1
        else:
            menu_id = 1
        restid = Restaurant_model.query.filter_by(id=restaurant_id).first()
        if not restid:
            abort(404, description="Restaurant id not exists.")
        meal = Menu_model(id=menu_id, name=args["name"],day=args["day"],price=args["price"],restaurant=restid)

        db.session.add(meal)
        db.session.commit()
        return meal, 201


class PatchMeal(Resource):
    @marshal_with(resource_fields_menu)
    def put(self, meal_id):
        args = meal_patch_args.parse_args()
        result = Menu_model.query.filter_by(id=meal_id).first()
        if not result:
            abort(404, description="Meal with this ID doesn´t exists")
        if args["name"]:
            result.name = args["name"]
        if args["day"]:
            result.day = args["day"]
        if args["price"]:
            result.price = args["price"]

        db.session.commit()
        return result


    def delete(self, meal_id):
        result = Menu_model.query.filter_by(id=meal_id).first()

        if not result:
            abort(404, description="Meal with this ID doesn´t exists")

        db.session.delete(result)
        db.session.commit()
        return{"message":"Meal was successfully deleted"}

#routes for request classes
api.add_resource(AllRestaurants,"/restaurants/")
api.add_resource(Restaurant,"/restaurant/<int:restaurant_id>")
api.add_resource(RestaurantMenu,"/restaurant/<int:restaurant_id>/menu")

api.add_resource(NewMeal,"/<int:restaurant_id>/new_meal")
api.add_resource(PatchMeal, "/meal/<int:meal_id>")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5444 ,debug=True)