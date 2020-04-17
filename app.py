import json
# imports of flask libraries used here

from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# imports of the sql tables
from models import db
from models import Todos

# app inits and coginfs
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["DEBUG"] = True
app.config["ENV"] = "development"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:occam463871@localhost/mytodoapi"

db.init_app(app)
Migrate(app, db)
bcrypt = Bcrypt(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

CORS(app)

# begining of routes
@app.route("/")
def main():
    return render_template("index.html")


#routes goes here

if __name__ == "__main__":
    manager.run()
