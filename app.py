#import modules
from flask import abort, Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

#set basic interface
app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///database.db" #"mysql+pymysql://root:myslq42dbpff@localhost/movies"#
db = SQLAlchemy(app)

#model for restaurant
class Restaurant_model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    opening_hours = db.Column(db.String(12),nullable=False)
    menu = db.relationship("Menu_model", backref="restaurant",lazy=True)

    def __repr__(self):
        return "Restaurant(name={name}, contact={contact}, opening={opening_hours})"

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
#db.create_all()

#arguments for add new restaurant
restaurant_put_args = reqparse.RequestParser()
restaurant_put_args.add_argument("name", type=str, help="Name of the restaurant is required", required=True)
restaurant_put_args.add_argument("contact", type=str, help="Contact of the restaurant is required", required=True)
restaurant_put_args.add_argument("opening_hours", type=str, help="Opening hours of the restaurant is required", required=True)

#arguments for update restaurant
restaurant_update_args = reqparse.RequestParser()
restaurant_update_args.add_argument("name", type=str, help="Name of the restaurant")
restaurant_update_args.add_argument("contact", type=str, help="Contact of the restaurant")
restaurant_update_args.add_argument("opening_hours", type=str, help="Opening hours of the restaurant")

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
}

resource_fields_menu = {
    "id":fields.Integer,
    "name":fields.String,
    "day":fields.String,
    "price":fields.Float,
    "restaurant_id":fields.Integer,
}

class AllRestaurants(Resource):
    @marshal_with(resource_fields_restaurant)
    def get(self):
        result = Restaurant_model.query.order_by(Restaurant_model.id).all()
        if not result:
            abort(404, description="No restaurant found")
        return result

class Restaurant(Resource):
    @marshal_with(resource_fields_menu)
    def get(self, restaurant_id):
        result = Restaurant_model.query.filter_by(id=restaurant_id).first()
        if not result:
            abort(404, description="Restaurant ID not found")
        return result.menu

    @marshal_with(resource_fields_restaurant)
    def put(self,restaurant_id):
        args = restaurant_put_args.parse_args()
        result = Restaurant_model.query.filter_by(id=restaurant_id).first()
        if result:
            abort(409, description="Restaurant with this ID already exists")
        restaurant = Restaurant_model(id=restaurant_id, name=args["name"],contact=args["contact"],opening_hours=args["opening_hours"])
        print(restaurant)
        db.session.add(restaurant)
        db.session.commit()
        return restaurant, 201

    @marshal_with(resource_fields_restaurant)
    def patch(self, restaurant_id):
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

        db.session.commit()

        return result

    @marshal_with(resource_fields_restaurant)
    def delete(self, restaurant_id):
        result = Restaurant_model.query.filter_by(id=restaurant_id).first()
        if not result:
            abort(404, description="Video not found")
        db.session.delete(result)
        db.session.commit()
        return "Resaturant was deleted successfully", 204

class AllMeal(Resource):
    @marshal_with(resource_fields_menu)
    def get():
        return

class Meal(Resource):
    @marshal_with(resource_fields_menu)
    def get(self, restaurantid, meal_id):
        restid = Restaurant_model.query.filter_by(id=restaurantid).first()
        result = Menu_model.query.filter_by(id=meal_id).first()
        if not result:
            abort(404, description="Meal ID not found")
        return restid

    @marshal_with(resource_fields_menu)
    def put(self, restaurantid, meal_id):
        args = meal_put_args.parse_args()
        result = Menu_model.query.filter_by(id=meal_id).first()

        restid = Restaurant_model.query.filter_by(id=restaurantid).first()

        if result:
            abort(409, description="Meal with this ID already exists")

        meal = Menu_model(id=meal_id, name=args["name"],day=args["day"],price=args["price"],restaurant=restid)

        db.session.add(meal)
        db.session.commit()
        return meal, 201


api.add_resource(Restaurant,"/restaurant/<int:restaurant_id>")
api.add_resource(AllRestaurants,"/restaurant/")
api.add_resource(Meal,"/restaurant/<int:restaurantid>/meal/<int:meal_id>/")
#api.add_resource(AllMeal,"/restaurant/<int:restaurant_id>/all")


if __name__ == "__main__":
    app.run(debug=True)