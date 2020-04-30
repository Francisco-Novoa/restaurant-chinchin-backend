from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255), nullable = True)
    email = db.Column(db.String(255), unique=True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = True)
    phone = db.Column(db.Integer, nullable = False)
    order= db.relationship("Orders", backref='order_user', cascade = 'all, delete')

    def __repr__(self):
        return 'User %r' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
        }

class Restaurantuser(db.Model):
    __tablename__ = 'restaurantusers'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255), unique=True, nullable = True)
    email = db.Column(db.String(255), unique=True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = True)
    phone = db.Column(db.Integer, nullable = False)
    address = db.Column(db.String(255), nullable = True)
    product= db.relationship("Product", cascade = 'all, delete', backref="product")
    order= db.relationship("Orders",  backref='order_restaurant', cascade = 'all, delete')

    def __repr__(self):
        return 'Restaurantuser %r' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
        }
    
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255), nullable = True)
    email = db.Column(db.String(255), unique=True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = True)

    def __repr__(self):
        return 'Admin %r' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }

class Product(db.Model):
    __tablename__ = 'product'
    id_product = db.Column(db.Integer,primary_key = True)
    name_product = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255))
    photo=db.Column(db.String(255), default="empty.png")
    price = db.Column(db.Float, nullable = False)
    id_restaurant = db.Column(db.Integer, db.ForeignKey("restaurantusers.id"))
    order_details= db.relationship("Orders_details", backref='order_details_product', cascade = 'all, delete')

    def __repr__(self):
        return 'Product %r' % self.name_product

    def serialize(self):
        
        return{
            'id_product': self.id_product,
            'name_product': self.name_product,
            'description': self.description,
            'price': self.price,
            'id_restaurant': self.id_restaurant,
        }

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id_ingredinet = db.Column(db.Integer,primary_key = True)
    name_ingredinet = db.Column(db.String(100), nullable = True)
    price = db.Column(db.Float, nullable = False)
    id_product = db.Column(db.Integer, db.ForeignKey('product.id_product'))

    def __repr__(self):
        return 'Ingredient %r' % self.name_ingredient

    def serialize(self):
        return{
            'id_ingredient': self.id_ingredient,
            'name_ingredient': self.name_ingredient,
            'price': self.price,
            "id_product": self.id_product
        }

class Orders(db.Model):
    __tablename__ = 'order'
    id_order = db.Column(db.Integer,primary_key = True)
    date = db.Column(db.DateTime, default=datetime.datetime.today())
    total = db.Column(db.Integer )
    comment = db.Column(db.String(500), nullable = True)
    done = db.Column(db.Boolean, default=False)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_name=db.Column(db.String(100))
    user_phone=db.Column(db.String(100))
    id_restaurant = db.Column(db.Integer, db.ForeignKey("restaurantusers.id"))
    order_details= db.relationship("Orders_details", backref ='order_details_order', cascade = 'all, delete')


    def __repr__(self):
        return 'Order %r' % self.id_order

    def serialize(self):
        return{
            'id_order': self.id_order,
            'date': self.date,
            'total': self.total,
            "comment": self.comment,
            "id_user": self.id_user,
            "user_name":self.user_name,
            "user_phone": self.user_phone,
            "done":self.done,
            "id_restaurant": self.id_restaurant
        }

class Orders_details(db.Model):
    __tablename__ = 'order_details'
    id_order_detail = db.Column(db.Integer,primary_key = True)
    amount = db.Column(db.Integer)
    product_name = db.Column(db.String(100))
    product_price = db.Column(db.String(100))
    id_product = db.Column(db.Integer, db.ForeignKey("product.id_product"))
    id_order = db.Column(db.Integer, db.ForeignKey("order.id_order"))
    def __repr__(self):
        return 'Order details %r' % self.id_order_detail

    def serialize(self):
        return{
            'id_order_detail': self.id_order_detail,
            'amount': self.amount,
            "product_name": self.product_name,
            "product_price":self.product_price,
            'id_product': self.id_product,
            'id_order': self.id_order,
        }
