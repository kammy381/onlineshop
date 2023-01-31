from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import ProductForm, UserForm, LoginForm, SearchForm
from flask_ckeditor import CKEditor
from mollie.api.client import Client


app = Flask(__name__)

#rich text editor init
ckeditor = CKEditor(app)

#env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
env_config = os.getenv("APP_SETTINGS", "config.ProductionConfig")
app.config.from_object(env_config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

from models import Products, Users, Carts, Cart_items, Orders,Order_lines, Payments


#login magic
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'


#mollie
mollie_key=os.getenv("MOLLIE_KEY")
mollie_client = Client()
mollie_client.set_api_key(mollie_key)

####need normal url    get_public_url()
PUBLIC_URL = 'https://bffa-2a02-a46e-fa6f-1-b1c7-b2d5-b338-75a7.eu.ngrok.io'

#admin  it's just user id=1 from db, needs to be sent to each site that checks for admin in template
admin=1


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

def check_cart(user):
    # old cart check
    cart_check = db.session.query(Carts).filter(Carts.user_id == current_user.id).first()

    # if there is a not logged in cart, it gets attached to your account, old one from account gets deleted
    if 'cart' in session:
        cartnumber = session['cart']

        # delete old cart,  and delete cartless items
        if cart_check:
            oldcart = Carts.query.get_or_404(cart_check.id)
            db.session.delete(oldcart)
            old_cart_items = db.session.query(Cart_items).filter(Cart_items.cart_id == None).all()
            for item in old_cart_items:
                db.session.delete(item)

        # replace with new one
        cart = Carts.query.get_or_404(cartnumber)

        cart.user_id = user.id
        db.session.add(cart)
        db.session.commit()
    else:
        # if there was none in session add existing one if there is one
        if cart_check:
            session['cart'] = cart_check.id
        else:
            pass

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if not user:
            flash("That user doesn't exist!")

        # correct user
        else:
            # check password
            if not check_password_hash(user.password_hash, form.password.data):
                flash("Wrong password!")

            # correct password
            else:

                login_user(user)
                check_cart(user)

                flash('You have successfully logged in!')
                return redirect(url_for('dashboard'))


    return render_template('login.html', form=form)

@app.route('/logout', methods=["GET","POST"])  #,"POST" can go?
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('index'))

@app.route('/dashboard', methods=["GET","POST"])
@login_required
def dashboard():
    orders= Orders.query.filter(Orders.user_id == current_user.id).order_by(Orders.updated_at.desc())

    #this is a list of orderlists
    order_list=[]
    for order in orders:
        order_items= Order_lines.query.filter(Order_lines.order_id==order.id).order_by(Order_lines.updated_at).all()
        order_list.append(order_items)

    return render_template('dashboard.html', order_items=order_list)
@app.route("/createuser", methods=['GET','POST'])
def user_form():

    form = UserForm()
    if form.validate_on_submit():
        unique_check = db.session.query(Users).filter(Users.email==form.email.data).first()
        if unique_check is None:
            username = form.username.data
            email = form.email.data
            password_hash = generate_password_hash(form.password_hash.data, "sha256")
            address = form.address.data
            postal_code = form.postal_code.data
            city = form.city.data
            country = form.country.data
            created_at=datetime.now()
            updated_at=datetime.now()

            user = Users(username, email, password_hash, address, postal_code, city, country, created_at, updated_at)
            db.session.add(user)
            db.session.commit()

            flash("Great Succes!  Account created succesfully")
            return redirect(url_for('login'))
        else:
            flash("This email is already in use!")

    return render_template('createuser.html', form=form)
@app.route('/updateuser/<int:id>', methods=['GET','POST'])   #methods=['PATCH']
@login_required
def update_user(id):
    form = UserForm()
    thing_to_update= Users.query.get_or_404(id)
    user_id = current_user.id
    if user_id == thing_to_update.id or user_id==admin:
        if request.method =='POST':
            thing_to_update.username=request.form['username']
            thing_to_update.email=request.form['email']
            thing_to_update.password_hash = generate_password_hash(form.password_hash.data, "sha256")
            thing_to_update.address = request.form['address']
            thing_to_update.postal_code = request.form['postal_code']
            thing_to_update.city = request.form['city']
            thing_to_update.country = request.form['country']
            thing_to_update.updated_at = datetime.now()
            try:
                db.session.commit()
                flash("Userprofile updated!")
                return render_template('updateuser.html', form=form, thing_to_update=thing_to_update, id=id)
            except:
                flash("Something went wrong :(")
                return render_template('updateuser.html', form=form, thing_to_update=thing_to_update, id=id)
        else:
            return render_template('updateuser.html', form=form, thing_to_update=thing_to_update, id=id)
    else:
        flash("You can only edit your own user!")
        products = db.session.query(Products).all()
        return render_template('index.html', products=products)

@app.route('/deleteuser/<int:id>') #, methods=['DELETE']
@login_required
def delete_user(id):
    user_to_delete = Users.query.get_or_404(id)
    user_id = current_user.id
    form = UserForm()
    if user_id == user_to_delete.id or user_id==admin:
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User deleted!")

            return render_template('createuser.html', form=form)
        except:
            flash('Something went wrong!')
            return render_template('createuser.html', form=form)
    else:
        flash('You can only delete your own user!')
        products = db.session.query(Products).all()
        return render_template('index.html', products=products)

@app.route("/addproduct", methods=['GET','POST'])
@login_required
def product_form():

    form = ProductForm()
    if form.validate_on_submit():
        user_id = current_user.id
        name = form.name.data
        price = form.price.data
        image_url = form.image_url.data
        description = form.description.data
        created_at=datetime.now()
        updated_at=datetime.now()

        product = Products(name,price,image_url,description,created_at,updated_at, user_id)
        db.session.add(product)
        db.session.commit()

        flash("Great Succes!  Product submitted succesfully")
        return redirect(url_for('product_form'))

    return render_template('addproduct.html', form=form)
@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
@login_required
def update_product(id):
    form = ProductForm()
    thing_to_update= Products.query.get_or_404(id)
    user_id = current_user.id
    if user_id == thing_to_update.user.id or user_id==admin:
        if form.validate_on_submit():
            thing_to_update.name=form.name.data
            thing_to_update.price=form.price.data
            thing_to_update.image_url=form.image_url.data
            thing_to_update.description=form.description.data
            thing_to_update.updated_at = datetime.now()

            #update database

            db.session.add(thing_to_update)
            db.session.commit()
            flash("Product updated!")
            return redirect(url_for('show_detail', target_id=thing_to_update.id))
        form.name.data = thing_to_update.name
        form.price.data= thing_to_update.price
        form.image_url.data=thing_to_update.image_url
        form.description.data=thing_to_update.description
        return render_template('updateproduct.html', form=form, thing_to_update=thing_to_update)
    else:
        flash("Not your product, you can't edit this one!")
        products = db.session.query(Products).all()
        return render_template('index.html', products=products)

@app.route('/deleteproduct/<int:id>')
@login_required
def delete_product(id):
    product_to_delete = Products.query.get_or_404(id)
    user_id = current_user.id
    if user_id == product_to_delete.user.id or user_id==admin:
        try:
############ delete from cart_items and from orderlines#################################################################
            db.session.delete(product_to_delete)
            db.session.commit()
            flash("Product deleted!")
            products = db.session.query(Products).all()
            return render_template('index.html', products=products)
        except:
            flash('Something went wrong!')
            products = db.session.query(Products).all()
            return render_template('index.html', products=products)
    else:
        flash("Not your product! You can't delete this one!")
        products = db.session.query(Products).all()
        return render_template('index.html', products=products)

@app.route("/")
def index():
    #ordered by update date
    page = request.args.get('page', 1, type=int)

    products = Products.query.order_by(Products.updated_at).paginate(page=page, per_page=8)
    return render_template('index.html', products=products)
@app.route("/howtosolve")
def how_to_solve():
    return render_template('howtosolve.html')

@app.route("/timer")
def timer():
    return render_template('timer.html')

@app.route("/aboutme")
def about_me():
    return render_template('aboutme.html')

@app.route("/shoppingcart")
def shoppingcart():

    if 'cart' in session:
        cartnumber = session['cart']
        cart_items = db.session.query(Cart_items).filter(Cart_items.cart_id == cartnumber).order_by(Cart_items.created_at).all()
        price = 0
        for item in cart_items:
            price += (item.product.price * item.quantity)
        return render_template('shoppingcart.html', cart_items=cart_items, total_price=price)
    else:
        return render_template('shoppingcart.html')

@app.route('/change_quantity/<int:id>', methods=['GET','POST'])
def change_quantity(id):

    cart_item_to_change = Cart_items.query.get_or_404(id)

    if request.method == 'POST':
        #there is no 'webform' for this
        quantity= request.form["quantity"]
        #update cart and item
        cart_item_to_change.cart.updated_at=datetime.now()

        cart_item_to_change.updated_at=datetime.now()
        cart_item_to_change.quantity = quantity

        try:
            db.session.add(cart_item_to_change)
            db.session.commit()

            return redirect(url_for('shoppingcart'))
        except:
            flash("something went wrong")
            return redirect(url_for('shoppingcart'))

    else:
        flash('something went wrong')
        return redirect(url_for('shoppingcart'))

def cart_item(product_id,cart_id):

    quantity=1
    created_at = datetime.now()
    updated_at = datetime.now()
    #create cart_item
    cart_item = Cart_items(product_id,cart_id,quantity,created_at,updated_at)
    #update cart
    cart=Carts.query.get_or_404(session['cart'])
    cart.updated_at = datetime.now()

    db.session.add(cart)
    db.session.add(cart_item)
    db.session.commit()

@app.route("/productpage/<string:target_id>/add_to_cart")
def add_to_cart(target_id):
    #user is logged in
    if not current_user.is_anonymous:
        cart_check = db.session.query(Carts).filter(Carts.user_id == current_user.id).first()
        #user already has a cart
        if cart_check:
            cartnumber=cart_check.id

        #user doesn't have a cart, let's make one
        else:
            full_name= None
            user_id = current_user.id
            created_at = datetime.now()
            updated_at = datetime.now()
            cart=Carts(full_name,user_id,created_at,updated_at)
            db.session.add(cart)
            db.session.commit()

            cartnumber = cart.id

        # add that cartnr to session
        session['cart'] = cartnumber

    #user is not logged in
    else:
        #already has a cart
        if 'cart' in session:
            cartnumber=session['cart']
        #create a cart
        else:
            full_name = None
            user_id = None
            created_at = datetime.now()
            updated_at = datetime.now()
            cart=Carts(full_name,user_id,created_at,updated_at)
            db.session.add(cart)
            db.session.commit()

            session["cart"]=cart.id

            cartnumber=session['cart']


    product = db.session.query(Products).filter(Products.id == target_id).first()

    if product is None:
        return render_template('error.html')
    else:
        #check if item is in cart_items and if that cart_item is in your cart
        item_already_in_cart = db.session.query(Cart_items).filter(Cart_items.product_id == target_id, Cart_items.cart_id == cartnumber).first()
        if item_already_in_cart:
            flash("product already in cart")
            return redirect(url_for('show_detail', target_id=product.id))
        else:
            cart_item(product_id=product.id,cart_id=cartnumber)
            flash(f'{product.name} has been added to your cart')
            return redirect(url_for('show_detail', target_id=product.id))

@app.route("/shoppingcart/<string:item_id>/delete_from_cart")
def delete_from_cart(item_id):

    #your session cart
    cart_id=session['cart']
    item_to_delete = Cart_items.query.get_or_404(item_id)
    item_to_delete.cart.updated_at = datetime.now()
    if item_to_delete.cart_id == cart_id:
        try:
            # update cart
            db.session.add(item_to_delete)

            #delete item
            db.session.delete(item_to_delete)

            db.session.commit()
            flash("Product removed from cart!")

            return redirect(url_for('shoppingcart'))
        except:
            flash('Something went wrong!')
            return redirect(url_for('shoppingcart'))
    else:
        flash("Not your product! You can't remove this one!")
        return redirect(url_for('shoppingcart'))


#passing searchbar to layout html page
@app.context_processor
def passthrough_searchbar():
    form= SearchForm()
    return dict(form=form)

#passing cartitem amount to layout html page
@app.context_processor
def passthrough_cart():

    if 'cart' in session:
        cartnumber = session['cart']
        cart_items = db.session.query(Cart_items).filter(Cart_items.cart_id == cartnumber).all()
        amount = 0
        for item in cart_items:
            amount += item.quantity
    else:
        amount=0

    return dict(amount=amount)

@app.route('/search', methods=['POST'])
def search():
    form= SearchForm()
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        #paginate or redirect index
        product_searched = form.searched.data

        products= Products.query.filter(Products.name.ilike('%' + product_searched + '%')).order_by(Products.updated_at).paginate(page=page, per_page=8)

        return render_template('index.html',form=form, products=products)
    return render_template('index.html', form=form, products = Products.query.order_by(Products.updated_at).paginate(page=page, per_page=8))

@app.route("/productpage/<string:target_id>")
def show_detail(target_id):
    product = db.session.query(Products).filter(Products.id==target_id).first()
    if product is None:
        return render_template('error.html')
    else:

        return render_template('productpage.html', product=product, admin=admin)

def order_line(order_id):
    cart=session['cart']

    cart_items = db.session.query(Cart_items).filter(Cart_items.cart_id == cart).all()
    for cart_item in cart_items:

        orderline=Order_lines(
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price_per_unit=cart_item.product.price,
            order_id=order_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
            )
        db.session.add(orderline)

    db.session.commit()

def payment_fl(order_id,user_id):

    ordered_items = db.session.query(Order_lines).filter(Order_lines.order_id == order_id).all()
    price = 0
    for item in ordered_items:
        price += (item.price_per_unit * item.quantity)

    #total price needs to be 2decimals for mollie
    price='{0:.2f}'.format(price)
    payment= Payments(
        amount=price,
        order_id=order_id,
        user_id=user_id,
        status='succeeded',
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.session.add(payment)
    db.session.commit()

    return price


@app.route("/shoppingcart/order")
def order():
    if 'cart' in session:

        full_name='get from form'

        #user not logged in
        if current_user.is_anonymous:
            user_id=None
        #user logged in
        else:
            user_id=current_user.id

        created_at=datetime.now()
        updated_at=datetime.now()

        order=Orders(full_name=full_name,user_id=user_id,created_at=created_at,updated_at=updated_at)

        db.session.add(order)
        db.session.commit()

        #creates order_lines after order has been made
        order_line(order.id)

        #creates a payment and return price
        price=payment_fl(order.id,user_id)


        #mollie create payment
        payment = mollie_client.payments.create({
            'amount': {
                'currency': 'EUR',
                'value': f'{price}'
            },
            'description': 'Thank you for shopping with us :)',
            'redirectUrl': f'{PUBLIC_URL}/shoppingcart/order/{order.id}',
            'webhookUrl': f'{PUBLIC_URL}/mollie-webhook/',
            'metadata': {"webshop_order_id": str(order.id)},
        })

        print(payment.id)
        print(payment.status)

        # also make a thing to pull fullname and maybe add bank number########
#

        #delete cart after payment is done, need to replace
        cart = db.session.query(Carts).filter(Carts.id == session['cart']).first()
        #delete cart from db
        db.session.delete(cart)
        db.session.commit()
        #delete cart from session
        session.pop('cart')


        ###

        # if user_id is not None:
        #     flash('Order successful! You can view your order in your dashboard')
        # else:
        #     flash("Order successful!")
        #return redirect(url_for('index'))
        return redirect(payment.checkout_url)
    else:
        return redirect(url_for('index'))

@app.route("/shoppingcart/order/<id>")
def order_view(id):
    order_items = Order_lines.query.filter(Order_lines.order_id == id).order_by(Order_lines.updated_at).all()

    return render_template('orderview.html', order_items=order_items)

#errors
@app.errorhandler(404)
def page_not_found(anything):
    return render_template('error.html')

if __name__ == '__main__':
    app.run()

