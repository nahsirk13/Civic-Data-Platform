from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from database import Base


class UserIssue(Base):
    """
    Junction table linking a User to an Issue they've marked
    as important to them.
    """
    __tablename__ = "user_issues"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    issue_id = Column(Integer, ForeignKey("issues.id"))