from fastapi import status


def test_create_order_with_success(client):
    _data=dict(name="John Doe", product="Latte", amount=1000)
    response = client.post('/order', json=_data)
    assert response.status_code == status.HTTP_201_CREATED



def test_create_order_return_data_with_id_and_status(client):
    _data=dict(name="John Doe", product="Latte", amount=1000)
    response = client.post('/order', json=_data)
    assert response.json() == dict(
        id=1,
        name="John Doe",
        product="Latte",
        amount=1000,
        status="Waiting Payment"
    )


def test_create_order_error_entity_incorrect(client):
    _data=dict(invalid="John Doe")
    response = client.post('/order', json=_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
