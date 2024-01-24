# models.py
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy import orm
from databases import engine
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()
        
class DataEntry(Base):
    __tablename__ = "ressources"

    id = Column(Integer, primary_key=True, index=True)
    cpu_usage = Column(Float)
    ram_available = Column(Float)
    ram_total = Column(Float)
    disk_available = Column(Float)
    disk_total = Column(Float)
    ip_address = Column(String)  # Ajout du champ IP_address
    created_at = Column(DateTime, default=datetime.now)
# Modèle SQLAlchemy pour la nouvelle table "history"
class HistoryEntry(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String)
    command = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    user = Column(String)
# Modèle SQLAlchemy pour la nouvelle table "users"
class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    password = Column(String)
# Modèle SQLAlchemy pour la nouvelle table "users"
class Network(Base):
    __tablename__ = "network"
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String)
    upload_speed = Column(Float)
    download_speed = Column(Float)
    created_at = Column(DateTime, default=datetime.now)

# Création de la table
Base.metadata.create_all(bind=engine)