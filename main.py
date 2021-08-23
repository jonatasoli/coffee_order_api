from fastapi import FastAPI, status
from order.entrypoints.api import order


def create_app():
    app = FastAPI()
    app.include_router(order)

    return app



