def test_create_review(client, auth_headers, product):
    response = client.post(
        'api/reviews/',
        headers=auth_headers,
        json={
            'stars': '5',
            'comment': 'muito bacana',
            'product_id': product.id,
        },
    )

    assert response.status_code == 201
    review_data = response.json()
    assert review_data['stars'] == 5
    assert review_data['comment'] == 'muito bacana'


def test_create_review_with_6_stars(client, auth_headers, product):
    response = client.post(
        'api/reviews/',
        headers=auth_headers,
        json={
            'stars': '6',
            'comment': 'muito bacana',
            'product_id': product.id,
        },
    )

    assert response.status_code == 422
    data = response.json()
    assert (
        data['detail'][0]['msg']
        == 'Value error, Estrelas devem estar entre 0 e 5'
    )


def test_create_review_unauthorize(client, product):
    response = client.post(
        'api/reviews/',
        json={
            'stars': '5',
            'comment': 'muito bacana',
            'product_id': product.id,
        },
    )

    assert response.status_code == 401


def test_update_review_unauthorize(client, review):
    response = client.put(
        f'api/reviews/{review.id}',
        json={
            'stars': '3',
            'comment': 'achei mais ou menos',
        },
    )

    assert response.status_code == 401


def test_update_review(client, review, auth_headers):
    response = client.put(
        f'api/reviews/{review.id}',
        headers=auth_headers,
        json={
            'stars': '3',
            'comment': 'achei mais ou menos',
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data['stars'] == 3
    assert data['comment'] == 'achei mais ou menos'


def test_update_review_not_fount(client, auth_headers):
    response = client.put(
        'api/reviews/15',
        headers=auth_headers,
        json={
            'stars': '3',
            'comment': 'achei mais ou menos',
        },
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Review não encontrado'}


def test_update_review_with_6_stars(client, auth_headers, product):
    response = client.put(
        f'api/reviews/{product.id}',
        headers=auth_headers,
        json={
            'stars': '6',
        },
    )

    assert response.status_code == 422
    data = response.json()
    assert (
        data['detail'][0]['msg']
        == 'Value error, Estrelas devem estar entre 0 e 5'
    )


def test_delete_review(client, review, auth_headers):
    response = client.delete(
        f'api/reviews/{review.id}',
        headers=auth_headers,
    )

    assert response.status_code == 204


def test_delete_review_not_fount(client, auth_headers):
    response = client.delete(
        'api/reviews/15',
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Review não encontrado'}
