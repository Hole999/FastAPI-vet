from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database import fetch_one_animal, fetch_all_animals, create_animal, fetch_vet, create_vet, delete_animal_from_db, fetch_one_treatment, fetch_treatments_by_animal, create_treatment, fetch_vet_by_id,delete_vet_from_db, update_animal_in_db, delete_treatment_from_db, update_treatment_in_db
from bson import ObjectId
from security import authenticate_vet, create_access_token, get_current_vet
from models import VetIn, AnimalIn, VetDb, AnimalDb, TreatmentDb, TreatmentIn
from typing import List

app = FastAPI()
ACCESS_TOKEN_EXPIRE_MINUTES = 45




@app.post("/vets/register", response_model=VetDb)
async def register_vet(vet: VetIn):
    db_vet = await fetch_vet(vet.username)
    if db_vet:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_vet = await create_vet(vet)
    created_vet = await fetch_vet_by_id(new_vet.inserted_id)
    return created_vet

@app.post("/vets/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    vet = await authenticate_vet(form_data.username, form_data.password)
    if not vet:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token = await create_access_token(data={"sub": vet['username']})
    return {"access_token": access_token, "token_type": "bearer"}

@app.delete("/vets/{vet_id}")
async def delete_vet(vet_id: str, current_vet: VetDb = Depends(get_current_vet)):
    await delete_vet_from_db(vet_id)
    return {"message": "Vet has been deleted"}



@app.put("/vets/{vet_id}", response_model=VetDb)
async def update_vet(vet_id: str, vet: VetIn, current_vet: VetDb = Depends(get_current_vet)):
    if vet_id != current_vet["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this vet")
    vet_data = vet.dict()
    await update_vet(vet_id, vet_data)
    return await fetch_vet_by_id(vet_id)


@app.post("/animals/")
async def add_animal(animal: AnimalIn, current_vet: VetDb = Depends(get_current_vet)):
    animal_id = str(ObjectId()) 
    await create_animal(AnimalDb(**animal.dict(), id=animal_id, vet_username=current_vet['username']))
    return {"inserted_id": animal_id}




@app.get("/animals/{animal_id}", response_model=AnimalDb)
async def get_single_animal(animal_id: str, current_vet: VetDb = Depends(get_current_vet)):
    return await fetch_one_animal(animal_id)

@app.get("/animals/", response_model=List[AnimalDb])
async def get_all_animals(current_vet: VetDb = Depends(get_current_vet)):
    return await fetch_all_animals()


@app.delete("/animals/{animal_id}")
async def delete_animal(animal_id: str, current_vet: VetDb = Depends(get_current_vet)):
    animal = await fetch_one_animal(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    if animal['vet_username'] != current_vet['username']:
        raise HTTPException(status_code=403, detail="Not authorized to delete this animal")
    await delete_animal_from_db(animal_id)
    return {"message": "Animal has been deleted"}


@app.put("/animals/{animal_id}", response_model=AnimalDb)
async def update_animal(animal_id: str, animal: AnimalIn, current_vet: VetDb = Depends(get_current_vet)):
    animal_data = await fetch_one_animal(animal_id)
    if not animal_data:
        raise HTTPException(status_code=404, detail="Animal not found")
    if animal_data['vet_username'] != current_vet['username']:
        raise HTTPException(status_code=403, detail="Not authorized to update this animal")
    await update_animal_in_db(animal_id, animal.dict())
    return await fetch_one_animal(animal_id)


@app.post("/animals/{animal_id}/treatments/")
async def add_treatment(treatment: TreatmentIn, animal_id: str, current_vet: VetDb = Depends(get_current_vet)):
    generated_id = "some_generated_id"
    treatment_db = TreatmentDb(
        **treatment.dict(),
        id=generated_id,
        animal_id=animal_id,
        vet_username=current_vet['username']
    )
    treatment_id = await create_treatment(treatment_db)
    return {"inserted_id": str(treatment_id)}

@app.get("/animals/{animal_id}/treatments/", response_model=List[TreatmentDb])
async def get_treatments(animal_id: str, current_vet: VetDb = Depends(get_current_vet)):
    return await fetch_treatments_by_animal(animal_id)

@app.delete("/treatments/{treatment_id}")
async def delete_treatment(treatment_id: str, current_vet: dict = Depends(get_current_vet)):
    treatment = await fetch_one_treatment(treatment_id)
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")
    if treatment['vet_username'] != current_vet['username']:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this treatment")
    await delete_treatment_from_db(treatment_id)
    return {"message": "Treatment has been deleted"}

from fastapi.responses import JSONResponse

@app.put("/treatments/{treatment_id}")
async def update_treatment(treatment_id: str, treatment: TreatmentDb, current_vet: dict = Depends(get_current_vet)):
    treatment_data = await fetch_one_treatment(treatment_id)
    if not treatment_data:
        raise HTTPException(status_code=404, detail="Treatment not found")

    if current_vet['username'] != treatment_data['vet_username']:
        raise HTTPException(status_code=403, detail="You don't have permission to update this treatment")

    allowed_fields = {
        "description": treatment.description,
        "medication": treatment.medication,
        "duration": treatment.duration,
    }

    await update_treatment_in_db(treatment_id, allowed_fields)

    return JSONResponse(content={"message": "Treatment has been updated"})
