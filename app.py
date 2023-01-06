from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime



#partials html


app = Flask(__name__)


env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db = SQLAlchemy(app)

from models import Products

@app.route("/")
def index():
    products=db.session.query(Products).all() #make it so it's not all but first x
    return render_template('index.html', products=products)


@app.route("/test")
def test_site():
    return render_template('test.html')

@app.route('/submitproduct', methods=['POST'])
def submit():

    if request.method=="POST":

        name = request.form['productname']
        price = request.form['price']
        image_url = request.form['pictureurl']
        description = request.form['description']
        created_at=datetime.now()
        updated_at=datetime.now()

        product = Products(name,price,image_url,description,created_at,updated_at)
        db.session.add(product)
        db.session.commit()

        products = db.session.query(Products).all()
    return render_template('index.html',products=products)


###broken
@app.route("/productpage/<string:target_id>")
def show_detail(target_id):
    products = db.session.query(Products).all()
    for product in products:

        if product==target_id:
            target_item=product
            return render_template('productpage.html', product=target_item)
    return render_template('error.html')



#errors
@app.errorhandler(404)
def page_not_found(anything):
    return render_template('error.html')

if __name__ == '__main__':
    app.run()


#makes it run, niet nodig tho  'flask --app main run' kan ook
#app.run(host='0.0.0.0', port=81)
