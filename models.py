from app import db

#alleen nodig voor json in column    db.Column(JSON)
from sqlalchemy.dialects.postgresql import JSON


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)   #first int pk has automagic autoincrement
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(2000))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    #runs when we create a new one
    def __init__(self, id, name, price, image_url, description, created_at, updated_at):
        self.id = id
        self.name = name
        self.price = price
        self.image_url = image_url
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    #represents object when we query for it
    def __repr__(self):
        return '<id {}>'.format(self.id)

class Cart_items(db.Model):
    __tablename__ = 'cart_items'

    product_id = db.Column(db.Integer)   #foreignkey? + one to many    = product_Id
    cart_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    #runs when we create a new one
    def __init__(self, product_id,cart_id, quantity, created_at, updated_at):
        self.product_id = product_id
        self.cart_id = cart_id
        self.quantity = quantity
        self.created_at = created_at
        self.updated_at = updated_at

    #represents object when we query for it
    def __repr__(self):
        return '<cart_id {}>'.format(self.cart_id)


class Carts(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)   #=cart-id
    full_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer) #=1to1  user_id
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # runs when we create a new one
    def __init__(self, id, full_name, user_id, created_at, updated_at):
        self.id = id
        self.full_name = full_name
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at

    # represents object when we query for it
    def __repr__(self):
        return '<id {}>'.format(self.id)


class Order_lines(db.Model):
    __tablename__ = 'order_lines'

    product_id = db.Column(db.Integer)  #product id
    cart_id = db.Column(db.Integer)        #orders
    quantity = db.Column(db.Integer)
    price_per_unit = db.Column(db.Float)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # runs when we create a new one
    def __init__(self, product_id, cart_id, quantity, price_per_unit, created_at, updated_at):
        self.product_id = product_id
        self.cart_id = cart_id
        self.quantity = quantity
        self.price_per_unit = price_per_unit
        self.created_at = created_at
        self.updated_at = updated_at

    # represents object when we query for it
    def __repr__(self):
        return '<cart_id {}>'.format(self.cart_id)

class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)   #payment
    full_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer)  #userid
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # runs when we create a new one
    def __init__(self, id, full_name, user_id, created_at, updated_at):
        self.id = id
        self.full_name = full_name
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at

    # represents object when we query for it
    def __repr__(self):
        return '<oder_id {}>'.format(self.id)

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)   #carts, orders, payments
    email = db.Column(db.String(50))
    password = db.Column(db.String(100))  #how to hash? yt
    adress = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # runs when we create a new one
    def __init__(self, id, email, password, adress, postal_code, city, country, created_at, updated_at):
        self.id = id
        self.email = email
        self.password = password
        self.adress = adress
        self.postal_code = postal_code
        self.city = city
        self.country = country
        self.created_at = created_at
        self.updated_at = updated_at

    # represents object when we query for it
    def __repr__(self):
        return '<id {}>'.format(self.id)

class Payments(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    order_id = db.Column(db.Integer) #order id
    user_id = db.Column(db.Integer) #user id
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # runs when we create a new one
    def __init__(self, id, amount, order_id, user_id, status, created_at, updated_at):
        self.id = id
        self.amount = amount
        self.order_id = order_id
        self.user_id = user_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    # represents object when we query for it
    def __repr__(self):
        return '<id {}>'.format(self.id)

