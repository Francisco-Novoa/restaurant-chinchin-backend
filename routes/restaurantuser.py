from flask import Blueprint, request, jsonify
from models import db, Restaurantuser
from flask_bcrypt import Bcrypt
from flask_jwt_extended import(
    jwt_required, create_access_token, create_access_token
)
bcrypt = Bcrypt()
route_restaurantusers = Blueprint('route_restaurantusers', __name__)
# yana
@route_restaurantusers.route('/restaurantusers', methods=['GET'])
@route_restaurantusers.route('/restaurantusers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def restaurantusers(id=None):
    if request.method == 'GET':
        if id is not None:
            restaurantuser = Restaurantuser.query.get(id)
            if restaurantuser:
                return jsonify(restaurantuser.serialize()), 200
            else:
                return jsonify({"restaurantuser": "Not found"}), 404
        else:
            restaurantusers = Restaurantuser.query.all()
            restaurantusers = list(
                map(lambda restaurantuser: restaurantuser.serialize(), restaurantusers))
            return jsonify(restaurantusers), 200

    if request.method == 'PUT':
        restaurantuser = Restaurantuser.query.get(id)
        restaurantuser.name = request.json.get('name')
        restaurantuser.phone = request.json.get('phone')
        restaurantuser.address = request.json.get('address')

        db.session.commit()

        return jsonify(restaurantuser.serialize()), 200

    if request.method == 'DELETE':
        restaurantuser = Restaurantuser.query.get(id)
        db.session.delete(restaurantuser)
        db.session.commit()

        return jsonify({'restaurantuser': 'Deleted'}), 200


@route_restaurantusers.route('/restaurantlogin', methods=['POST'])
def login():
    email = request.json.get('email')
    password_hash = request.json.get('password_hash')
    if not email:
        return jsonify({"msg": "You need insert your email"}), 422
    if not password_hash:
        return jsonify({"msg": "You need insert your password"}), 422
    restaurantuser = Restaurantuser.query.filter_by(email=email).first()
    if not restaurantuser:
        return jsonify({"msg": "Email is not correct"}), 404
    pw_hash = bcrypt.generate_password_hash(password_hash)
    if bcrypt.check_password_hash(restaurantuser.password_hash, password_hash):
        access_token = create_access_token(identity=restaurantuser.email)
        data = {
            "access_token": access_token,
            "restaurantuser": restaurantuser.serialize()
        }
        return jsonify(data), 200
    else:
        return jsonify({"msg": "Email or password is not correct"}), 401


@route_restaurantusers.route('/restaurantregistration', methods=['POST'])
def registerrestaurant():
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
    restaurantuser = Restaurantuser.query.filter_by(email=email).first()
    if restaurantuser:
        return jsonify({"msg": "This email already exist"}), 422
    restaurantuser = Restaurantuser()
    restaurantuser.email = email
    restaurantuser.name = name
    restaurantuser.phone = phone
    restaurantuser.password_hash = bcrypt.generate_password_hash(password_hash)
    db.session.add(restaurantuser)
    db.session.commit()
    if bcrypt.check_password_hash(restaurantuser.password_hash, password_hash):
        access_token = create_access_token(identity=restaurantuser.email)
        data = {
            "access_token": access_token,
            "restaurantuser": restaurantuser.serialize()
        }
        return jsonify(data), 200
    else:
        return jsonify({"msg": "Email or password is incorrect"}), 401



