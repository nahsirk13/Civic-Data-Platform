import json
from database import SessionLocal
from models.representative import Representative

# Load both data files
with open("senators.json", "r") as f:
    senators_data = json.load(f)

with open("additional_reps.json", "r") as f:
    additional_data = json.load(f)

all_reps = senators_data + additional_data

# Open a database session
db = SessionLocal()

try:
    for rep_data in all_reps:
        rep = Representative(
            id=rep_data["id"],
            name=rep_data["name"],
            level=rep_data["level"],
            chamber=rep_data["chamber"],
            office=rep_data["office"],
            district=rep_data["district"],
            state=rep_data["state"],
        )
        db.add(rep)

    db.commit()
    print(f"Seeded {len(all_reps)} representatives successfully.")

except Exception as e:
    db.rollback()
    print(f"Error seeding data: {e}")

finally:
    db.close()
