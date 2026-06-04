"""Эндпоинты, которые демонстрируют кастомные исключения (задание 10.1/10.2)."""

from fastapi import APIRouter

from app.exceptions import CustomExceptionA, CustomExceptionB

router = APIRouter(prefix="/demo", tags=["errors-demo"])

_resources = {1: "alpha", 2: "beta"}


@router.get("/check/{value}")
def check_value(value: int):
    # CustomExceptionA вызывается, если не выполнено условие.
    if value <= 0:
        raise CustomExceptionA("Value must be greater than zero")
    return {"value": value, "ok": True}


@router.get("/resource/{resource_id}")
def get_resource(resource_id: int):
    # CustomExceptionB вызывается, если ресурс не найден.
    if resource_id not in _resources:
        raise CustomExceptionB(f"Resource {resource_id} does not exist")
    return {"id": resource_id, "name": _resources[resource_id]}
