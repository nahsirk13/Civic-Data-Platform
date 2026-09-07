from pydantic import BaseModel


class Representative(BaseModel):
    id: int
    name: str
    office: str
    district: str
