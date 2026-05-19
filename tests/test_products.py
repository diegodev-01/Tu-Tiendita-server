from fastapi.testclient import TestClient
from main import app
from src.api.endpoints.products import get_product_service
from src.dependencies.auth import get_current_user
from src.schemas.auth_schema import UserAuthDetails
from src.models.role import Role

client = TestClient(app)


class MockProductService:
    async def create_product(self, product_in, ownerId: str) -> str:
        return "fake-id-product"

    async def get_all_products(self):
        return [
            {
                "_id": "fake-id-product",
                "storeId": "store_123",
                "name": "Producto Test",
                "sku": "SKU-TEST-01",
                "nfcTagId": "TAG123",
                "price": 10.5,
                "stock": 20,
                "minStock": 5,
                "shelf": "Estante A",
                "status": "active",
                "createdAt": "2026-05-10T12:00:00Z",
                "updatedAt": "2026-05-14T22:58:45Z",
            }
        ]


def override_get_product_service():
    return MockProductService()


def override_get_current_user():
    return UserAuthDetails(
        sub="fake-id-user",
        name="Fake User",
        email="fake-user@fake-email.com",
        roles=[Role.CUSTOMER],
        permissions=["product:create", "product:view"],
    )


app.dependency_overrides[get_product_service] = override_get_product_service
app.dependency_overrides[get_current_user] = override_get_current_user


def test_create_product():
    payload = {
        "storeId": "fake-id-store",
        "name": "Coca Cola",
        "sku": "123",
        "nfcTagId": "123",
        "price": 12.5,
        "stock": 10,
        "minStock": 2,
        "shelf": "Refrigerador",
        "status": "active",
    }
    response = client.post("/api/products/", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Producto creado"
    assert "id" in response.json()
    assert response.json()["id"] == "fake-id-product"


def test_list_products():
    response = client.get("/api/products/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    primer_producto = data[0]
    assert primer_producto["name"] == "Producto Test"

    assert "_id" in primer_producto

    assert "updatedAt" in primer_producto
    assert primer_producto["updatedAt"].startswith("2026-05-14")
