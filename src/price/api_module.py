from fastapi import FastAPI

from src.price.api.api_v1.price.commands import price_commands_router
from src.price.api.api_v1.price.q import price_q_router


class PriceApiModule:
    name = "price"
    order = 12
    mount_paths = ["/price"]

    def mount(self, app: FastAPI) -> None:
        app.include_router(price_q_router, prefix="/price")
        app.include_router(price_commands_router, prefix="/price")
