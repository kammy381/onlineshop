from models import Users, Products

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
    # go to login page
    resp1 = client.get("/login")
    assert b"<h1>Login</h1>" in resp1.data

    with app.app_context():

        assert Users.query.count() == 1
        assert Users.query.first().email == "testuser@hotmail.com"

    # login
    resp2 = client.post("/login", data=dict([('username', 'testuser'), ('password', '123')]), follow_redirects=True)

    # check if user is redirected to dashboard after loging in
    assert b"<h1>Dashboard</h1>" in resp2.data

    resp3= client.get("/products/new", follow_redirects=True)
    assert b"<title>Add a product</title>" in resp3.data

    resp4 = client.post("/products/new", data=dict([('user_id', '1'), ('name', 'testproduct'), ('price', '123'), ('image_url', 'https://i.ibb.co/cYCby3R/r4.png'), ('description', 'test descp')]), follow_redirects=True )

    with app.app_context():
        assert Products.query.count() == 1
        assert Products.query.first().name == "testproduct"

    assert b"<title>Add a product</title>" in resp4.data

def test_register_login_logout_again(client, app):
    #register
    client.post("/users/new", data=dict([('username', 'testuser'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'), ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]) )

    #login
    resp2=client.post("/login", data=dict([('username', 'testuser'), ('password', '123')]), follow_redirects=True)

    #check if user is redirected to dashboard after loging in
    assert b"<h1>Dashboard</h1>" in resp2.data

    #logout
    resp3=client.get("/logout", follow_redirects=True)

    #check if user redirected to indexpage after logging out
    assert b"<title>Index</title>" in resp3.data

