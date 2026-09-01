def test_create_and_get_item(client):
    create_response = client.post("/api/v1/item", json={"name": "Test Item"})
    assert create_response.status_code == 200
    created_item = create_response.json()
    assert created_item["name"] == "Test Item"
    assert "id" in created_item

    get_response = client.get(f"/api/v1/item/{created_item['id']}")
    assert get_response.status_code == 200
    fetched_item = get_response.json()
    assert fetched_item["id"] == created_item["id"]
    assert fetched_item["name"] == "Test Item"


def test_list_items(client):
    first_response = client.post("/api/v1/item", json={"name": "First Item"})
    second_response = client.post("/api/v1/item", json={"name": "Second Item"})

    response = client.get("/api/v1/items")

    assert response.status_code == 200
    assert response.json() == [
        {"id": first_response.json()["id"], "name": "First Item"},
        {"id": second_response.json()["id"], "name": "Second Item"},
    ]


def test_update_item(client):
    create_response = client.post("/api/v1/item", json={"name": "Old Name"})
    item_id = create_response.json()["id"]

    response = client.put(f"/api/v1/item/{item_id}", json={"name": "New Name"})

    assert response.status_code == 200
    assert response.json() == {"id": item_id, "name": "New Name"}


def test_update_missing_item_returns_404(client):
    response = client.put("/api/v1/item/1", json={"name": "New Name"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_delete_item(client):
    create_response = client.post("/api/v1/item", json={"name": "Test Item"})
    item_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/item/{item_id}")
    get_response = client.get(f"/api/v1/item/{item_id}")

    assert response.status_code == 200
    assert response.json() == {"id": item_id, "name": "Test Item"}
    assert get_response.status_code == 404


def test_delete_missing_item_returns_404(client):
    response = client.delete("/api/v1/item/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_get_missing_item_returns_404(client):
    response = client.get("/api/v1/item/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
