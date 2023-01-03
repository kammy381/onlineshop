from flask import Flask, render_template
from testlibfile import testlib
from flask_sqlalchemy import SQLAlchemy
import os


#partials html


app = Flask(__name__)


env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# secret_key = app.config.get("SECRET_KEY")
# print(f"The configured secret key is {secret_key}.")
#app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

from models import Products

@app.route("/")
def index():
    return render_template('index.html',testlib=testlib)


@app.route("/test")
def test_site():
    return render_template('test.html')

@app.route("/productpage/<string:target_id>")
def show_detail(target_id):

    for item in testlib:
        if item["id"]==target_id:
            target_item=item
            return render_template('productpage.html', item=target_item)
    return render_template('error.html')



#errors
@app.errorhandler(404)
def page_not_found(anything):
    return render_template('error.html')

if __name__ == '__main__':
    app.run()


#makes it run, niet nodig tho  'flask --app main run' kan ook
#app.run(host='0.0.0.0', port=81)
