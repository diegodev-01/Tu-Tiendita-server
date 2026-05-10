from fastapi.testclient import TestClient
from main import app
from src.api.endpoints.products import get_product_service
from src.dependencies.auth import get_current_user
from src.schemas.auth_schema import UserAuthDetails

client = TestClient(app)


class MockProductService:
    async def create_product(self, product_in, owner_id):
        return "mocked_id_123"

    async def get_all_products(self):
        return [
            {
                "id": "1",
                "name": "Producto Test",
                "price": 10.5,
                "nfc_tag_id": "TAG123",
                "sync_date": "2026-05-10T12:00:00",
            }
        ]


def override_get_product_service():
    return MockProductService()


def override_get_current_user():
    return UserAuthDetails(
        username="testuser",
        roles=["admin"],
        permissions=[
            "product:create",
            "product:view",
            "product:edit",
            "product:delete",
        ],
    )


app.dependency_overrides[get_product_service] = override_get_product_service
app.dependency_overrides[get_current_user] = override_get_current_user


def test_create_product():
    payload = {"name": "Coca Cola", "price": 12.5, "nfc_tag_id": "NFC_ABC_123"}
    response = client.post("/api/products/", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Producto creado"
    assert "id" in response.json()


def test_list_products():
    response = client.get("/api/products/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["name"] == "Producto Test"
