from flask import Blueprint, request, jsonify
from models import db, Product

route_product = Blueprint('route_product', __name__)

@route_product.route('/product', methods = ['GET'])
def get_all_product():
    _product = Product.query.all()
    _product = list(map(lambda product: product.serialize(), _product))
    return jsonify(_product), 200

@route_product.route('/product', methods = ['POST'])
def post_product():
    if not request.is_json:
        return jsonify({'msg':'JSON Requerido'}), 400

    _name_product = request.json.get('name_product', None)
    _description = request.json.get('description', None)
    _price = request.json.get('price', None)

    if not _name_product and _name_product == '':
        return jsonify({'msg':'Field name product is required'}), 400
    if not _price and _price == '':
        return jsonify({'msg':'Field price is required'}), 400

    _product = Product()
    _product.name_product = _name_product
    _product.description = _description
    _product.price = _price

    db.session.add(_product)
    db.session.commit()
    return jsonify({'msg':'registrado', 'restul':_product.serialize()}), 201

@route_product.route('/product/<int:id>', methods = ['GET'])
def get_product(id):
    return jsonify({'msg':'Method Get id'}), 200

@route_product.route('/product/<int:id>', methods = ['PUT'])
def put_product(id):
    return jsonify({'msg':'Method PUT'}), 200

@route_product.route('/product/<int:id>', methods = ['DELETE'])
def delete_product(id):
    return jsonify({'msg':'Method DELETE'}), 200