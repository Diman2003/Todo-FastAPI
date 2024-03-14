from fastapi import FastAPI, Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from engine import session as SessionLocal
import models
from models import User
import schemas
from typing import List
from utils import *

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.TodoList])
def list_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Todo).filter_by(user=current_user)



@router.get("/{task_id}", response_model=schemas.TodoDetail)
def list_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == task_id,models.Todo.user==current_user).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return todo



@router.post("/")
def create_task(task: schemas.TodoCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = models.Todo(**task.dict())
    todo.user_id = current_user.id
    db.add(todo)
    db.commit()
    return {"success": True}



@router.delete("/{task_id}")
def delete_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == task_id,models.Todo.user==current_user).delete()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.commit()
    return {"success": True}



@router.put("/{task_id}")
def edit_task(task_id: int, task: schemas.TodoCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == task_id,models.Todo.user==current_user).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    todo.title = task.title
    todo.description = task.description
    db.commit()
    return {"success": True}



@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    return {"message": "User created successfully"}



@router.post("/login")
def login(user: schemas.UserCreate):
    email = user.email
    password = user.password
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}



@app.post("/logout")
def logout(current_user: str = Depends(oauth2_scheme)):
    add_token_to_blacklist(current_user)
    return {"message": f"Logout successful for user: {current_user}"}

app.include_router(router)
