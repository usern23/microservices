from dotenv import load_dotenv

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

app.include_router(users.router)
app.include_router(articles.router)
app.include_router(comments.router)

