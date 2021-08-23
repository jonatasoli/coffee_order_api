from fastapi import APIRouter, status
from .api_schemas import CreateOrderResponseAPI, CreateOrderAPI
from loguru import logger


order = APIRouter()

@order.post("/order",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateOrderResponseAPI,
)
async def create_order(
    _data: CreateOrderAPI
):
    logger.debug(_data)
    return CreateOrderResponseAPI(
        id=1,
        name="John Doe",
        product="Latte",
        amount=1000,
        status="Waiting Payment"
    )
