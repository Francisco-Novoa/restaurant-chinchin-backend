from flask import Blueprint, request, jsonify
from models import db, Ingredient

route_ingredient = Blueprint('route_ingredient', __name__)

@route_ingredient.route('/ingredient', methods = ['GET'])
def get_all_ingredient():
    _ingredient = Ingredient.query.all()
    _ingredient = list(map(lambda ingredient: ingredient.serialize(), _ingredient))
    return jsonify(_ingredient), 200

@route_ingredient.route('/ingredient', methods = ['POST'])
def post_ingredient():
    if not request.is_json:
        return jsonify({'msg':'JSON Requerido'}), 400

    _name_ingredient = request.json.get('name_ingredient', None)
    _price = request.json.get('price', None)

    if not _name_ingredient and _name_ingredient == '':
        return jsonify({'msg':'Field name ingredient is required'}), 400
    if not _price and _price == '':
        return jsonify({'msg':'Field price is required'}), 400

    _ingredient = Ingredient()
    _ingredient.name_product = _name_ingredient
    _ingredient.price = _price

    db.session.add(_ingredient)
    db.session.commit()
    return jsonify({'msg':'registrado', 'restul':_ingredient.serialize()}), 201

@route_ingredient.route('/ingredient/<int:id>', methods = ['GET'])
def get_product(id):
    _product = Product.query.get(id)
    if not _product:
        return jsonify({'msg':'Product not found'})
    return jsonify(_product.serialize()), 200

@route_ingredient.route('/ingredient/<int:id>', methods = ['PUT'])
def put_product(id):
    if not request.is_json:
        return jsonify({'msg':'JSON Requerido'}), 400

    _name_product = request.json.get('name_product', None)
    _description = request.json.get('description', None)
    _price = request.json.get('price', None)

    if not _name_product and _name_product == '':
        return jsonify({'Product name':'No changes'}), 400
    if not _price and _price == '':
        return jsonify({'Price':'No changes'}), 400

    _product = Product.query.get(id)
    _product.name_product = _name_product
    _product.description = _description
    _product.price = _price

    db.session.commit()
    return jsonify({'msg':'registrado', 'restul':_product.serialize()}), 201

@route_ingredient.route('/ingredient/<int:id>', methods = ['DELETE'])
def delete_product(id):
    _product = Product.query.get(id)
    if not _product:
        return jsonify({'msg':'Product not found'}), 404

    db.session.delete(_product)
    db.session.commit()
    
    return jsonify({'msg':'Product deleted'})
    