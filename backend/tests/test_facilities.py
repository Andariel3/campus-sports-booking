from fastapi.testclient import TestClient

TENNIS_COURT = {
    "name": "Teren tenis 1",
    "sport": "tennis",
    "location": "Corp E, langa sala de sport",
    "capacity": 4,
}


def create(client: TestClient, **overrides) -> dict:
    response = client.post("/api/facilities", json={**TENNIS_COURT, **overrides})
    assert response.status_code == 201, response.text
    return response.json()


def test_health(client: TestClient) -> None:
    assert client.get("/api/health").json() == {"status": "ok"}


def test_create_and_get(client: TestClient) -> None:
    created = create(client)
    assert created["id"] > 0
    assert created["is_active"] is True

    response = client.get(f"/api/facilities/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Teren tenis 1"


def test_list_and_filter_by_sport(client: TestClient) -> None:
    create(client)
    create(client, name="Bazin", sport="swimming", capacity=40)

    assert len(client.get("/api/facilities").json()) == 2
    pools = client.get("/api/facilities", params={"sport": "swimming"}).json()
    assert [f["name"] for f in pools] == ["Bazin"]


def test_update_changes_only_sent_fields(client: TestClient) -> None:
    created = create(client)
    response = client.patch(f"/api/facilities/{created['id']}", json={"capacity": 6})
    assert response.status_code == 200
    assert response.json()["capacity"] == 6
    assert response.json()["name"] == created["name"]


def test_delete(client: TestClient) -> None:
    created = create(client)
    assert client.delete(f"/api/facilities/{created['id']}").status_code == 204
    assert client.get(f"/api/facilities/{created['id']}").status_code == 404


def test_missing_facility_returns_404(client: TestClient) -> None:
    assert client.get("/api/facilities/999").status_code == 404
    assert client.patch("/api/facilities/999", json={"capacity": 2}).status_code == 404
    assert client.delete("/api/facilities/999").status_code == 404


def test_duplicate_name_returns_409(client: TestClient) -> None:
    create(client)
    response = client.post("/api/facilities", json=TENNIS_COURT)
    assert response.status_code == 409


def test_invalid_data_returns_422(client: TestClient) -> None:
    response = client.post("/api/facilities", json={**TENNIS_COURT, "capacity": 0})
    assert response.status_code == 422
    response = client.post("/api/facilities", json={**TENNIS_COURT, "sport": "chess"})
    assert response.status_code == 422
