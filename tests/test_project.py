from models import Products, Users, Carts, Cart_items, Orders,Order_lines, Payments

#test staticpages
def test_index(client):
    response = client.get("/")
    #b to convert t bytes
    assert b"<title>Index</title>" in response.data

def test_howtosolve(client):
    response = client.get("/howtosolve")
    #b to convert t bytes
    assert b"<title>How to solve</title>" in response.data

def test_timer(client):
    response = client.get("/timer")
    #b to convert t bytes
    assert b"<title>   Timer  </title>" in response.data

def test_aboutme(client):
    response = client.get("/aboutme")
    # b to convert t bytes
    assert b"<p>This website is a project by Kamil Romasz ;) </p>" in response.data

#test other
def test_register(client, app):
    response = client.post("/users/new", data=dict([('username', 'testuser'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'), ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]) )

    with app.app_context():

        assert Users.query.count() == 1
        assert Users.query.first().email == "testuser@hotmail.com"

def test_register_login_logout(client):
    #register
    client.post("/users/new", data=dict([('username', 'testuser'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'), ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]) )
    #go to login page
    resp1 = client.get("/login")
    assert b"<h1>Login</h1>" in resp1.data

    #login
    resp2=client.post("/login", data=dict([('username', 'testuser'), ('password', '123')]), follow_redirects=True)

    #check if user is redirected to dashboard after loging in
    assert b"<h1>Dashboard</h1>" in resp2.data

    #logout
    resp3=client.get("/logout", follow_redirects=True)

    #check if user redirected to indexpage after logging out
    assert b"<title>Index</title>" in resp3.data

def test_wronglogin(client):
    # register
    client.post("/users/new", data=dict(
        [('username', 'testuser'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'),
         ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]))

    # login wrong username
    resp2 = client.post("/login", data=dict([('username', 'wrongtestuser'), ('password', '123')]), follow_redirects=True)

    # check if user is put on the login page after entering incorrect username
    assert b"<h1>Login</h1>" in resp2.data

    # login wrong username
    resp3 = client.post("/login", data=dict([('username', 'testuser'), ('password', 'wrong123')]), follow_redirects=True)
    # check if user is put on the login page after entering incorrect password
    assert b"<h1>Login</h1>" in resp3.data

def test_register_login_delete(client, app):
    #register
    client.post("/users/new", data=dict([('username', 'testuser'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'), ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]) )

    #login
    resp1=client.post("/login", data=dict([('username', 'testuser'), ('password', '123')]), follow_redirects=True)


    #check if user in db and it it's the correct one
    with app.app_context():
        assert Users.query.count() == 1
        assert Users.query.first().email == "testuser@hotmail.com"

    #delete user
    resp2=client.get("/users/1/delete", follow_redirects=True)
    #check if user was deleted from db
    with app.app_context():
        assert Users.query.count() == 0

    #check if user redirected to createuser after deleting
    assert b"<title>Create User</title>" in resp2.data

def test_updateuser(client, app):
    #register
    client.post("/users/new", data=dict([('username', 'testuser2'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'), ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]) )
    #login
    resp1=client.post("/login", data=dict([('username', 'testuser2'), ('password', '123')]), follow_redirects=True)

    #check if user in db and it it's the correct one
    with app.app_context():
        assert Users.query.first().username == "testuser2"

    #update userpage
    resp2=client.get("/users/1/update", follow_redirects=True)
    assert b"<title>Update User</title>" in resp2.data

    #update user
    resp3=client.post("/users/1/update", data=dict([('username', 'differentname'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'), ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]), follow_redirects=True )

    assert b"<title>Update User</title>" in resp3.data

    #check if user was updated
    with app.app_context():
        assert Users.query.first().username == "differentname"

def test_newproduct(client, app):

    client.post("/users/new", data=dict(
        [('username', 'testuser'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'),
         ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]))

    # login
    resp2 = client.post("/login", data=dict([('username', 'testuser'), ('password', '123')]), follow_redirects=True)


    resp3= client.get("/products/new", follow_redirects=True)
    assert b"<title>Add a product</title>" in resp3.data

    resp4 = client.post("/products/new", data=dict([('user_id', '1'), ('name', 'testproduct'), ('price', '123'), ('image_url', 'https://i.ibb.co/cYCby3R/r4.png'), ('description', 'test descp')]), follow_redirects=True )

    with app.app_context():
        assert Products.query.count() == 1
        assert Products.query.first().name == "testproduct"

    assert b"<title>Add a product</title>" in resp4.data

def test_showdetails(client,app):
    # register
    client.post("/users/new", data=dict(
        [('username', 'testuser'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'),
         ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]))
    # login
    client.post("/login", data=dict([('username', 'testuser'), ('password', '123')]), follow_redirects=True)
    # add a product
    client.post("/products/new", data=dict(
        [('user_id', '1'), ('name', 'testproduct'), ('price', '123'), ('image_url', 'https://i.ibb.co/cYCby3R/r4.png'),
         ('description', 'test descp')]), follow_redirects=True)
    #show details
    resp2 = client.get("/products/1", follow_redirects=True)

    assert b'<h5 class="card-title">testproduct</h5>' in resp2.data

def test_productupdate(client, app):
    #register
    client.post("/users/new", data=dict(
        [('username', 'testuser'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'),
         ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]))

    # login
    client.post("/login", data=dict([('username', 'testuser'), ('password', '123')]), follow_redirects=True)
    # add a product
    client.post("/products/new", data=dict([('user_id', '1'), ('name', 'testproduct'), ('price', '123'), ('image_url', 'https://i.ibb.co/cYCby3R/r4.png'), ('description', 'test descp')]), follow_redirects=True )
    #check db
    with app.app_context():
        assert Products.query.first().name == "testproduct"
    #check update page
    resp1= client.get("/products/1/update", follow_redirects=True)
    assert b"<h1> Edit Product </h1>" in resp1.data
    #update product
    resp2=client.post("/products/1/update", data=dict([('user_id', '1'), ('name', 'newname'), ('price', '123'), ('image_url', 'https://i.ibb.co/cYCby3R/r4.png'), ('description', 'test descp')]), follow_redirects=True)
    #check db
    with app.app_context():
        assert Products.query.first().name == "newname"
    #check redirect
    assert b"<h1>Product Details</h1>" in resp2.data

def test_productdelete(client, app):
    #register
    client.post("/users/new", data=dict(
        [('username', 'testuser'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'),
         ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]))

    # login
    client.post("/login", data=dict([('username', 'testuser'), ('password', '123')]), follow_redirects=True)
    # add a product
    client.post("/products/new", data=dict([('user_id', '1'), ('name', 'testproduct'), ('price', '123'), ('image_url', 'https://i.ibb.co/cYCby3R/r4.png'), ('description', 'test descp')]), follow_redirects=True )
    #check db
    with app.app_context():
        assert Products.query.first().name == "testproduct"

    #delete product
    resp1=client.get("/products/1/delete", follow_redirects=True)
    #check db
    with app.app_context():
        assert Products.query.count() == 0
    #check redirect
    assert b"<title>Index</title>" in resp1.data

def test_search(client):
    # register
    client.post("/users/new", data=dict(
        [('username', 'testuser'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'),
         ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]))
    # login
    client.post("/login", data=dict([('username', 'testuser'), ('password', '123')]), follow_redirects=True)

    resp=client.post("/search", data=dict([('searched',"test")]), follow_redirects=True)
    assert b"No products found :( !" in resp.data

    # add a product
    client.post("/products/new", data=dict(
        [('user_id', '1'), ('name', 'testproduct'), ('price', '123'), ('image_url', 'https://i.ibb.co/cYCby3R/r4.png'),
         ('description', 'test descp')]), follow_redirects=True)

    resp2=client.post("/search", data=dict([('searched',"test")]), follow_redirects=True)
    assert b"testproduct" in resp2.data

def test_shoppingcart(client,app):
    # register
    client.post("/users/new", data=dict(
        [('username', 'testuser'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'),
         ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]))
    # login
    client.post("/login", data=dict([('username', 'testuser'), ('password', '123')]), follow_redirects=True)
    # add a product
    client.post("/products/new", data=dict(
        [('user_id', '1'), ('name', 'testproduct'), ('price', '123'), ('image_url', 'https://i.ibb.co/cYCby3R/r4.png'),
         ('description', 'test descp')]), follow_redirects=True)
    #check empty cart
    resp3 = client.get("/shoppingcart", follow_redirects=True)
    assert b'Your shoppingcart is empty!' in resp3.data

    # add a product to cart
    resp1=client.get("/products/1/add",follow_redirects=True)
    assert b'<h5 class="card-title">testproduct</h5>' in resp1.data

    #there should be a cart and a cartitem
    with app.app_context():
        assert Carts.query.count() == 1
        assert Cart_items.query.count() == 1
    #the cart shows the product
    resp2 = client.get("/shoppingcart", follow_redirects=True)
    assert b'<h5 class="text-primary">testproduct</h5>' in resp2.data
    #change quantity in cart
    resp4=client.post("/shoppingcart/1/change_quantity", data=dict([("quantity", '4')]), follow_redirects=True)
    assert b'<input class="quantity fw-bold text-black "  min="1" max="99"  name="quantity" value="4" type="number" readonly>' in resp4.data
    with app.app_context():
        cart=Cart_items.query.first()
        assert cart.quantity==4


def test_order(client,app):
    # register
    client.post("/users/new", data=dict(
        [('username', 'testuser'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'),
         ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]))
    # login
    client.post("/login", data=dict([('username', 'testuser'), ('password', '123')]), follow_redirects=True)
    # add a product
    client.post("/products/new", data=dict(
        [('user_id', '1'), ('name', 'testproduct'), ('price', '123'), ('image_url', 'https://i.ibb.co/cYCby3R/r4.png'),
         ('description', 'test descp')]), follow_redirects=True)

    # add a product to cart
    resp1=client.get("/products/1/add",follow_redirects=True)
    assert b'<h5 class="card-title">testproduct</h5>' in resp1.data

    #not following the redirect to mollie here
    client.post("/shoppingcart/order", data=dict([('email', 'testuser@testmail.com'), ('fullname', 'testname')]))
    with app.app_context():
        #order gets made, payment made, cart deleted from db
        assert Orders.query.count()== 1
        assert Payments.query.count() == 1
        assert Carts.query.count() == 0






