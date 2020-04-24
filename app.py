import os
import json
from flask import Flask, request, jsonify, render_template, Blueprint, jsonify, send_from_directory
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_jwt_extended import(
    JWTManager, get_jwt_identity
)
from datetime import timedelta
from models import db, User, Restaurantuser
from routes.user import route_users
from routes.restaurantuser import route_restaurantusers
from routes.sendemail import sendemail
from routes.forgotPassUser import route_forgetpassusers
from routes.forgotPassRestaurantUser import route_forgetpassrestaurantusers
from routes.forgotPassAdmin import route_forgetpassadmin
from routes.admin import route_admins
from routes.product import route_product
from routes.ingredient import route_ingredient
from routes.orders import route_orders

# app inits and coginfs
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["DEBUG"] = True
app.config["ENV"] = "development"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['JWT_SECRET_KEY'] = 'super-secrets'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1000)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'fineukraine94@gmail.com'
app.config['MAIL_PASSWORD'] = 'dqhxchlvckgjlbks'
jwt = JWTManager(app)
db.init_app(app)
mail = Mail(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

CORS(app)

# begining of routes
@app.route("/")
def main():
    return render_template("index.html", name = 'home')


app.register_blueprint(route_users)
app.register_blueprint(route_restaurantusers)
app.register_blueprint(route_admins)
<<<<<<< HEAD
app.register_blueprint(route_product)
app.register_blueprint(route_ingredient)
app.register_blueprint(route_ingredient)
=======
app.register_blueprint(route_forgetpassusers)
app.register_blueprint(route_forgetpassrestaurantusers)
app.register_blueprint(route_forgetpassadmin)
>>>>>>> 7a11b515584f076b4fd9f3c82e7f2c6e1265c150

if __name__ == "__main__":
    manager.run()
