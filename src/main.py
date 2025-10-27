from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
# Это нужно сделать до импорта модулей, которые их используют
load_dotenv()

from fastapi import FastAPI
from .routes import users, articles, comments

app = FastAPI(
    title="Blog Platform API",
    description="A simple API for a blog platform.",
    version="1.0.0",
)

@app.get("/healthz", tags=["Health Check"])
def health_check():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(users.router)
app.include_router(articles.router)
app.include_router(comments.router)

