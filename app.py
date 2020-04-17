import os
import json
from flask import Flask, request, jsonify, render_template, Blueprint
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import(
    JWTManager, get_jwt_identity
)
from datetime import timedelta
from models import db, User
from routes.user import route_users


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
jwt = JWTManager(app)
db.init_app(app)
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

if __name__ == "__main__":
    manager.run()
