from flask import Blueprint, request, jsonify
from models import db, User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import(
    jwt_required, create_access_token, create_access_token
)
bcrypt = Bcrypt()
route_users = Blueprint('route_users', __name__)
#yana
@route_users.route('/users', methods = ['GET'])
@route_users.route('/users/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def users(id = None):
    if request.method == 'GET':
        if id is not None:
            user = User.query.get(id)
            if user:
                return jsonify(user.serialize()), 200
            else:
                return jsonify({"user": "Not found"}), 404
        else:
            users = User.query.all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users), 200

    if request.method == 'PUT':
        user = User.query.get(id)
        user.name = request.json.get('name')
        user.phone = request.json.get('phone')

        db.session.commit()

        return jsonify(user.serialize()), 200

    if request.method == 'DELETE':
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()

        return jsonify({'user':'Deleted'}), 200
    
    
@route_users.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password_hash = request.json.get('password_hash')
    if not email:
        return jsonify({"msg": "You need insert your email"}), 422
    if not password_hash:
        return jsonify({"msg": "You need insert your password"}), 422
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg": "Email is not correct"}), 404
    pw_hash = bcrypt.generate_password_hash(password_hash)
    if bcrypt.check_password_hash(user.password_hash, password_hash):
        access_token = create_access_token(identity=user.email)
        data = {
            "access_token": access_token,
            "user": user.serialize()
        }
        return jsonify(data), 200
    else: 
        return jsonify({"msg": "Email or password is not correct"}), 401
        
@route_users.route('/registration', methods=['POST'])
def register():
    email = request.json.get('email')
    name = request.json.get('name')
    phone = request.json.get('phone')
    password_hash = request.json.get('password_hash')
    if not email:
        return jsonify({"msg": "You need to write yor email"}), 422
    if not name:
        return jsonify({"msg": "You need to write your name"}), 422  
    if not phone:
        return jsonify({"msg": "You need to write your phone"}), 422           
    if not password_hash:
        return jsonify({"msg": "You need to write your password_hash"}), 422
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"msg": "This email already exist"}), 422
    user = User()
    user.email = email
    user.name = name
    user.phone = phone
    user.password_hash = bcrypt.generate_password_hash(password_hash)
    db.session.add(user)
    db.session.commit()
    if bcrypt.check_password_hash(user.password_hash, password_hash):
        access_token = create_access_token(identity=user.email)
        data = {
            "access_token": access_token,
            "user": user.serialize()
        }
        return jsonify(data), 200
    else: 
        return jsonify({"msg": "Email or password is incorrect"}), 401
