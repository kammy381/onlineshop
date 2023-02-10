from models import Users


def test_home(client):
    response = client.get("/")
    #b to convert t bytes
    assert b"<title>Index</title>" in response.data

def test_register(client, app):
    response = client.post("/users/new", data=dict([('username', 'testuser'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'), ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]) )

    with app.app_context():

        assert Users.query.count() == 1
        assert Users.query.first().email == "testuser@hotmail.com"

def test_register_login_logout(client, app):
    #register
    client.post("/users/new", data=dict([('username', 'testuser'), ('email', 'testuser@hotmail.com'), ('password_hash', '123'), ('password_hash2', '123'), ('address', '123'), ('postal_code', '123'), ('city', '123'), ('country', '123')]) )
    #login
    response=client.post("/login", data=dict([('username', 'testuser'), ('password', '123')]), follow_redirects=True)

    #check if user in db and it it's the correct one
    with app.app_context():
        assert Users.query.count() == 1
        assert Users.query.first().email == "testuser@hotmail.com"
    #check if user is redirected to dashboard after loging in
    assert b"<h1>Dashboard</h1>" in response.data

    #logout
    resp2=client.get("/logout", follow_redirects=True)

    #check if user redirected to indexpage after logging out
    assert b"<title>Index</title>" in resp2.data