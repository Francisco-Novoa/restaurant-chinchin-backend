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
    order= db.relationship("Orders", backref = backref('children', cascade = 'all, delete'))

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
    name = db.Column(db.String(255), nullable = True)
    email = db.Column(db.String(255), unique=True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = True)
    phone = db.Column(db.Integer, nullable = False)
    address = db.Column(db.String(255), nullable = True)
    product= db.relationship("Product", backref = backref('children', cascade = 'all, delete'))
    order= db.relationship("Orders", backref = backref('children', cascade = 'all, delete'))

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
    description = db.Column(db.String(255), unique=True, nullable = True)
    price = db.Column(db.Float, nullable = False)
    id_restaurant = db.Column(db.Integer, db.ForeignKey("restaurantusers.id"))
    order_details= db.relationship("Orders_details", backref = backref('children', cascade = 'all, delete'))

    def __repr__(self):
        return 'Product %r' % self.name_product

    def serialize(self):
        return{
            'id_product': self.id_product,
            'name_product': self.name_product,
            'description': self.description,
            'price': self.price,
            'id_restaurant': self.restaurantusers.serialize(),
        }

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id_ingredient = db.Column(db.Integer,primary_key = True)
    name_ingredient = db.Column(db.String(100), nullable = True)
    price = db.Column(db.Float, nullable = False)
    id_product = db.Column(db.Integer, db.ForeignKey('product.id_product'))

    def __repr__(self):
        return 'Ingredient %r' % self.name_ingredient

    def serialize(self):
        return{
            'id_ingredient': self.id_ingredient,
            'name_ingredient': self.name_ingredient,
            'price': self.price,
            'id_product': self.product.serialize()
        }

class Orders(db.Model):
    __tablename__ = 'order'
    id_order = db.Column(db.Integer,primary_key = True)
    date = db.Column(db.DateTime, default=datetime.datetime.today())
    total = db.Column(db.Integer, unique=True, nullable = False)
    comment = db.Column(db.String(500), nullable = True)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"))
    id_restaurant = db.Column(db.Integer, db.ForeignKey("restaurantusers.id"))
    order_details= db.relationship("Orders_details", backref = backref('children', cascade = 'all, delete'))


    def __repr__(self):
        return 'Order %r' % self.name

    def serialize(self):
        return{
            'id': self.id_order,
            'date': self.date,
            'total': self.total,
            "comment": self.comment,
            'user': self.user.serialize(),
            'restaurant': self.restaurantusers.serialize()
        }

class Orders_details(db.Model):
    __tablename__ = 'order_details'
    id_order_detail = db.Column(db.Integer,primary_key = True)
    amount = db.Column(db.Integer)
    total = db.Column(db.Integer)
    id_product = db.Column(db.Integer, db.ForeignKey("product.id_product"))
    id_order = db.Column(db.Integer, db.ForeignKey("restaurantusers.id"))

    def __repr__(self):
        return 'Order details %r' % self.name

    def serialize(self):
        return{
            'id': self.id_order_detail,
            'amount': self.amount,
            'total': self.total,
            'id_product': self.product.serialize(),
            'id_order': self.order.serialize()
        }



""" class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=True, nullable = True)
    address = db.Column(db.String(255), nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = True)
    user = db.relationship(User, backref = backref('children', cascade = 'all, delete'))

    def __repr__(self):
        return 'Restaurant %r' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'address':self.address,
            'user': self.user.serialize(),
          
        }

class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key = True)
    dishname = db.Column(db.String(255), nullable = True)
    price = db.Column(db.Integer, nullable = True)
    ingridients = db.Column(db.String(255), nullable = True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable = True)
    restaurant = db.relationship(Restaurant, backref = backref('children', cascade = 'all, delete'))

    def __repr__(self):
        return 'Menu %r' % self.dishname

    def serialize(self):
        return{
            'id': self.id,
            'dishname': self.name,
            'price':self.price,
            'ingridients': self.ingridients,
            'restaurant': self.restaurant.serialize(),  
        } """

""" class Orderlog(db.Model):
    __tablename__ = 'orderlogs'
    id = db.Column(db.Integer, primary_key = True)
    dishes = db.Column(db.String(255), nullable = True)
    totalprice = db.Column(db.Integer, nullable = True)
    comment = db.Column(db.String(255), nullable = True)
    done =db.Column(db.Boolean, default = False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable = True)
    restaurant = db.relationship(Restaurant, backref = backref('children', cascade = 'all, delete'))
    

    def __repr__(self):
        return 'Orderlog %r' % self.dishes

    def serialize(self):
        return{
            'id': self.id,
            'dishes': self.dishes,
            'totalprice':self.totalprice,
            'comment': self.comment,
            'done': self.done, 
            'restaurant': self.restaurant.serialize(), 
        } """
