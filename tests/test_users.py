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


def test_create_user(client, auth_headers):
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


def test_create_duplicate_username(client, auth_headers):
    response = client.post(
        'api/users/',
        headers=auth_headers,
        json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'secret123',
        },
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Username já está em uso'}


def test_create_duplicate_email(client, auth_headers):
    response = client.post(
        'api/users/',
        headers=auth_headers,
        json={
            'username': 'testusernew',
            'email': 'test@example.com',
            'password': 'secret123',
        },
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Email já está em uso'}


def test_create_user_username_too_short(client, auth_headers):
    response = client.post(
        'api/users/',
        headers=auth_headers,
        json={
            'username': 'ab',
            'email': 'test@example.com',
            'password': 'password123',
        },
    )

    assert response.status_code == 422
    error_data = response.json()
    assert 'Username deve ter pelo menos 3 caracteres' in str(error_data)


def test_create_user_password_too_short(client, auth_headers):
    response = client.post(
        'api/users/',
        headers=auth_headers,
        json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '12345',
        },
    )

    assert response.status_code == 422
    error_data = response.json()
    assert 'Senha deve ter pelo menos 6 caracteres' in str(error_data)


def test_list_user(client, auth_headers):
    response = client.get(
        'api/users/',
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data['users']) == 1


def test_list_user_with_search(client, auth_headers):
    response = client.get(
        'api/users/?search=testuser',
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data['users'][0]['username'] == 'testuser'
    assert data['users'][0]['email'] == 'test@example.com'


def test_list_user_with_search_none_existe(client, auth_headers):
    response = client.get(
        'api/users/?search=rodrigo',
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_get_user_by_id(client, auth_headers):
    response = client.get(
        'api/users/1',
        headers=auth_headers,
    )

    assert response.status_code == 200
    user_data = response.json()
    assert user_data['id'] == 1
    assert user_data['username'] == 'testuser'


def test_get_user_not_found(client, auth_headers):
    response = client.get(
        'api/users/10',
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_update_user_success(client, auth_headers):
    response = client.put(
        'api/users/1',
        headers=auth_headers,
        json={'username': 'updatetesteuser'},
    )

    assert response.status_code == 200
    user_data = response.json()
    assert user_data['username'] == 'updatetesteuser'


def test_update_user_password(client, auth_headers):
    response = client.put(
        'api/users/1',
        headers=auth_headers,
        json={'password': 'newpassword123456'},
    )

    assert response.status_code == 200


def test_update_user_not_found(client, auth_headers):
    response = client.put(
        'api/users/10', headers=auth_headers, json={'username': 'usernotfound'}
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_update_user_same_username(client, user, second_user, auth_headers):
    response = client.put(
        f'api/users/{user.id}',
        headers=auth_headers,
        json={'username': second_user.username},
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Username já está em uso'}


def test_update_user_same_email(client, user, second_user, auth_headers):
    response = client.put(
        f'api/users/{user.id}',
        headers=auth_headers,
        json={'email': second_user.email},
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Email já está em uso'}


def test_update_user_username_too_short(client, auth_headers, user):
    response = client.put(
        f'api/users/{user.id}',
        headers=auth_headers,
        json={
            'username': 'ab',
        },
    )

    assert response.status_code == 422
    error_data = response.json()
    assert 'Username deve ter pelo menos 3 caracteres' in str(error_data)


def test_update_user_password_too_short(client, auth_headers, user):
    response = client.put(
        f'api/users/{user.id}',
        headers=auth_headers,
        json={
            'password': '12345',
        },
    )

    assert response.status_code == 422
    error_data = response.json()
    assert 'Senha deve ter pelo menos 6 caracteres' in str(error_data)


def test_delete_user(client, second_user, auth_headers):
    response = client.delete(
        f'api/users/{second_user.id}',
        headers=auth_headers,
    )

    assert response.status_code == 204


def test_delete_user_not_found(client, auth_headers):
    response = client.delete(
        'api/users/10',
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuário não encontrado'}
