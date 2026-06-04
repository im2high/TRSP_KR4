"""Задание 10.1 / 10.2 — пользовательские исключения и обработчики."""

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas import ErrorResponse


class CustomExceptionA(Exception):
    """Бизнес-условие не выполнено."""

    status_code = status.HTTP_400_BAD_REQUEST
    error = "BusinessRuleViolation"

    def __init__(self, message: str = "Business rule was violated"):
        self.message = message
        super().__init__(message)


class CustomExceptionB(Exception):
    """Ресурс не найден."""

    status_code = status.HTTP_404_NOT_FOUND
    error = "ResourceNotFound"

    def __init__(self, message: str = "Requested resource not found"):
        self.message = message
        super().__init__(message)


def _log(message: str) -> None:
    # В реальном проекте здесь был бы logging. Для КР достаточно print.
    print(f"[ERROR] {message}")


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(CustomExceptionA)
    async def handle_custom_a(request: Request, exc: CustomExceptionA):
        _log(f"CustomExceptionA on {request.url.path}: {exc.message}")
        body = ErrorResponse(
            error=exc.error,
            message=exc.message,
            status_code=exc.status_code,
        )
        return JSONResponse(status_code=exc.status_code, content=body.model_dump())

    @app.exception_handler(CustomExceptionB)
    async def handle_custom_b(request: Request, exc: CustomExceptionB):
        _log(f"CustomExceptionB on {request.url.path}: {exc.message}")
        body = ErrorResponse(
            error=exc.error,
            message=exc.message,
            status_code=exc.status_code,
        )
        return JSONResponse(status_code=exc.status_code, content=body.model_dump())

    # Задание 11.1 / 10.2 — кастомная обработка ошибок валидации.
    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        _log(f"Validation error on {request.url.path}: {exc.errors()}")
        body = ErrorResponse(
            error="ValidationError",
            message="Request validation failed",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"errors": jsonable_encoder(exc.errors())},
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=body.model_dump(),
        )
