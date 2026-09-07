"""
Pydantic schemas for the Users.

Defines the shape of data going in and out of the API for
users — separate from the SQLAlchemy model.
"""

from pydantic import BaseModel, field_validator
from datetime import date


class UserOut (BaseModel):
    """
    Shape of User as returned BY the API.
    Does NOT include password hash - never want to send that out
    """
    id: int
    email: str
    first_name: str
    last_name: str
    dob: date
    zipcode: str

    class Config:
        from_attributes = True


class UserCreate (BaseModel):
    """
    Shape of a User as required to sign a new user.
    """
    email: str
    first_name: str
    last_name: str
    dob: date
    password: str
    zipcode: str


    @field_validator("dob")
    @classmethod
    def validate_dob(cls, value):
        """
        Ensures date of birth is not a date in future.
        """
        if value < date.today():
            return value
        else:
            raise ValueError("Please select a date of birth before today.")


class UserLogin(BaseModel):
    """
    Shape of data required to log in an existing user.
    """
    email: str
    password: str

