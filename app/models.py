from sqlalchemy import Column, Integer, String, Float

from app.database import Base


class Product(Base):
    """Задание 9.1 — модель ресурса Product.

    Поле description добавляется во второй миграции и является NOT NULL.
    """

    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False, default=0)
    description = Column(String(1000), nullable=False)
