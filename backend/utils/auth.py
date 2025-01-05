from jose import JWTError
import jwt
from fastapi import HTTPException, Depends, Query
from datetime import datetime, timedelta
import logging
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from bson import ObjectId
from bson.errors import InvalidId
from routers.models import User
# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SECRET_KEY = "87c4334d2c14b86a7d1d88f1acf9a5baa93b2ee011301f4481a37007906db5fc"
ALGORITHM = "HS256"

def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token and check the "sub" claim
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return User(username=username)
    except JWTError:
        raise credentials_exception

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Query(...)):
    logger.info(f"Decoding token: {token}")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            logger.error("Missing subject in token")
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        logger.info(f"Authenticated user: {username}")
        return username
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError as e:
        logger.error(f"Token decoding failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")