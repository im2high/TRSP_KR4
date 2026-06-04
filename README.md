# Контрольная работа №4 — Технологии разработки серверных приложений

Приложение на **FastAPI**, объединяющее задания 9.1, 10.1, 10.2, 11.1, 11.2:

- **9.1** — миграции БД через Alembic, модель `Product`.
- **10.1 / 10.2** — пользовательские исключения, обработчики и Pydantic-модели ответов об ошибках.
- **11.1** — валидация данных пользователя (`conint`, `EmailStr`, `constr`) + кастомный обработчик ошибок валидации, тесты через `TestClient`.
- **11.2** — асинхронные тесты эндпоинтов через `httpx.AsyncClient` + `ASGITransport` + `Faker`.

## Структура проекта

```
app/         — код приложения (роутеры, модели, схемы, исключения)
migrations/  — миграции Alembic
tests/       — модульные и асинхронные тесты
```

## Установка зависимостей

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Скопируйте файл с переменными окружения:

```bash
cp .env.example .env
```

По умолчанию используется SQLite (`sqlite:///./app.db`) — никаких внешних сервисов не нужно.

## Запуск приложения

```bash
# 1. Применить миграции (создаст таблицу product с полем description)
alembic upgrade head

# 2. Запустить сервер
uvicorn app.main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs
- Health-check: http://127.0.0.1:8000/health

## Запуск в Docker (PostgreSQL)

```bash
docker compose up --build
```

Приложение поднимется вместе с PostgreSQL, миграции применятся автоматически.
В контейнере используется драйвер **psycopg 3** (`postgresql+psycopg://...`),
который ставится готовым wheel и не требует сборки из исходников.

## Локальный запуск с PostgreSQL (опционально)

Если хотите гонять Postgres без Docker, установите драйвер отдельно:

```bash
pip install "psycopg[binary]==3.2.3"
```

и укажите в `.env`:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/kr4
```

## Работа с миграциями (задание 9.1)

```bash
# Применить все миграции
alembic upgrade head

# Откатить последнюю миграцию (вернёт схему без description)
alembic downgrade -1

# Создать новую автогенерируемую миграцию
alembic revision --autogenerate -m "message"
```

Готовые миграции:
1. `0001_create_product_table` — создаёт таблицу `product` (`id`, `title`, `price`, `count`).
2. `0002_add_description_to_product` — добавляет `description` (NOT NULL).

### Добавление двух записей (п.5 задания)

Через API после `alembic upgrade head`:

```bash
curl -X POST http://127.0.0.1:8000/products \
  -H "Content-Type: application/json" \
  -d '{"title":"Coffee","price":9.99,"count":10,"description":"Arabica"}'

curl -X POST http://127.0.0.1:8000/products \
  -H "Content-Type: application/json" \
  -d '{"title":"Tea","price":4.50,"count":20,"description":"Green tea"}'
```

Либо напрямую в SQLite после первой миграции:

```sql
INSERT INTO product (title, price, count) VALUES ('Coffee', 9.99, 10);
INSERT INTO product (title, price, count) VALUES ('Tea', 4.50, 20);
```

## Проверка основной функциональности

| Сценарий | Запрос |
|---|---|
| Создать продукт | `POST /products` |
| Список продуктов | `GET /products` |
| Продукт не найден (CustomExceptionB) | `GET /products/999` |
| Нарушение бизнес-правила (CustomExceptionA) | `GET /demo/check/0` |
| Ресурс не найден (CustomExceptionB) | `GET /demo/resource/999` |
| Валидация пользователя | `POST /users/validate` |
| CRUD пользователей (in-memory) | `POST/GET/DELETE /users` |

## Тестирование

Запуск всех тестов:

```bash
pytest
```

Запуск отдельных наборов:

```bash
# Задание 11.1 — валидация и кастомные ошибки (TestClient)
pytest tests/test_validation.py -v

# Задание 11.2 — асинхронные тесты (httpx.AsyncClient + Faker)
pytest tests/test_users_async.py -v
```

Все тесты должны завершиться статусом **passed**.
