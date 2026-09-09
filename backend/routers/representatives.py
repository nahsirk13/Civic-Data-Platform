"""
API routes for the Representative resource.

Handles reading representative data from the database and
returning it in the shape defined by our Pydantic schemas.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.representative import Representative
from schemas.representative import RepresentativeOut, RepresentativeCreate

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
    if state is not None:
        query = query.filter(Representative.state == state.upper())
    return query.all()


@router.get("/representatives/lookup", response_model=list[RepresentativeOut])
def lookup_representatives(
    district: str | None = None,
    state: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Look up representatives by district and/or state.
    Example: GET /representatives/lookup?district=30&state=NY
    """
    query = db.query(Representative)
    if state:
        query = query.filter(Representative.state == state.upper())
    if district:
        query = query.filter(Representative.district == district)
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


@router.post("/representatives/", response_model=RepresentativeCreate, status_code=201)
def create_representative(rep_data: RepresentativeOut, db: Session = Depends(get_db)):
    """
    Create a new representative. Returns new representative.
    """
    new_rep = Representative(
        name=rep_data.name,
        level=rep_data.level,
        chamber=rep_data.chamber,
        office=rep_data.office,
        district=rep_data.district,
        state=rep_data.state
    )
    db.add(new_rep)
    db.commit()
    db.refresh(new_rep)
    return new_rep

