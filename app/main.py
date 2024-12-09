from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas, auth
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/oauth/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectas.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/videogames/", response_model=schemas.Videogame)
def create_videogame(videogame: schemas.VideogameCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.create_videogame(db=db, videogame=videogame)

@app.get("/videogames/", response_model=List[schemas.Videogame])
def read_videogames(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    videogames = crud.get_videogames(db, skip=skip, limit=limit)
    return videogames

@app.get("/videogames/{videogame_id}", response_model=schemas.Videogame)
def read_videogame(videogame_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_videogame = crud.get_videogame(db, videogame_id=videogame_id)
    if db_videogame is None:
        raise HTTPException(status_code=404, detail="Juego no encontrado.")
    return db_videogame

@app.put("/videogames/{videogame_id}", response_model=schemas.Videogame)
def update_videogame(videogame_id: int, videogame: schemas.VideogameUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_videogame = crud.update_videogame(db, videogame_id=videogame_id, videogame=videogame)
    if db_videogame is None:
        raise HTTPException(status_code=404, detail="Juego no encontrado.")
    return db_videogame

@app.delete("/videogames/{videogame_id}", response_model=schemas.Videogame)
def delete_videogame(videogame_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_videogame = crud.delete_videogame(db, videogame_id=videogame_id)
    if db_videogame is None:
        raise HTTPException(status_code=404, detail="Juego no encontrado.")
    return db_videogame