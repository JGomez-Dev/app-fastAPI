from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"],
                   responses={404 : {"message": "No encontrado"}})

# Iniciar el server: python -m uvicorn users:app --reload

@router.get("/usersjson")
async def usersjson():
    return [{"name" : "Javier", "surname": "Gomez", "email" : "javier@gmail.com", "age": 33},
            {"name" : "Eduardo", "surname": "Gomez", "email" : "eduardo@gmail.com", "age": 30},
            {"name" : "Alba", "surname": "Alvaro", "email" : "alba@gmail.com", "age": 12}]


class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    age: int

users_list = [User(id = 1 , name = "Javier", surname =  "Gomez", email=  "javier@gmail.com",age= 33),
         User(id = 2 ,name = "Eduardo",surname =  "Gomez", email= "eduardo@gmail.com", age= 30),
         User(id = 3 ,name = "Alba", surname = "Alvaro", email= "alba@gmail.com", age= 12)]

@router.get("/users")
async def users():
    return users_list

#Path
@router.get("/user/{id}")
async def users(id: int):
     return search_user(id = id)

# Query
# http://127.0.0.1:8000/userquery/?id=1
@router.get("/user/")
async def users(id: int):
    return search_user(id = id)
    
@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    
    users_list.append(user)
    return user

@router.put("/user/")
async def user(user: User):
    found = False

    for index, saved_user in enumerate(users_list):
        if(saved_user.id == user.id):
            users_list[index] = user
            found = True

    if not found:
        return {"error": "No se ha actualizado el usuario"}
   
    return user

@router.delete("/user/{id}")
async def user(id: int):
     found = False
     for index, saved_user in enumerate(users_list):
        if(saved_user.id == id):
            del users_list[index]
            found = True
   
     if not found:
        return {"error": "No se ha elimnado el usuario"}


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except: 
        return {"error": "No se ha encontrado el usuario"}
    


