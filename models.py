from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255), nullable = True)
    email = db.Column(db.String(255), unique=True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = True)
    phone = db.Column(db.Integer, nullable = False)
    isowner =db.Column(db.Boolean, default = False)

    def __repr__(self):
        return 'User %r' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'isowner': self.isowner,
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
