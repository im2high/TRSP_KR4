from fastapi import FastAPI

from app.config import settings
from app.exceptions import register_exception_handlers
from app.routers import demo_errors, products, users


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    register_exception_handlers(app)

    app.include_router(products.router)
    app.include_router(users.router)
    app.include_router(demo_errors.router)

    @app.get("/health", tags=["system"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
