def test_item_crud(client):
    response = client.post("/api/v1/item", json={"name": "one"})
    assert response.status_code == 200
    item = response.json()
    assert item == {"id": 1, "name": "one"}

    response = client.get("/api/v1/item/1")
    assert response.status_code == 200
    assert response.json() == item

    response = client.put("/api/v1/item/1", json={"name": "two"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "two"}

    response = client.get("/api/v1/items")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "two"}]

    response = client.delete("/api/v1/item/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "two"}

    response = client.get("/api/v1/items")
    assert response.status_code == 200
    assert response.json() == []


def test_item_not_found(client):
    assert client.get("/api/v1/item/404").status_code == 404
    assert client.put("/api/v1/item/404", json={"name": "nope"}).status_code == 404
    assert client.delete("/api/v1/item/404").status_code == 404
