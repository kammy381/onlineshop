from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import ProductForm, UserForm, LoginForm, SearchForm
from flask_ckeditor import CKEditor



app = Flask(__name__)

#rich text editor init
ckeditor = CKEditor(app)

env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db = SQLAlchemy(app)

from models import Products, Users, Carts, Cart_items


#login magic
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            #check password
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash('You have successfully logged in!')
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password!")
        else:
            flash("That user doesn't exist!")
    return render_template('login.html', form=form)

@app.route('/logout', methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('index'))

@app.route('/dashboard', methods=["GET","POST"])
@login_required
def dashboard():

    return render_template('dashboard.html')


@app.route("/createuser", methods=['GET','POST'])
def user_form():
    username = None
    email = None
    password_hash = None
    address = None
    postal_code = None
    city = None
    country = None

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

            form.username.data = ''
            form.email.data = ''
            form.password_hash.data = ''
            form.address.data = ''
            form.postal_code.data = ''
            form.city.data = ''
            form.country.data = ''

            flash("Great Succes!  Account created succesfully")
            return redirect(url_for('login'))
        else:
            flash("This email is already in use!")

    users=db.session.query(Users).all()
    return render_template('createuser.html', form=form, users=users)

@app.route('/updateuser/<int:id>', methods=['GET','POST'])   #methods=['PATCH']
@login_required
def update_user(id):
    form = UserForm()
    thing_to_update= Users.query.get_or_404(id)
    user_id = current_user.id
    if user_id == thing_to_update.id or user_id==19: #adminkammy:
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
    if user_id == user_to_delete.id or user_id==19: #adminkammy:
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User deleted!")
            users = db.session.query(Users).all()
            return render_template('createuser.html', form=form, users=users)
        except:
            flash('Something went wrong!')
            return render_template('createuser.html', form=form, users=users)
    else:
        flash('You can only delete your own user!')
        products = db.session.query(Products).all()
        return render_template('index.html', products=products)


@app.route("/addproduct", methods=['GET','POST'])
@login_required
def product_form():
    name = None
    price = None
    image_url = None
    description = None

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

        form.name.data = ''
        form.price.data = ''
        form.image_url.data = ''
        form.description.data = ''

        flash("Great Succes!  Product submitted succesfully")

    return render_template('addproduct.html', form=form)
@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
@login_required
def update_product(id):
    form = ProductForm()
    thing_to_update= Products.query.get_or_404(id)
    user_id = current_user.id
    if user_id == thing_to_update.user.id or user_id==19: #adminkammy
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
    if user_id == product_to_delete.user.id or user_id==19: #adminkammy:
        try:

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
    #order by something?
    page = request.args.get('page', 1, type=int)

    products = Products.query.order_by(Products.updated_at).paginate(page=page, per_page=8)
    #products=Products.query.order_by(Products.updated_at)
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
@login_required
def shoppingcart():
    cart_check = db.session.query(Carts).filter(Carts.user_id == current_user.id).first()
    if cart_check:
        cart_items = db.session.query(Cart_items).filter(Cart_items.cart_id == cart_check.id).order_by(Cart_items.created_at).all()
        price=0
        for item in cart_items:
            price+= (item.product.price * item.quantity)
        return render_template('shoppingcart.html', cart_items=cart_items , total_price=price)
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


    # cart_item_to_change = Cart_items.query.get_or_404(item_id)
    # cart_item_to_change.quantity=quantity
    #            # update database
    # if request.method == 'POST':
    #     try:
    #         db.session.add(cart_item_to_change)
    #         db.session.commit()
    #     except:
    #         flash('something went wrong')
    #
    #     cart_check = db.session.query(Carts).filter(Carts.user_id == current_user.id).first()
    #     if cart_check:
    #         cart_items = db.session.query(Cart_items).filter(Cart_items.cart_id == cart_check.id).all()
    #         return render_template('shoppingcart.html', cart_items=cart_items)
    #     else:
    #         return render_template('shoppingcart.html')


def cart_item(product_id,cart_id):
    #add updated_at whole cart
    quantity=1
    created_at = datetime.now()
    updated_at = datetime.now()
    cart_item = Cart_items(product_id,cart_id,quantity,created_at,updated_at)
    db.session.add(cart_item)
    db.session.commit()

@app.route("/productpage/<string:target_id>/add_to_cart")
@login_required #for now
def add_to_cart(target_id):
    product = db.session.query(Products).filter(Products.id == target_id).first()

    #check if cart for the user exists
    cart_check=db.session.query(Carts).filter(Carts.user_id==current_user.id).first()

    #no cart with current user id?  create new one, else use the existing one
    if cart_check is None:
        full_name= 'fullname'
        user_id = current_user.id
        created_at = datetime.now()
        updated_at = datetime.now()
        cart=Carts(full_name,user_id,created_at,updated_at)
        db.session.add(cart)
        db.session.commit()
    else:
        cart=cart_check

    cart_id=cart.id

    if product is None:
        return render_template('error.html')
    else:
        #check if item is in cart_items and if that cart_item is in your cart
        item_already_in_cart = db.session.query(Cart_items).filter(Cart_items.product_id == target_id, Cart_items.cart_id == cart_id ).first()
        if item_already_in_cart:
            flash("product already in cart")
            return redirect(url_for('show_detail', target_id=product.id))
        else:
            cart_item(product_id=product.id,cart_id=cart_id)
            flash(f'{product.name} has been added to your cart')
            return redirect(url_for('show_detail', target_id=product.id))

@app.route("/shoppingcart/<string:item_id>/delete_from_cart")
@login_required #for now
def delete_from_cart(item_id):

    cart_check = db.session.query(Carts).filter(Carts.user_id == current_user.id).first()
    #don't need to check if cart exists, because you don't have a delete button in an empty cart

    item_to_delete = Cart_items.query.get_or_404(item_id)
    item_to_delete.cart.updated_at = datetime.now()
    if cart_check.id == item_to_delete.cart_id:
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
            cart_items = db.session.query(Cart_items).filter(Cart_items.cart_id == cart_check.id).all()
            return render_template('shoppingcart.html', cart_items=cart_items)
    else:
        flash("Not your product! You can't remove this one!")
        cart_items = db.session.query(Cart_items).filter(Cart_items.cart_id == cart_check.id).all()
        return render_template('shoppingcart.html', cart_items=cart_items)



#passing stuff to layout html page
@app.context_processor
def passthrough():
    form= SearchForm()
    return dict(form=form)

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

        return render_template('productpage.html', product=product)


#errors
@app.errorhandler(404)
def page_not_found(anything):
    return render_template('error.html')

if __name__ == '__main__':
    app.run()



#app.run(host='0.0.0.0', port=81)
