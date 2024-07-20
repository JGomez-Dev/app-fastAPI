from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix=("/usersdb"), 
                   tags=["usersdb"],
                   responses={status.HTTP_404_NOT_FOUND : {"message": "No encontrado"}})
# Iniciar el server: python -m uvicorn users:app --reload

@router.get("/usersjson")
async def usersjson():
    return [{"name" : "Javier", "surname": "Gomez", "email" : "javier@gmail.com", "age": 33},
            {"name" : "Eduardo", "surname": "Gomez", "email" : "eduardo@gmail.com", "age": 30},
            {"name" : "Alba", "surname": "Alvaro", "email" : "alba@gmail.com", "age": 12}]



@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

#Path
@router.get("/{id}")
async def users(id: str):
     return search_user("_id", ObjectId(id))

# Query
# http://127.0.0.1:8000/userquery/?id=1
@router.get("/userdb/")
async def users(id: str):
    return search_user("_id", ObjectId(id))
    
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    user_dic = dict(user)
    del user_dic["id"]

    id = db_client.users.insert_one(user_dic).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id":id}))

    return User(**new_user)

@router.put("/")
async def user(user: User):
    user_dic = dict(user)
    del user_dic["id"]
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dic )
    except:
        return {"error": "No se ha actualizado el usuario"}
   
    return search_user("_id", ObjectId(user.id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
     found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

     if not found:
         return {"error": "No se ha elimnado el usuario"}


def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except: 
        return {"error", "No se ha encontrado el usuario"}
    


