from pydantic import BaseModel


class BaseOrder(BaseModel):
    name: str
    product: str
    amount: int


class CreateOrderResponseAPI(BaseOrder):
    id: int
    status: str


class CreateOrderAPI(BaseOrder):
    ...
