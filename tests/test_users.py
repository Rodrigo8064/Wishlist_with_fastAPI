def test_create_user_without_permission(client):
    response = client.post(
        'api/users/',
        json={
            'username': 'newuser',
            'email': 'newuser@teste.com',
            'password': 'password123',
        },
    )

    assert response.status_code == 401


def test_create_user(client, user, auth_headers):
    response = client.post(
        'api/users/',
        headers=auth_headers,
        json={
            'username': 'newuser',
            'email': 'newuser@teste.com',
            'password': 'password123',
        },
    )

    assert response.status_code == 201
    user_data = response.json()
    assert user_data['username'] == 'newuser'
    assert user_data['email'] == 'newuser@teste.com'
    assert user_data['id'] == 2
    assert 'created_at' in user_data
    assert 'updated_at' in user_data
