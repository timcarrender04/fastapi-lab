# FastAPI CRUD lab

A small items API you can run and hit. Clone it into `~/docker-course/fastapi-lab`. Leave your from-scratch app in `~/docker-course/fastapi-app` alone.

The item list lives in the process. Stop the server and the list goes back to the two seed items the next time you start it. Postgres is next week.

## Setup

```bash
cd ~/docker-course/fastapi-lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The prompt must show `(.venv)` before the `$`. Open http://localhost:8000/docs

## Routes

| Method | Path | Status | What it does |
|---|---|---|---|
| GET | `/` | 200 | Hello check |
| GET | `/items` | 200 | List items |
| GET | `/items/{item_id}` | 200 or 404 | One item |
| POST | `/items` | 201 or 422 | Add an item. Body is `name` and `price` |
| PUT | `/items/{item_id}` | 200, 404, or 422 | Replace `name` and `price` |
| DELETE | `/items/{item_id}` | 204 or 404 | Remove an item. Empty body |
| GET | `/users` | 200, 401, or 422 | List users. Needs `X-Token: secret-token` |
| POST | `/users` | 201, 401, or 422 | Add a user. Same token |

A missing `X-Token` on `/users` is 422. A wrong token is 401.

## Try the full cycle

Use a second terminal. Leave uvicorn running in the first.

```bash
curl http://localhost:8000/items

curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "eraser", "price": 1.25}'

curl http://localhost:8000/items/3

curl -X PUT http://localhost:8000/items/3 \
  -H "Content-Type: application/json" \
  -d '{"name": "eraser pack", "price": 2.00}'

curl -i -X DELETE http://localhost:8000/items/3
```

A POST with valid JSON and no `Content-Type: application/json` header comes back `json_invalid`. The body was fine. The header was the bug.

```bash
curl -i -X POST http://localhost:8000/items \
  -d '{"name": "Widget", "price": 9.99}'
```

## Tests

From the lab folder, with the venv active:

```bash
pytest
```

That runs create, list, get, update, delete, a missing id (404), and a bad body (422).

## Docker

Stop uvicorn first so port 8000 is free.

```bash
docker build -t fastapi-lab .
docker run -d -p 8000:8000 --name fastapi-lab fastapi-lab
curl http://localhost:8000/items
docker stop fastapi-lab && docker rm fastapi-lab
```

The image listens on `0.0.0.0`. Without that, `docker run -p` cannot reach uvicorn.
