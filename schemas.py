# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List

# Modèle Pydantic pour la validation des données postées
class DataEntryCreate(BaseModel):
    cpu_usage: float
    ram_available: float
    ram_total: float
    disk_available: float
    disk_total: float
    ip_address: str  # Champ IP_address
class NetworkPydantic(BaseModel):
    ip_address:str
    created_at:str
    upload_speed:float
    download_speed:float

class NetworkPydanticReponse(BaseModel):
    data:List[NetworkPydantic]
class DataEntryPydantic(BaseModel):
    cpu_usage: float
    ram_available: float
    ram_total: float
    disk_available: float
    disk_total: float
    ip_address: str
    created_at: str  # Convert the datetime to string for response
class DataEntryResponse(BaseModel):
    data: List[DataEntryPydantic]
class User_schema(BaseModel):
    username: str
    password: str
class User_schema_pydantic(BaseModel):
    username:str
    password:str
class UsersReponse(BaseModel):
    data:List[User_schema_pydantic]
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None