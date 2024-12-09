from sqlalchemy.orm import Session
from . import models, schemas, auth

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_videogames(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Videogame).filter(models.Videogame.status == "AC").offset(skip).limit(limit).all()

def create_videogame(db: Session, videogame: schemas.VideogameCreate):
    db_videogame = models.Videogame(**videogame.dict())
    db.add(db_videogame)
    db.commit()
    db.refresh(db_videogame)
    return db_videogame

def get_videogame(db: Session, videogame_id: int):
    return db.query(models.Videogame).filter(models.Videogame.id == videogame_id, models.Videogame.status == "AC").first()

def update_videogame(db: Session, videogame_id: int, videogame: schemas.VideogameUpdate):
    db_videogame = db.query(models.Videogame).filter(models.Videogame.id == videogame_id).first()
    if db_videogame:
        for key, value in videogame.dict().items():
            setattr(db_videogame, key, value)
        db.commit()
        db.refresh(db_videogame)
    return db_videogame

def delete_videogame(db: Session, videogame_id: int):
    db_videogame = db.query(models.Videogame).filter(models.Videogame.id == videogame_id).first()
    if db_videogame:
        db_videogame.status = "IN"
        db.commit()
    return db_videogame