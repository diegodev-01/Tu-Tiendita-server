from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    productId: str
    name: str
    price: float
    quantity: int = Field(gt=0)
