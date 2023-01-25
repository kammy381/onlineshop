from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#alleen nodig voor json in column    db.Column(JSON)
from sqlalchemy.dialects.postgresql import JSON


class Products(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(2000))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    #posted by
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    ##
    cart_items = db.relationship('Cart_items', backref='product')
    order_lines = db.relationship('Order_lines', backref='product')

    #runs when we create a new one
    def __init__(self, name, price, image_url, description, created_at, updated_at, user_id):

        self.name = name
        self.price = price
        self.image_url = image_url
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.user_id = user_id


    #represents object when we query for it
    def __repr__(self):
        return '<id {}>'.format(self.id)

class Cart_items(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
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
        return '<id {}>'.format(self.id)


class Carts(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    cart_items = db.relationship('Cart_items', backref='cart')


    # runs when we create a new one
    def __init__(self, full_name, user_id, created_at, updated_at):

        self.full_name = full_name
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at



    # represents object when we query for it
    def __repr__(self):
        return '<id {}>'.format(self.id)

class Order_lines(db.Model):
    __tablename__ = 'order_line'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    quantity = db.Column(db.Integer)
    price_per_unit = db.Column(db.Float)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # runs when we create a new one
    def __init__(self, product_id, order_id, quantity, price_per_unit, created_at, updated_at):

        self.product_id = product_id
        self.order_id = order_id
        self.quantity = quantity
        self.price_per_unit = price_per_unit
        self.created_at = created_at
        self.updated_at = updated_at

    # represents object when we query for it
    def __repr__(self):
        return '<cart_id {}>'.format(self.cart_id)

class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    order_lines = db.relationship('Order_lines',backref='orders')
    payments = db.relationship('Payments', backref='orders', uselist=False)

    # runs when we create a new one
    def __init__(self, full_name, user_id, created_at, updated_at):

        self.full_name = full_name
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at


    # represents object when we query for it
    def __repr__(self):
        return '<oder_id {}>'.format(self.id)

class Users(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)

    address = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    products = db.relationship('Products', backref='user')
    orders = db.relationship('Orders', backref='user')
    carts = db.relationship('Carts', backref='user', uselist=False)
    payments = db.relationship('Payments', backref='user', uselist=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

    # runs when we create a new one
    def __init__(self,username, email, password_hash, address, postal_code, city, country, created_at, updated_at):

        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.address = address
        self.postal_code = postal_code
        self.city = city
        self.country = country
        self.created_at = created_at
        self.updated_at = updated_at

    # represents object when we query for it
    def __repr__(self):
        return '<id {}>'.format(self.id)

class Payments(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # runs when we create a new one
    def __init__(self, amount, order_id, user_id, status, created_at, updated_at):
        #self.id = id
        self.amount = amount
        self.order_id = order_id
        self.user_id = user_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    # represents object when we query for it
    def __repr__(self):
        return '<id {}>'.format(self.id)

