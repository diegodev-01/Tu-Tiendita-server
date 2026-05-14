from pydantic import BaseModel, Field


class TransactionItem(BaseModel):
    productId: str
    quantityToReceive: int = Field(gt=0)
