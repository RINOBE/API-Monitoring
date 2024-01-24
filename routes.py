# routes.py
from fastapi import HTTPException, Depends, status,WebSocket,APIRouter,WebSocketDisconnect,Path
from sqlalchemy.orm import Session
from schemas import DataEntryCreate, DataEntryResponse, DataEntryPydantic,NetworkPydantic,NetworkPydanticReponse
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from databases import SessionLocal, engine,get_db
from models import DataEntry,User,HistoryEntry,Network
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from schemas import User_schema,User_schema_pydantic,Token,TokenData,UsersReponse
from datetime import timedelta, datetime
from jose import JWTError, jwt
from json.decoder import JSONDecodeError
import json
from security import *
router = APIRouter()

@router.websocket("/crd/")
async def create_data_entry(websocket: WebSocket,current_user: User=Depends(get_current_user)):
    await websocket.accept()
    try:
        while True:
            try:
                server_ip=websocket.client.host
                data = await websocket.receive_text()
                data_dict = json.loads(data)
                data_dict["ip_address"]=server_ip
                db_data = DataEntry(**data_dict)
                db = SessionLocal()
                db.add(db_data)
                db.commit()
            except JSONDecodeError:
                pass
    except WebSocketDisconnect:
        pass
@router.websocket("/network/")
async def create_data_entry(websocket: WebSocket,current_user: User=Depends(get_current_user)):
    await websocket.accept()
    try:
        while True:
            server_ip=websocket.client.host
            data = await websocket.receive_text()
            data_dict=json.loads(data)
            data_dict["ip_address"]=server_ip
            db_data = Network(**data_dict)
            db = SessionLocal()
            db.add(db_data)
            db.commit()
            await websocket.send_text("Bien reçu")  # Utilisez 'await' pour envoyer le message
    except WebSocketDisconnect:
        pass
@router.websocket("/history/")
async def create_data_entry(websocket: WebSocket,current_user: User=Depends(get_current_user)):
    await websocket.accept()
    try:
        while True:
            server_ip= websocket.client.host
            data = await websocket.receive_text()
            try:
                data_dict = json.loads(data)
                data_dict["ip_address"]=server_ip

                history_entry = HistoryEntry(**data_dict)
            # Vous pouvez ajouter d'autres champs du modèle si nécessaire.
            
            # Créez une session SQLAlchemy
                db = SessionLocal()
            
            # Ajoutez l'entrée à la session
                db.add(history_entry)
            
            # Committez la transaction pour l'insérer dans la base de données
                db.commit()
            
            except JSONDecodeError:
                pass
            await websocket.send_text("Bien reçu")  # Utilisez 'await' pour envoyer le message
    except WebSocketDisconnect:
        pass

@router.post("/data/")
def create_data_entry(data_entry: DataEntryCreate,current_user: User=Depends(get_current_user)):
    db_data = DataEntry(**data_entry.dict())
    db = SessionLocal()
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    db.close()
    return db_data
# Route pour obtenir les données depuis la base de données
@router.get("/data/", response_model=DataEntryResponse)
def get_data_entries(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),current_user: User=Depends(get_current_user)):
    data_entries = db.query(DataEntry).offset(skip).limit(limit).all()

    # Convertissez les objets DataEntry en objets DataEntryPydantic
    data_entries_pydantic = [DataEntryPydantic(
        cpu_usage=entry.cpu_usage,
        ram_available=entry.ram_available,
        ram_total=entry.ram_total,
        disk_available=entry.disk_available,
        disk_total=entry.disk_total,
        ip_address=entry.ip_address,
        created_at=entry.created_at.isoformat(),
    ) for entry in data_entries]

    # Créez un objet DataEntryResponse avec la liste de données
    response = DataEntryResponse(data=data_entries_pydantic)
    return response
@router.get("/history")
def get_history_entries(db: Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    history_entries = db.query(HistoryEntry).all()
    return history_entries

# Route pour obtenir les dernières données pour chaque adresse IP
@router.get("/latest_data/")
def get_latest_data_entries(db: Session = Depends(get_db),current_user: User=Depends(get_current_user)):
    # Sous-requête pour obtenir la date maximale (la plus récente) pour chaque adresse IP
    subquery = db.query(DataEntry.ip_address, func.max(DataEntry.created_at).label("max_created_at")).group_by(DataEntry.ip_address).subquery()

    # Requête principale pour obtenir les enregistrements correspondant aux dates maximales
    latest_data_entries = db.query(DataEntry).join(subquery, and_(
        DataEntry.ip_address == subquery.c.ip_address,
        DataEntry.created_at == subquery.c.max_created_at
    )).all()

    # Convertissez les objets DataEntry en objets DataEntryPydantic pour la réponse
    data_entries_pydantic = [DataEntryPydantic(
        cpu_usage=entry.cpu_usage,
        ram_available=entry.ram_available,
        ram_total=entry.ram_total,
        disk_available=entry.disk_available,
        disk_total=entry.disk_total,
        ip_address=entry.ip_address,
        created_at=entry.created_at.isoformat(),
    ) for entry in latest_data_entries]
    # Créez un objet DataEntryResponse avec la liste de données
    response = DataEntryResponse(data=data_entries_pydantic)
    return response
# Route pour obtenir les dernières données pour chaque adresse IP
@router.get("/latest_data_network/")
def get_latest_data_entries_network(db: Session = Depends(get_db),current_user: User=Depends(get_current_user)):
    # Sous-requête pour obtenir la date maximale (la plus récente) pour chaque adresse IP
    subquery = db.query(Network.ip_address, func.max(Network.created_at).label("max_created_at")).group_by(Network.ip_address).subquery()

    # Requête principale pour obtenir les enregistrements correspondant aux dates maximales
    latest_data_entries = db.query(Network).join(subquery, and_(
        Network.ip_address == subquery.c.ip_address,
        Network.created_at == subquery.c.max_created_at
    )).all()

    # Convertissez les objets DataEntry en objets DataEntryPydantic pour la réponse
    network_entries_pydantic = [NetworkPydantic(
        ip_address=entry.ip_address,
        created_at=entry.created_at.isoformat(),
        upload_speed=entry.upload_speed,
        download_speed=entry.download_speed
    ) for entry in latest_data_entries]
    # Créez un objet DataEntryResponse avec la liste de données
    response = NetworkPydanticReponse(data=network_entries_pydantic)
    return response

@router.post("/register/")
def register_user(user: User_schema, db: Session = Depends(get_db),current_user: User=Depends(get_current_user)):
    # Vérifiez si l'utilisateur existe déjà
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="L'utilisateur existe déjà")
    # Hachez le mot de passe avant de le stocker
    hashed_password = pwd_context.hash(user.password)
    user_data = User(username=user.username, password=hashed_password)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {"status":"successfull add user","status_code":200,"data":user_data}
@router.get("/users")
def get_all_user(db: Session = Depends(get_db),current_user: User=Depends(get_current_user)):
    users=db.query(User).all()
    user_list=[User_schema_pydantic(username=entry.username,password=entry.password) for entry in users]
    response= UsersReponse(data=user_list)
    return response

@router.delete("/users/{user_name}")
def delete_user(user_name: str = Path(..., title="User name", description="name of the user to delete"),current_user: User=Depends(get_current_user)):
    db = SessionLocal()
    user = db.query(User).filter(User.username == user_name).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    db.close()
    return {"message": "User deleted successfully"}

# Route pour mettre à jour un utilisateur
@router.put("/users/{username}")
async def update_user(username: str, user_data: User_schema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    db_user.username=user_data.username
    db_user.password = get_password_hash(user_data.password)
    db.commit()
    db.refresh(db_user)
    return {"message": "Utilisateur mis à jour avec succès"}
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login ou mot de passe incorrecte",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
