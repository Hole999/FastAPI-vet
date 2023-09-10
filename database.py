import security
import motor.motor_asyncio
from decouple import config
from models import VetIn, AnimalDb, TreatmentDb
from bson import ObjectId

MONGODB_URL = config("MONGODB_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.vet_database


async def fetch_one_animal(animal_id: str):
    animal = await db.animals.find_one({"_id": ObjectId(animal_id)})
    if animal:
        animal["id"] = str(animal.pop("_id"))  
    return animal




async def fetch_all_animals():
    return await db.animals.find().to_list(100)

async def create_animal(animal: AnimalDb):
    animal_doc = animal.dict()
    insert_result = await db.animals.insert_one(animal_doc)
    return str(insert_result.inserted_id)  
 



async def fetch_vet(username: str):
    return await db.vets.find_one({"username": username})

async def create_vet(vet: VetIn):
    vet_doc = vet.dict()
    vet_doc["hashed_password"] = security.hash_password(vet.password)
    del vet_doc["password"]
    return await db.vets.insert_one(vet_doc)
async def fetch_vet_by_id(vet_id):
    vet = await db.vets.find_one({"_id": vet_id})
    if vet:
        vet["id"] = str(vet.pop("_id"))  
    return vet


async def delete_vet_from_db(vet_id: str):
    await db.vets.delete_one({"_id": ObjectId(vet_id)})

async def update_vet(vet_id: str, vet_data: dict):
    
    await db.vets.update_one({"_id": ObjectId(vet_id)}, {"$set": vet_data})



async def delete_animal_from_db(animal_id: str):
    await db.animals.delete_one({"_id": ObjectId(animal_id)})



async def update_animal_in_db(animal_id: str, animal_data: dict):
    try:
        await db.animals.update_one({"_id": ObjectId(animal_id)}, {"$set": animal_data})
    except Exception as e:
        print(f"Error updating animal: {e}")
        



async def fetch_one_treatment(treatment_id: str):
    treatment = await db.treatments.find_one({"_id": ObjectId(treatment_id)})
    return treatment


async def fetch_treatments_by_animal(animal_id: str):
    try:
        treatments = await db.treatments.find({"animal_id": animal_id}).to_list(length=100)
        return treatments
    except Exception as e:
        print(f"Error fetching treatments by animal: {e}")
        return []  



async def create_treatment(treatment: TreatmentDb):
    treatment_doc = treatment.dict()
    new_treatment = await db.treatments.insert_one(treatment_doc)
    return new_treatment.inserted_id

async def delete_treatment_from_db(treatment_id: str):
    await db.treatments.delete_one({"_id": ObjectId(treatment_id)})

async def update_treatment_in_db(treatment_id: str, treatment_data: dict):
    await db.treatments.update_one({"_id": ObjectId(treatment_id)}, {"$set": treatment_data})
