from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
# Generacion de token aleatorio: openssl rand -hex 32
SECRET = "728470b711131d49dcafe3667150a5fe"

router = APIRouter(tags=["oauth"])

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "$2a$12$Uke.LL1hhziEGkILYubdLuBiBJhYoy7DfavdZLb.d1lubwHuGl8De"
    },
    "javier2": {
        "username": "javier2",
        "fullname": "Javier Gomez 2",
        "email": "javiergomez2@gmail.com",
        "disable": True,
        "password": "$2a$12$n5yLPJMIagoFnFoMNZc8gOpuIZTpSpmZ.KWorULp6fkFlbqRKfNDK"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales de autenticación inválidas", 
                            headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
              raise exception
        
    except JWTError:  
           raise exception
     
    return search_user(username = username)


async def current_user(user: User = Depends(auth_user)):

    if user.disable:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo", 
                            headers={"WWW-Authenticate": "Bearer"})

    return user

@router.post("/loginjwt")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    
    user_db = users_db.get(form.username)
    
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
     
    user = search_user_db(form.username)
     
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {
        "sub" : user.username, 
        "exp" : datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION) 
        }

    return {"access_token": jwt.encode(claims=access_token, key= SECRET, algorithm=ALGORITHM), "token_type" : "bearer"}



@router.get("/users/mejwt")
async def me(user: User = Depends(current_user)):
    return user



