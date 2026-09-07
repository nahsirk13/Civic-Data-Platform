"""
API routes for the Representative resource.

Handles reading representative data from the database and
returning it in the shape defined by our Pydantic schemas.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.representative import Representative
from schemas.representative import RepresentativeOut

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


@router.get("/representatives", response_model=list[RepresentativeOut])
def get_representatives(state: str | None = None, db: Session = Depends(get_db)):
    """
    Get all representatives, optionally filtered by state.
    Example: GET /representatives?state=NY
    """
    query = db.query(Representative)
    if state:
        query = query.filter(Representative.state == state.upper())
    return query.all()


@router.get("/representatives/{rep_id}", response_model=RepresentativeOut)
def get_representative(rep_id: int, db: Session = Depends(get_db)):
    """
    Get a single representative by their ID.
    """
    rep = db.query(Representative).filter(Representative.id == rep_id).first()
    if not rep:
        raise HTTPException(status_code=404, detail="Representative not found")
    return rep