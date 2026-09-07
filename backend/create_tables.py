from database import engine, Base

from models.representative import Representative
from models.user import User
from models.issue import Issue
from models.representative_issue import RepresentativeIssue

Base.metadata.create_all(bind=engine)

print("Tables created successfully.")