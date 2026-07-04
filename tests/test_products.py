def test_create_product(client, auth_headers):
    response = client.post(
        'api/products/',
        headers=auth_headers,
        json={
            'title': 'teclado logi',
            'price': 2000,
            'description': 'rapido e bonito',
            'brand': 'logitec',
        },
    )

    assert response.status_code == 201
    product_data = response.json()
    assert product_data['title'] == 'teclado logi'


def test_create_product_unauthorize(client):
    response = client.post(
        'api/products/',
        json={
            'title': 'teclado logi',
            'price': 2000,
            'description': 'rapido e bonito',
            'brand': 'logitec',
        },
    )

    assert response.status_code == 401


def test_create_product_title_too_short(client, auth_headers):
    response = client.post(
        'api/products/',
        headers=auth_headers,
        json={
            'title': 't',
            'price': 2000,
            'description': 'rapido e bonito',
            'brand': 'logitec',
        },
    )

    assert response.status_code == 422
    error_data = response.json()
    assert 'Título deve ter pelo menos 2 caracteres' in str(error_data)


def test_create_product_brand_too_short(client, auth_headers):
    response = client.post(
        'api/products/',
        headers=auth_headers,
        json={
            'title': 'teclado logi',
            'price': 2000,
            'description': 'rapido e bonito',
            'brand': 'l',
        },
    )

    assert response.status_code == 422
    error_data = response.json()
    assert 'Marca deve ter pelo menos 2 caracteres' in str(error_data)


def test_create_product_price_zero(client, auth_headers):
    response = client.post(
        'api/products/',
        headers=auth_headers,
        json={
            'title': 'teclado logi',
            'price': 0,
            'description': 'rapido e bonito',
            'brand': 'logitec',
        },
    )

    assert response.status_code == 422
    error_data = response.json()
    assert 'Preço deve ser maior que zero' in str(error_data)


def test_list_products(client, auth_headers, product, second_product):
    response = client.get(
        'api/products/',
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data['products']) == 2
    assert data['products'][0]['title'] == product.title
    assert data['products'][1]['title'] == second_product.title


def test_list_products_with_search(client, auth_headers, product):
    response = client.get(
        'api/products/?search=de teste',
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data['products']) == 1
    assert data['products'][0]['title'] == product.title


def test_list_products_min_price(client, auth_headers, product):
    response = client.get(
        'api/products/?min_price=2000',
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data['products']) == 1
    assert data['products'][0]['title'] == product.title


def test_list_products_max_price(client, auth_headers, second_product):
    response = client.get(
        'api/products/?max_price=1500',
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data['products']) == 1
    assert data['products'][0]['title'] == second_product.title


def test_list_products_with_price_and_search(client, auth_headers, product):
    response = client.get(
        'api/products/?max_price=3000&min_price=2000&search=testando',
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data['products']) == 1
    assert data['products'][0]['title'] == product.title


def test_get_product(client, product, auth_headers):
    response = client.get(
        f'api/products/{product.id}',
        headers=auth_headers,
    )

    assert response.status_code == 200
    product_data = response.json()
    assert product_data['title'] == 'testando'
    assert product_data['id'] == 1


def test_get_product_not_found(client, auth_headers):
    response = client.get(
        'api/products/10',
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'produto não encontrado'}


def test_update_product(client, product, auth_headers):
    response = client.put(
        f'api/products/{product.id}',
        headers=auth_headers,
        json={'title': 'mouse laranja', 'price': 500},
    )

    assert response.status_code == 200
    product_data = response.json()
    assert product_data['title'] == 'mouse laranja'
    assert product_data['price'] == '500.00'


def test_update_product_not_found(client, auth_headers):
    response = client.put(
        'api/products/10',
        headers=auth_headers,
        json={'title': 'mouse laranja', 'price': 500},
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Produto não encontrado'}


def test_update_product_title_too_short(client, auth_headers, product):
    response = client.put(
        f'api/products/{product.id}',
        headers=auth_headers,
        json={
            'title': 't',
        },
    )

    assert response.status_code == 422
    error_data = response.json()
    assert 'Título deve ter pelo menos 2 caracteres' in str(error_data)


def test_update_product_brand_too_short(client, auth_headers, product):
    response = client.put(
        f'api/products/{product.id}',
        headers=auth_headers,
        json={
            'brand': 'l',
        },
    )

    assert response.status_code == 422
    error_data = response.json()
    assert 'Marca deve ter pelo menos 2 caracteres' in str(error_data)


def test_update_product_price_zero(client, auth_headers, product):
    response = client.put(
        f'api/products/{product.id}',
        headers=auth_headers,
        json={
            'title': 'teclado logi',
            'price': 0,
            'description': 'rapido e bonito',
            'brand': 'logitec',
        },
    )

    assert response.status_code == 422
    error_data = response.json()
    assert 'Preço deve ser maior que zero' in str(error_data)


def test_delete_product(client, second_product, auth_headers):
    response = client.delete(
        f'api/products/{second_product.id}',
        headers=auth_headers,
    )

    assert response.status_code == 204


def test_delete_product_not_found(client, auth_headers):
    response = client.delete(
        'api/products/10',
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Produto não encontrado'}
