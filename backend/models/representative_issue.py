from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from database import Base


class RepresentativeIssue(Base):
    """
    Junction table linking representatives to issues, with an
    AI-generated stance score (1=left, 5=right) and summary.
    """
    __tablename__ = "representative_issues"

    id = Column(Integer, primary_key=True)
    representative_id = Column(Integer, ForeignKey("representatives.id"))
    issue_id = Column(Integer, ForeignKey("issues.id"))

    sponsored_count = Column(Integer, nullable=True,
                             default=0)  # bills sponsored/cosponsored/signed related to this issue
    authored_count = Column(Integer, nullable=True,
                            default=0)  # pieces of legislation they personally wrote related to this issue

    stance_score = Column(Integer, nullable=True)
    ai_summary = Column(String, nullable=True)

    __table_args__ = (
        CheckConstraint('stance_score >= 1 AND stance_score <= 5', name='stance_score_range'),
    )