def test_create_favorite(client, auth_headers, product):
    response = client.post(
        'api/favorites/',
        headers=auth_headers,
        json={
            'product_id': product.id,
        },
    )

    assert response.status_code == 201
    favorite_data = response.json()
    assert favorite_data['id'] == 1
    assert favorite_data['product']['title'] == product.title


def test_create_favorite_unauthorize(client, product):
    response = client.post(
        'api/favorites/',
        json={
            'product_id': product.id,
        },
    )

    assert response.status_code == 401


def test_create_favorite_product_not_exists(client, auth_headers):
    response = client.post(
        'api/favorites/',
        headers=auth_headers,
        json={
            'product_id': 10,
        },
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Produto não encontrado'}


def test_create_favorite_duplicated(client, auth_headers, product, favorite):
    response = client.post(
        'api/favorites/',
        headers=auth_headers,
        json={
            'product_id': product.id,
        },
    )

    assert response.status_code == 400


def test_list_favorite_(client, favorite, auth_headers):
    response = client.get(
        'api/favorites/',
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data['favorites']) == 1


def test_list_favorite_unauthorize(client):
    response = client.get(
        'api/favorites/',
    )

    assert response.status_code == 401


def test_delete_favorite(client, favorite, auth_headers):
    response = client.delete(
        f'api/favorites/{favorite.id}',
        headers=auth_headers,
    )

    assert response.status_code == 204


def test_delete_favorite_not_fount(client, auth_headers):
    response = client.delete(
        'api/favorites/15',
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Produto não encontrado'}
