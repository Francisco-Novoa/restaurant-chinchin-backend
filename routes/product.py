from flask import Blueprint, request, jsonify
from models import db, Product
from libs.functions import allowed_file

route_product = Blueprint('route_product', __name__)

@route_product.route('/product', methods = ['GET'])
def get_all_product():
    _product = Product.query.all()
    _product = list(map(lambda product: product.serialize(), _product))
    return jsonify(_product), 200

@route_product.route('/product', methods = ['POST'])
def post_product():
    _name_product = request.json.get('name_product')
    _description = request.json.get('description')
    _price = request.json.get('price')
    id_restaurant = request.json.get("id_restaurant")
    if not _name_product or _name_product == '':
        return jsonify({'msg':'Field name product is required'}), 400
    if not _price or _price == '':
        return jsonify({'msg':'Field price is required'}), 400
    if not id_restaurant or id_restaurant == '':
        return jsonify({'msg':'Field restaurant_id is required'}), 400
    _product = Product()
    _product.name_product = _name_product
    _product.description = _description
    _product.id_restaurant = id_restaurant
    _product.price = _price
    db.session.add(_product)
    db.session.commit()
    return jsonify({"msg":"producto registrado"}), 200

@route_product.route('/product/<int:id>', methods = ['GET'])
def get_product(id):
    _product = Product.query.get(id)
    if not _product:
        return jsonify({'msg':'Product not found'})
    return jsonify(_product.serialize()), 200

@route_product.route('/product/from/<int:id>', methods=['GET'])
def get_all_products_of(id):
    def allofthem(elem):
        diccionario=elem.serialize()
        diccionario["id_restaurant"]=id
        return diccionario
    _products = Product.query.filter_by(id_restaurant=id).all()
    _product = list(map(allofthem, _products))
    return jsonify(_product), 200

@route_product.route('/product/<int:id>', methods = ['PUT'])
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

@route_product.route('/product/<int:id>', methods = ['DELETE'])
def delete_product(id):
    _product = Product.query.get(id)
    if not _product:
        return jsonify({'msg':'Product not found'}), 404

    db.session.delete(_product)
    db.session.commit()
    
    return jsonify({'msg':'Product deleted'})


"""  
@route_product.route('/product/upload/<int:id>', methods = ['POST'])
def upload(id):
    _product = Product.query.get(id)
    if not _product:
        return jsonify({'msg':'Product not found'}), 404
    if "file" not in request.files:
        return {"msg": "file required"}
    photo=request.file["photo"]
    if file.filename=="":
        return {"msg": "no selected file"}
    
    db.session.delete(_product)
    db.session.commit()
    
    return jsonify({'msg':'Product deleted'})
     """
    
