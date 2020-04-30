from flask import Blueprint, request, jsonify
from models import db, Orders, Orders_details, Product, Restaurantuser, User
from libs.functosendemail import sendMailNew

route_orders = Blueprint('route_orders', __name__)

@route_orders.route('/orders', methods=['GET'])
@route_orders.route('/orders/<int:id>', methods=['GET'])
def get_all_orders(id=None):
    if id is not None:
        order = Orders.query.get(id)
        if order:
            return jsonify(order.serialize()), 200
        else:
            return jsonify({"msg": "order nor found"}), 404
    else:
            order = Orders.query.all()
            order = list(map(lambda orders: order.serialize(), order))
            return jsonify(order), 200

@route_orders.route('/orderof/<int:id>')
def get_orders_of(id=None):
    if id is not None:
        order = Orders.query.filter_by(id_restaurant=id).all()
        if not order:
            return {"msg":"there are no orders"},200
        order = list(map(lambda orders: orders.serialize(), order))
        for x in order:
            details = Orders_details.query.filter_by(id_order=x["id_order"]).all()
            details = list(map(lambda details: details.serialize(), details))
            x["order_details"]=details
        return jsonify(order),200
    else:
        return {"msg": "order missing"}

@route_orders.route('/orderby/<int:id>')
def get_orders_by(id=None):
    if id is not None:
        order = Orders.query.filter_by(id_user=id).all()
        if not order:
            return {"msg":"there are no orders"},200
        order = list(map(lambda orders: orders.serialize(), order))
        for x in order:
            details = Orders_details.query.filter_by(id_order=x["id_order"]).all()
            details = list(map(lambda details: details.serialize(), details))
            x["order_details"]=details
        return jsonify(order),200
    else:
        return {"msg": "order missing"}

@route_orders.route("/finish/<int:id>",methods=['PUT'])
def finish (id=None):
    if not request.is_json:
        return jsonify({'msg':'JSON Requerido'}), 400
    if not id:
        return {"msg":"order not found"}
    order=Orders.query.filter_by(id_order=id).first()
    if order.done==True:
        return {"msg":"order already finished"}
    order.done=True
    db.session.commit()
    return{"msg":"ok"},200

    #small function to add the id_order and serialize
    def allofthem(elem):
                    diccionario=elem.serialize()
                    diccionario["id_order"]=order.id_order
                    return diccionario
    #return everything in an orderly fashion
    details = Orders_details.query.filter_by(id_order=order.id_order).all()
    details = list(map(allofthem, details))
    return jsonify({"order":order.serialize(),
                    "details":details}), 200  

@route_orders.route("/cancel/<int:id>",methods=['PUT'])
def cancel (id=None):
    if not request.is_json:
        return jsonify({'msg':'JSON Requerido'}), 400
    if not id:
        return {"msg":"order not found"}
    order=Orders.query.filter_by(id_order=id).first()
    if order.done==True:
        return {"msg":"order already finished"}
    order.done=None
    db.session.commit()
    return{"msg":"ok"},200

    #small function to add the id_order and serialize
    def allofthem(elem):
                    diccionario=elem.serialize()
                    diccionario["id_order"]=order.id_order
                    return diccionario
    #return everything in an orderly fashion
    details = Orders_details.query.filter_by(id_order=order.id_order).all()
    details = list(map(allofthem, details))
    return jsonify({"order":order.serialize(),
                    "details":details}), 200  

@route_orders.route("/neworder", methods=['POST'])
def new_order():
    #check if fields are there
    if not request.is_json:
        return jsonify({'msg':'JSON Requerido'}), 400
    user=request.json.get('user')
    if not user:
        return {"msg":"user input is required"}
    restaurant=request.json.get('restaurant')
    if not restaurant:
        return {"msg":"restaurant input is required"}
    product=request.json.get('product')
    if not product:
        return {"msg":"product input is required"}
    total=request.json.get('total')
    if not product:
        return {"msg":"total input is required"}
    usuario=User.query.filter_by(id=user).first()
    if not usuario:
        return {"msg": "usuario inexistente"}

    comment=request.json.get('comment')
    #add fields to sqlalchemy
    order=Orders()
    order.total=total
    order.id_restaurant=restaurant
    order.id_user=user
    order.comment=comment
    order.user_name=usuario.name
    order.user_phone=usuario.phone
    db.session.add(order)
    db.session.commit()
    
    #add each detail
    for x in product:
        detail=Orders_details()
        detail.amount=x["amount"]
        detail.id_product=x["id_product"]
        detail.product_name=x["name_product"]
        detail.product_price=x["price"]
        detail.id_order=order.id_order
        db.session.add(detail)
        db.session.commit()
        
   #small function to add the id_order and serialize
    def allofthem(elem):
                    diccionario=elem.serialize()
                    diccionario["id_order"]=order.id_order
                    return diccionario
    #return everything in an orderly fashion
    details = Orders_details.query.filter_by(id_order=order.id_order).all()
    details = list(map(allofthem, details))

    #email here!!


    user = User.query.filter_by(id=order.id_user).first()

    if not user:
        return jsonify({"msg": "This email is not registered"}), 404    
    subject = "Reservation"
    try : 
        sendMailNew("Order sent", user.email)
    except: 
        print("there is no such mail") 
    restaurant=Restaurantuser.query.filter_by(id=order.id_restaurant).first()

    if not restaurant:
        return jsonify({"msg": "This email is not registered"}), 404    
    subject = "Reservation"
    
    try : 
        sendMailNew("New Order", restaurant.email)
    except:
         print("there is no such mail") 

    return jsonify({"order":order.serialize()}),200

