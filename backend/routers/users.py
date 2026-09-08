"""
API routes for user signup and login.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from schemas.user import UserCreate, UserOut, UserLogin
from auth_utils import hash_password, verify_password, create_access_token, get_current_user_id

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", response_model=UserOut, status_code=201)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account. Hashes the password before storing it.
    """
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        dob=user_data.dob,
        password_hash=hash_password(user_data.password),
        zipcode=user_data.zipcode,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Verify a user's email and password, and return a JWT access token
    if valid.
    """
    user = db.query(User).filter(User.email == credentials.email).first()

    # if user does not exist or password verify password (in auth_utils) returns False
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserOut)
def get_current_user(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """
    Returns the profile of the currently authenticated user.
    Requires a valid JWT in the Authorization header.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user