"""
Main FastAPI application entry point.
Wires together all routers.
"""

from fastapi import FastAPI
from routers import representatives, issues, users

app = FastAPI()
app.include_router(representatives.router)
app.include_router(issues.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Civic Data API running"}