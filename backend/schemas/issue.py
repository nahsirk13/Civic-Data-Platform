from pydantic import BaseModel

class Issue(BaseModel):
    id: int
    name: str
    description: str
    important_representative_ids: list[int]
