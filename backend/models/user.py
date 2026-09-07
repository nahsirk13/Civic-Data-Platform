from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    """
    Represents an app user who can sign up, log in, and view
    representatives relevant to their ZIP code.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    zipcode = Column(String)
