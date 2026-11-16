from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
import crud_sql
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth import verify_password, create_access_token
from fastapi.security import OAuth2PasswordBearer
from auth import decode_access_token



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # Говорим, где брать токен

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Невалидный токен")
    
    username = payload.get("sub")
    user = crud_sql.get_user_by_username_sql(db, username)

    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user

@app.get("/")
def read_root():
    return {"message": "Привет, это мой первый API!"}

@app.get("/books")
def books(
    skip: int = 0, 
    limit: int = 10, 
    author: str = None, 
    db: Session = Depends(get_db)
):
    return crud_sql.get_books_sql(db, skip=skip, limit=limit, author=author)

@app.get("/about")
def about():
    return {"message": "Книга о великом"}

@app.get("/books/{book_id}")
def get_book(book_id: int,db: Session = Depends(get_db)):
    book = crud_sql.get_book_sql(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

class BookCreate(BaseModel):
    title: str
    author_id: int

@app.post("/books")
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud_sql.create_book_sql(db, title = book.title, author_id=book.author_id)

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    book = crud_sql.delete_book_sql(db, book_id)
    if not book:
        return {"error": "Книга не найдена"}
    return {"message": "Книга удалена"}

@app.put("/books/{book_id}")
def update_book(updated_book: BookCreate, book_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    book = crud_sql.update_book_sql(db, book_id=book_id, title=updated_book.title, author_id=updated_book.author_id)
    if not book:
        return {"error": "Книга не найдена"}
    return book

class AuthorCreate(BaseModel):
    name: str

@app.post("/authors")
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return crud_sql.create_author_sql(db, name=author.name)

class UserCreate(BaseModel):
    username: str
    password:str


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
        return crud_sql.create_user_sql(db, username = user.username, password = user.password)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_sql.get_user_by_username_sql(db, form_data.username)
    
    if not user:
        raise HTTPException(status_code=401, detail="Неверное имя или пароль")
        
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Неверное имя или пароль")
        
    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}




