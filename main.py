from flask import Flask, render_template
from testlibfile import testlib

app = Flask(__name__)
#"{{url_for('static', filename='images/r2.png')}}"

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
            break

    return render_template('productpage.html', item=target_item)




#makes it run, niet nodig tho  'flask --app main run' kan ook
app.run(host='0.0.0.0', port=81)
