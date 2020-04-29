from flask import Blueprint, request, jsonify
import re
from models import db, Restaurantuser,Product
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
                return jsonify({"msg": "Not found"}), 404
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

        return jsonify({'msg': 'Deleted'}), 200

@route_restaurantusers.route('/restaurantbyname/<name>', methods=['GET'])
def byName(name=None):
        if name is not None:
            restaurantuser = Restaurantuser.query.filter_by(name=name).first()
            if restaurantuser:
                def allofthem(elem):
                    diccionario=elem.serialize()
                    diccionario["id_restaurant"]=id
                    return diccionario
                id=restaurantuser.id
                _products = Product.query.filter_by(id_restaurant=restaurantuser.id).all()
                _product = list(map(allofthem, _products))
                return jsonify({"restaurant":restaurantuser.serialize(),
                                "products":_product}), 200
            else:
                return jsonify({"msg": "Not found"}), 404
        else:
            return jsonify({"msg": "you must specify a name"}), 404

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
        return jsonify({"msg": "You need to write your password"}), 422
    restaurantuser = Restaurantuser.query.filter_by(email=email).first()
    if restaurantuser:
        return jsonify({"msg": "This email already exist"}), 422
    restaurantuser = Restaurantuser.query.filter_by(name=name).first()
    if restaurantuser:
        return jsonify({"msg": "This user name already exist"}), 422
    name=re.sub('\s+', '_',name)
    print(name)
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



