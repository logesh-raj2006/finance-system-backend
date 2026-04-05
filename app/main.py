from fastapi import FastAPI
from .database import engine, Base
from .routes import transactions, users, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance System API")

app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(analytics.router)