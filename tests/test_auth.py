
def test_signup(client):
    response = client.post('/auth/signup', json={'username': 'kartikeyy', 'password': 'mishra#6000'})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'User registered successfully.'}


def test_signup_existing_user(client):
    client.post('/auth/signup', json={'username': 'shobhit', 'password': 'shobhit@segwise'})
    response = client.post('/auth/signup', json={'username': 'shobhit', 'password': 'shobhit@segwise'})
    assert response.status_code == 400
    assert 'User already registered' in response.get_json()['message']


def test_login(client):
    client.post('/auth/signup', json={'username': 'kartikey', 'password': 'mishra#600'})
    response = client.post('/auth/login', json={'username': 'kartikeyy', 'password': 'mishra#6000'})
    assert response.status_code == 200
    assert 'token' in response.get_json()
