from bson import ObjectId
from pydantic import BaseModel
import datetime
import json
from typing import Optional

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class Task(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    status: str = "pending"
    class Config:
        
        json_encoders = {
            ObjectId: str  
        }

class titleUpdate(BaseModel):
    title: Optional[str] = None

class descriptionUpdate(BaseModel):
    description :Optional[str] = None

class statusUpdate(BaseModel):
    status: Optional[str] = None

class User(BaseModel):
    username: str
    password: str
