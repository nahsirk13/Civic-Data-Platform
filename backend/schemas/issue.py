"""
Pydantic schemas for the Issue resource.

Defines the shape of data going in and out of the API for
policy issues — separate from the SQLAlchemy model.
"""

from pydantic import BaseModel

class Issue(BaseModel):
    """
    Shape of an Issue as returned BY the API.
    """
    id: int
    name: str
    description: str
