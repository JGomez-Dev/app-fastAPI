from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(tags=["oauth"])

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disable: bool

class UserDB(User):
    password: str

users_db = {
    "javier": {
        "username": "javier",
        "fullname": "Javier Gomez",
        "email": "javiergomez@gmail.com",
        "disable": False,
        "password": "1234"
    },
    "javier2": {
        "username": "javier2",
        "fullname": "Javier Gomez 2",
        "email": "javiergomez2@gmail.com",
        "disable": True,
        "password": "4321"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user =  search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales de autenticación inválidas", 
                            headers={"WWW-Authenticate": "Bearer"})
    
    if user.disable:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo", 
                            headers={"WWW-Authenticate": "Bearer"})

    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
     user_db = users_db.get(form.username)
     if not user_db:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
     
     user = search_user_db(form.username)
     if not form.password == user.password:
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta"
            )
     
     return {"access_token": user.username, "token_type" : "bearer"}



@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

         
