from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from utils.db import users_collection
from utils.auth import create_access_token, get_current_user
from .models import User

router = APIRouter()

class RegisterUser(BaseModel):
    username: str
    password: str

@router.post("/register")
def register_user(user: User):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    users_collection.insert_one(user.dict())
    return {"message": "User registered successfully"}

@router.post("/token")
async def generate_token(user: User):
    db_user = users_collection.find_one({"username": user.username, "password": user.password})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}