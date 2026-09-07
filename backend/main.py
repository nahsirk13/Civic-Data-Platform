from fastapi import FastAPI
from schemas.representative import Representative
from schemas.issue import Issue
#from models.issue import Issue
#from models.representative import Representative


app = FastAPI()

representatives = [
    {
        "id": 1,
        "name": "Steven Raga",
        "office": "NY State Assembly",
        "district": "30"
    },
    {
        "id": 2,
        "name": "Aber Kawas",
        "office": "NY State Senate",
        "district": "12"
    }
]

issues = [
    {
        "id": 1,
        "name": "Medicare for All",
        "description": "Universal health care and single payer systems",
        "important_representative_ids": [1]
    },
    {
        "id": 2,
        "name": "Israel Palestine",
        "description": "Question of allegiance, funding, or divestment from Israel, and supporting"
                       "the Palestinian liberation movement",
        "important_representative_ids": [2]
    }
]


@app.get("/")
def root():
    return {"message": "Civic Data API running"}


@app.get("/representatives", response_model=list[Representative])
def get_representatives():
    return representatives


@app.get("/issues", response_model=list[Issue])
def get_issues():
    return issues
