import os
import requests
from dotenv import load_dotenv
from fastapi import APIRouter

load_dotenv()


router = APIRouter()

OPENSTATES_API_KEY = os.getenv("OPENSTATES_API_KEY")
print("API KEY LOADED:", OPENSTATES_API_KEY)

@router.get("/openstates/test")
def openstates_test():
    """
    Quick proof-of-concept: pulls real legislative data
    for a NY State Assembly member from the Open States API.
    """
    response = requests.get(
        "https://v3.openstates.org/people",
        params={"jurisdiction": "New York", "name": "Steven Raga", "apikey": OPENSTATES_API_KEY},
    )
    return response.json()


@router.get("/openstates/recent-bills")
def recent_bills(name: str = "Steven Raga", jurisdiction: str = "New York"):
    people_response = requests.get(
        "https://v3.openstates.org/people",
        params={"jurisdiction": jurisdiction, "name": name, "apikey": OPENSTATES_API_KEY},
    )
    print("PEOPLE STATUS:", people_response.status_code)
    print("PEOPLE BODY:", people_response.json())

    people = people_response.json().get("results", [])
    if not people:
        return {"bills": []}

    person_id = people[0]["id"]
    bills_response = requests.get(
        "https://v3.openstates.org/bills",
        params={
            "sponsor": person_id,
            "jurisdiction": jurisdiction,
            "sort": "updated_desc",
            "per_page": 3,
            "apikey": OPENSTATES_API_KEY,
        },
    )
    return bills_response.json()