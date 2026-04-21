from fastapi import FastAPI
from src.routers import clothes, users
from fastapi.staticfiles import StaticFiles
from src.routers import outfit_router


app = FastAPI()
app.include_router(outfit_router.router)
app.include_router(clothes.router)
app.include_router(users.router)

app.mount("/uploads", StaticFiles(directory="src/uploads"), name="uploads")

app.include_router(clothes.router)
@app.get("/")
def root():
    return {"Smart Closet backend running"}


