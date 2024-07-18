
def test_get_numerical_data(client, auth_token):
    response = client.get('/query/query?Positive=87', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_name(client,auth_token):
    response = client.get('/query/query?Name=Tele', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_date_range_search(client, auth_token):
    response = client.get('/query/query?start_date=2020-01-03&end_date=2020-05-03', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200


def test_aggregate_search(client, auth_token):
    response = client.get('/query/query?aggregate_field=Price&aggregate_type=count',
                          headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, int)



