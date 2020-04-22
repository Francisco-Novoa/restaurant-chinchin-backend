from flask import Blueprint, request, jsonify
from models import db, Orders, Orders_details, Product, Restaurantuser, User

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
"""
{
    "user_id":"id",
    "restaurant_id" : "id2",
    "comment":"comment_text",
    "productos":"["product_id1 , amount",]
}
"""
@route_orders("neworder", methods=["POST"])
def neworder():
    id_user=request.json.get("user_id")
    id_restaurant=request.json.get("restaurant_id")
    comment=request.json.get("comment")
    productos=request.json.get("productos")

    if not id_user:
        return {"msg": "user id missing"}, 422
    
    if not id_restaurant:
        return {"msg": "restaurant id missing"}, 422
    
    if not productos:
        return {"msg": "you need atleast one product"}, 422

    #making the parent order

    order=Orders()
    order.id_user=id_user
    order.id_restaurant=id_restaurant
    if comment:
        order.comment=comment
    order.total=0
    db.session.add(order)
    db.session.commit()

    ### making the detail

    for producto in productos:
        fetched_product = Product.query.filter_by(id=producto[0]).first()
        if fetched_product:
            details=Orders_details()
            details.amount=producto[1]
            details.total=fetched_product.price
            details.id_product=producto[0]
            details.id_order=order.id_order
            db.session.add(details)
            db.session.commit()
        else:
            return {"msg": "product id not found"}, 404
    
    return {"msg": "transaccion registered successfully"}, 200
    




