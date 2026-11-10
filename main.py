from fastapi import FastAPI

from routers import items, users

app = FastAPI(title="FastAPI CRUD Lab")


@app.get("/")
def read_root():
    # GET / is the health check. It does not touch the item list.
    return {"hello": "fastapi"}


app.include_router(items.router)
app.include_router(users.router)
