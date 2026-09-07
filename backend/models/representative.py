from sqlalchemy import Column, Integer, String
from database import Base


class Representative(Base):
    """
    Represents a public official (city, state, or federal level).
    Chamber, district, and state are nullable since not every
    office type uses all of them (e.g. executive/judicial roles,
    city council seats, or Nebraska's unicameral legislature).
    """
    __tablename__ = "representatives"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    level = Column(String)  # "city", "state", "federal"
    chamber = Column(String, nullable=True)  # e.g. "Assembly", "Senate", "Congress" — null for executive/judicial/unicameral Nebraska/city
    office = Column(String)  # specific institution/title, e.g. "NY State Assembly", "Mayor", etc.
    district = Column(String, nullable=True)  # most times a number but sometimes has letters
    state = Column(String, nullable=True)  # null for federal-level offices representing the whole country
