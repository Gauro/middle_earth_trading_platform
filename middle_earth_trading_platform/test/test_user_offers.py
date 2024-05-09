def test_get_user_positive(client):
    user_id = 1

    # Send a GET request to the endpoint
    response = client.get(f"/users/{user_id}")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200


def test_get_user_not_found(client):
    user_id = 10000000

    # Send a GET request to the endpoint
    response = client.get(f"/users/{user_id}")

    # Assert that the response status code is 404 (OK)
    assert response.status_code == 404
    assert response.content == b'{"error":"User not found"}'


def test_get_user_inventory_success(client):
    user_id = 1

    # Send a GET request to the endpoint
    response = client.get(f"/users/{user_id}/user_inventory")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200


def test_get_user_inventory_user_not_found(client):
    user_id = 10000000

    # Send a GET request to the endpoint
    response = client.get(f"/users/{user_id}/user_inventory")

    # Assert that the response status code is 404 (OK)
    assert response.status_code == 404


def test_get_user_inventory_user_inventory_not_found(client):
    user_id = 5

    # Send a GET request to the endpoint
    response = client.get(f"/users/{user_id}/user_inventory")

    # Assert that the response status code is 404 (OK)
    assert response.status_code == 404


def test_create_offer(client):
    user_id = 1
    receiver_id = 2
    sender_items = {"staff": 2}
    receiver_items = {"sword": 2}

    # Send a POST request to the endpoint
    response = client.post(
        "/offers/create_offer",
        json={
            "user_id": user_id,
            "sender_items": sender_items,
            "receiver_id": receiver_id,
            "receiver_items": receiver_items
        }
    )

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Optionally, you can also assert the response content if needed
    assert response.json() == {"data": "success"}


def test_create_offer_error_cases(client):
    # test 1: sender does not have enough weapons in inventory to barter
    body1 = {
        "user_id": 1,
        "sender_items": {"staff": 10},
        "receiver_id": 2,
        "receiver_items": {"sword": 2}
    }

    # Send a POST request to the endpoint
    response = client.post(
        "/offers/create_offer",
        json=body1
    )

    assert response.status_code == 400

    # test 2: sender does not possess the weapon for barter
    body2 = {
        "user_id": 1,
        "sender_items": {"sickle": 1},
        "receiver_id": 2,
        "receiver_items": {"sword": 2}
    }

    # Send a POST request to the endpoint
    response = client.post(
        "/offers/create_offer",
        json=body2
    )

    assert response.status_code == 400

    # test 3: receiver does not have enough weapons in inventory to barter
    body3 = {
        "user_id": 1,
        "sender_items": {"staff": 2},
        "receiver_id": 2,
        "receiver_items": {"sword": 20}
    }

    # Send a POST request to the endpoint
    response = client.post(
        "/offers/create_offer",
        json=body3
    )

    assert response.status_code == 400

    # test 4: sender does not possess the weapon for barter
    body4 = {
        "user_id": 1,
        "sender_items": {"axe": 2},
        "receiver_id": 2,
        "receiver_items": {"hammer": 2}
    }

    # Send a POST request to the endpoint
    response = client.post(
        "/offers/create_offer",
        json=body4
    )

    assert response.status_code == 400


def test_get_user_offers_success(client):
    user_id = 2

    # Send a GET request to the endpoint
    response = client.get(f"/users/{user_id}/get_offers")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200


def test_get_all_offers_success(client):
    response = client.get("/offers/all_offers")
    assert response.status_code == 200
