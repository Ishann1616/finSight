from fastapi import FastAPI
from fuckArounds.practice import User,Gender,Role
from typing import List
from uuid import uuid4

app= FastAPI()

db: List[User] = [
    User(
        id=uuid4(),
        first_name="Ishan",
        last_name="Dewangan",
        middle_name="",
        gender=Gender.male,
        role=[Role.admin]
    ),   
    User(
        id=uuid4(),
        first_name="Sidarth",
        last_name="Guptrog",
        middle_name="",
        gender=Gender.male,
        role=[Role.student,Role.user]
    )
]
@app.get("/api/v1/users")
async def root():
    return db

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id:UUID):
    for user in db:
        if user.id==uuid4:
            db.remove(user)
            return



@app.post("/api/v1/users")
async def register_user(user:User):
    db.append(user)
    return {"id":user.id}



@app.get("/")
async def root():
    return {"Hello":"friend"}