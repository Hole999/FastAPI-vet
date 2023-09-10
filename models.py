from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class VetIn(BaseModel):
    username: str
    email: str
    password: str

class VetDb(BaseModel):
    id: Optional[str]  
    username: str
    email: str
    hashed_password: str

class AnimalIn(BaseModel):
    name: str
    species: str
    breed: Optional[str]
    owner: str

class AnimalDb(AnimalIn):
    _id: Optional[str]  
    vet_username: str


class TreatmentIn(BaseModel):
    description: str
    medication: str
    duration: str

class TreatmentDb(TreatmentIn):
    _id: str
    animal_id: str
    vet_username: str
