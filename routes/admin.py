from flask import Blueprint, request, jsonify
from models import db, Admin
from flask_bcrypt import Bcrypt
from flask_jwt_extended import(
    jwt_required, create_access_token, create_access_token
)
bcrypt = Bcrypt()
route_admins = Blueprint('route_admins', __name__)
#yana
@route_admins.route('/admins', methods = ['GET'])
@route_admins.route('/admins/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def admins(id = None):
    if request.method == 'GET':
        if id is not None:
            admin = Admin.query.get(id)
            if admin:
                return jsonify(admin.serialize()), 200
            else:
                return jsonify({"admin": "Not found"}), 404
        else:
            admins = Admin.query.all()
            admins = list(map(lambda admin: admin.serialize(), admins))
            return jsonify(admins), 200

    if request.method == 'PUT':
        admin = Admin.query.get(id)
        admin.name = request.json.get('name')

        db.session.commit()

        return jsonify(admin.serialize()), 200

    if request.method == 'DELETE':
        admin = Admin.query.get(id)
        db.session.delete(admin)
        db.session.commit()

        return jsonify({'admin':'Deleted'}), 200
    
    
@route_admins.route('/adminlogin', methods=['POST'])
def login():
    email = request.json.get('email')
    password_hash = request.json.get('password_hash')
    if not email:
        return jsonify({"msg": "You need insert your email"}), 422
    if not password_hash:
        return jsonify({"msg": "You need insert your password"}), 422
    admin = Admin.query.filter_by(email=email).first()
    if not admin:
        return jsonify({"msg": "Email is not correct"}), 404
    pw_hash = bcrypt.generate_password_hash(password_hash)
    if bcrypt.check_password_hash(admin.password_hash, password_hash):
        access_token = create_access_token(identity=admin.email)
        data = {
            "access_token": access_token,
            "admin": admin.serialize()
        }
        return jsonify(data), 200
    else: 
        return jsonify({"msg": "Email or password is not correct"}), 401
        
@route_admins.route('/adminregistration', methods=['POST'])
def register():
    email = request.json.get('email')
    name = request.json.get('name')
    password_hash = request.json.get('password_hash')
    if not email:
        return jsonify({"msg": "You need to write yor email"}), 422
    if not name:
        return jsonify({"msg": "You need to write your name"}), 422       
    if not password_hash:
        return jsonify({"msg": "You need to write your password_hash"}), 422
    admin = Admin.query.filter_by(email=email).first()
    if admin:
        return jsonify({"msg": "This email already exist"}), 422
    admin = Admin()
    admin.email = email
    admin.name = name
    admin.password_hash = bcrypt.generate_password_hash(password_hash)
    db.session.add(admin)
    db.session.commit()
    if bcrypt.check_password_hash(admin.password_hash, password_hash):
        access_token = create_access_token(identity=admin.email)
        data = {
            "access_token": access_token,
            "admin": admin.serialize()
        }
        return jsonify(data), 200
    else: 
        return jsonify({"msg": "Email or password is incorrect"}), 401
