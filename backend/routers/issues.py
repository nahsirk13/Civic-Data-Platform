"""
API routes for the Issue resource.

Handles reading representative data from the database and
returning it in the shape defined by our Pydantic schemas.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import SessionLocal
from models.issue import Issue
from schemas.issue import IssueOut

router = APIRouter()

def get_db():
    """
    Provides a fresh database session for a single request,
    and guarantees it closes afterward, even if an error occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    @router.get("/issues", response_model=list[IssueOut])
    def get_issues(name: str | None = None, db: Session = Depends(get_db)):
        """
        Get all issues, optionally filtered by name.
        Example: GET /issues?name=Healthcare
        """
        query = db.query(Issue)
        if name is not None:
            query = query.filter(func.lower(Issue.name) == name.lower())
        return query.all()

