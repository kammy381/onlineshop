from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, TextAreaField, PasswordField, BooleanField,ValidationError
from wtforms.validators import DataRequired, NumberRange, URL, Email, EqualTo, Length
from wtforms.widgets import TextArea
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


app = Flask(__name__)


env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db = SQLAlchemy(app)

from models import Products, Users


#login magic
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

##form class
class ProductForm(FlaskForm):
    name = StringField("Product name:", validators=[DataRequired()])
    price = DecimalField("Price:", validators=[DataRequired(), NumberRange(min=0.01,max=99999)])
    image_url = StringField("Image url:", validators=[URL(message='wrong url')])
    description = StringField("Product description:", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password_hash = PasswordField("Password:", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match!')])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    address = StringField("Address:", validators=[DataRequired()])
    postal_code = StringField("Postalcode:", validators=[DataRequired()])
    city = StringField('City:', validators=[DataRequired()])
    country = StringField('Country:', validators=[DataRequired()])
    submit = SubmitField("Submit")



class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")


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
        else:
            flash("This email is already in use!")

    users=db.session.query(Users).all()
    return render_template('createuser.html', form=form, users=users)

@app.route('/updateuser/<int:id>', methods=['GET','POST'])
def update_user(id):
    form = UserForm()
    thing_to_update= Users.query.get_or_404(id)
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
            return render_template('updateuser.html', form=form, thing_to_update=thing_to_update)
        except:
            flash("Something went wrong :(")
            return render_template('updateuser.html', form=form, thing_to_update=thing_to_update)
    else:
        return render_template('updateuser.html', form=form, thing_to_update=thing_to_update)

@app.route('/deleteuser/<int:id>')
def delete_user(id):
    user_to_delete = Users.query.get_or_404(id)

    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted!")
        users = db.session.query(Users).all()
        return render_template('createuser.html', form=form, users=users)
    except:
        flash('Something went wrong!')
        return render_template('createuser.html', form=form, users=users)

@app.route("/addproduct", methods=['GET','POST'])
def product_form():
    name = None
    price = None
    image_url = None
    description = None

    form = ProductForm()
    if form.validate_on_submit():

        name = form.name.data
        price = form.price.data
        image_url = form.image_url.data
        description = form.description.data
        created_at=datetime.now()
        updated_at=datetime.now()

        product = Products(name,price,image_url,description,created_at,updated_at)
        db.session.add(product)
        db.session.commit()

        form.name.data = ''
        form.price.data = ''
        form.image_url.data = ''
        form.description.data = ''

        flash("Great Succes!  Product submitted succesfully")

    return render_template('addproduct.html', form=form)
@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def update_product(id):
    form = ProductForm()
    thing_to_update= Products.query.get_or_404(id)

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

    # if request.method =='POST':
    #
    #     thing_to_update.name=request.form['name']
    #     thing_to_update.price = request.form['price']
    #     thing_to_update.image_url = request.form['image_url']
    #     thing_to_update.description = request.form['description']
    #     thing_to_update.updated_at = datetime.now()
    #     try:
    #         db.session.commit()
    #         flash("Product updated!")
    #         return render_template('updateproduct.html', form=form, thing_to_update=thing_to_update)
    #     except:
    #         flash("Something went wrong :(")
    #         return render_template('updateproduct.html', form=form, thing_to_update=thing_to_update)
    # else:
    #     return render_template('updateproduct.html', form=form, thing_to_update=thing_to_update)


@app.route('/deleteproduct/<int:id>')
def delete_product(id):
    product_to_delete = Products.query.get_or_404(id)

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        flash("Product deleted!")
        products = db.session.query(Products).all()
        return render_template('index.html', products=products)
    except:
        flash('Something went wrong!')
        return render_template('index.html', products=products)

@app.route("/")
def index():
    #order by something?
    products=Products.query.order_by(Products.updated_at)
    return render_template('index.html', products=products)

@app.route("/howtosolve")
def how_to_solve():
    return render_template('howtosolve.html')

@app.route('/search', methods=['POST'])
def search():

    if request.method=="POST":
        searched=request.form['searched']


        products = db.session.query(Products).filter(Products.name.contains(searched)).all()
    return render_template('index.html',products=products)


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
