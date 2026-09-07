"""
Pydantic schemas for the Representative resource.

These define the *shape* of data going in and out of the API —
separate from the SQLAlchemy model, which defines the database
table structure. This separation lets us control exactly what
gets exposed via the API without being tied to internal DB columns.
"""

from pydantic import BaseModel, field_validator

valid_levels = {"city", "state", "federal"}


class RepresentativeOut(BaseModel):
    id: int
    name: str
    level: str  # "city", "state", or "federal"
    chamber: str | None = None  # e.g. "Senate", "Assembly" — null where not applicable
    office: str  # specific institution/title
    district: str | None = None  # string, not int — not all districts are numeric
    state: str | None = None  # null for federal-level offices representing the whole country

    class Config:
        # Allows this schema to be built directly from a SQLAlchemy
        # model instance (e.g. db.query(Representative).first()),
        # not just from a raw dict/JSON.
        from_attributes = True


class RepresentativeCreate(BaseModel):
    """
    Shape of data required to CREATE a new Representative
    (e.g. in a POST /representatives request body).
    No 'id' field — the database assigns that automatically.
    """
    name: str
    level: str
    chamber: str | None = None
    office: str
    district: str | None = None
    state: str | None = None

    @field_validator("state")
    @classmethod
    def validate_state(cls, value):
        """
        Ensures 'state' is a valid 2-letter abbreviation (e.g. 'NY').
        Runs automatically whenever a RepresentativeCreate object
        is built, before the request even reaches the router logic.
        """
        if value is not None:
            if len(value) != 2 or not value.isalpha():
                raise ValueError("state must be a 2-letter abbreviation (e.g. 'NY')")
            return value.upper()  # normalize to uppercase automatically
        return value

    @field_validator("state")
    @classmethod
    def validate_state(cls, value):
        """
        Ensures 'state' is a valid 2-letter abbreviation (e.g. 'NY').
        Runs automatically whenever a RepresentativeCreate object
        is built, before the request even reaches the router logic.
        """
        if value is not None:
            if len(value) != 2 or not value.isalpha():
                raise ValueError("state must be a 2-letter abbreviation (e.g. 'NY')")
            return value.upper()  # normalize to uppercase automatically
        return value  # if null, just return the None that was passed in

    @field_validator("level")
    @classmethod
    def validate_level(cls, value):
        """
        Ensures 'level' either city, state, or federal.
        """
        if value.lower() not in valid_levels:
            raise ValueError(f"level must be one of the following: {valid_levels}")
        return value.lower()
