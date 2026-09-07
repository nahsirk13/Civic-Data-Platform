from sqlalchemy import Column, Integer, String
from database import Base


class Issue(Base):
    """
    Represents a political/policy issue (e.g. "Medicare for All")
    that representatives can be linked to via RepresentativeIssue.
    """
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)