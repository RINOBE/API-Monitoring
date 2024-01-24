# main.py
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from models import Base,User
from databases import engine,get_db,get_db_synch
from security import get_password_hash
from routes import router  # Importez le routeur depuis le fichier routes
import uvicorn
def create_admin_user_on_startup():
    db = get_db_synch()
    Base.metadata.create_all(bind=engine)  # Assurez-vous que la base de données est bien initialisée

    # Vérifiez si la table d'utilisateurs est vide
    user_count = db.query(User).count()
    
    if user_count == 0:
        # Si la table d'utilisateurs est vide, ajoutez un utilisateur "ADMIN" avec le mot de passe hashé
        hashed_password = get_password_hash("Test2001")
        admin_data = User(username="ADMIN", password=hashed_password)
        db.add(admin_data)
        db.commit()
        db.refresh(admin_data)

# Appelez la fonction pour créer l'utilisateur "ADMIN" au démarrage
create_admin_user_on_startup()
app = FastAPI()


        
origins = [
    "http://localhost:5173",  # Adresse de votre application React
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ajoutez les routes du routeur ici
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, ws_ping_interval=300,ws_ping_timeout=300,reload=True)