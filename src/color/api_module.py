from fastapi import FastAPI

from src.color.api.api_v1.color.commands import color_commands_router
from src.color.api.api_v1.color.q import color_q_router
from src.color.api.api_v1.color_assign.commands import color_assign_commands_router
from src.color.api.api_v1.color_assign.q import color_assign_q_router


class ColorApiModule:
    name = "color"
    order = 11
    mount_paths = ["/color"]

    def mount(self, app: FastAPI) -> None:
        app.include_router(color_q_router, prefix="/color")
        app.include_router(color_commands_router, prefix="/color")
        app.include_router(color_assign_q_router, prefix="/color-assign")
        app.include_router(color_assign_commands_router, prefix="/color-assign")
