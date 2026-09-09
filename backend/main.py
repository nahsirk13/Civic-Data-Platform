"""
Main FastAPI application entry point.
Wires together all routers.
"""

from fastapi import FastAPI
from routers import representatives, issues, users
from fastapi.middleware.cors import CORSMiddleware
from routers import openstates


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(openstates.router)
app.include_router(representatives.router)
app.include_router(issues.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Civic Data API running"}