import requests_mock


def test_upload_csv(client, auth_token):
    with requests_mock.Mocker() as m:
        # Mock the GET request to the specified URL
        m.get('https://drive.google.com/uc?export=download&id=18450NWcYxXZoEVrwwjwfIfDgLUUZPJPQ',
              text='AppID,Name,Release date,Required age,Price\n1,Test Game,2022-01-01,0,19.99')
        response = client.post('/main/upload_csv', json={
            "csv_url": "https://drive.google.com/uc?export=download&id=18450NWcYxXZoEVrwwjwfIfDgLUUZPJPQ"
        }, headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'CSV upload and processing completed.'}
