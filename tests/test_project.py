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
