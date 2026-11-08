# import json

# #task 1
# def read_file(path: str) -> str:
#     try:
#         with open(path, "r") as file:
#             return file.read()
#     except FileNotFoundError:
#         return ""

# #task 2
# # user = {
# #     "name" : "Alex",
# #     "age" : 12,
# #     "visits" : 0
# # }

# # try:
# #     with open("data.json", "w") as file:
# #         json.dump(user, file, indent=4)
# # except (FileNotFoundError):
# #     print("Error")

# #task 3

# def safe_divide(a, b) -> float | None:
#     try:
#         return (a / b)
#     except (ZeroDivisionError, TypeError):
#         return None





# #task 4

# default_user = {
#     "name" : "Egor",
#     "visits" : 0
# }

# def Smart():
#     try:
#         with open("data.json", "r") as file:
#             data = json.load(file)

#     except (FileNotFoundError, json.JSONDecodeError):
#         data = default_user.copy()


#     visits = data.get("visits", 0)
#     if not isinstance(visits, int):   
#         visits = 0
#     data["visits"] = visits + 1
#     save_data(data, "data.json")

#     print(data)

    




# def save_data(data, path):
#     with open(path, "w") as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)


# #Task 5
# def count_words(text: str) -> dict:
#     word_counts = {}
#     words = text.lower().split()


#     for word in words:
#         cleaned_word = word.strip(".,!?;:")
#         if cleaned_word:
#             word_counts[cleaned_word] = word_counts.get(cleaned_word, 0) + 1

#     return word_counts


# Smart()



#DAY 3
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models, crud
from database import engine, SessionLocal
import crud_sql
from fastapi import FastAPI, Depends, HTTPException

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Привет, это мой первый API!"}

@app.get("/books")
def books(db: Session = Depends(get_db)):
    return crud_sql.get_books_sql(db)

@app.get("/about")
def about():
    return {"message": "Книга о великом"}

#DAY 4


@app.get("/books/{book_id}")
def get_book(book_id: int,db: Session = Depends(get_db)):
    book = crud_sql.get_book_sql(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


# DAY 5
class BookCreate(BaseModel):
    title: str
    author_id: int

@app.post("/books")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud_sql.create_book_sql(db, title = book.title, author_id=book.author_id)

#DAY 6

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = crud_sql.delete_book_sql(db, book_id)
    if not book:
        return {"error": "Книга не найдена"}
    return {"message": "Книга удалена"}


@app.put("/books/{book_id}")
def update_book(updated_book: BookCreate, book_id: int, db: Session = Depends(get_db)):
    book = crud_sql.update_book_sql(db, book_id=book_id, title=updated_book.title, author_id=updated_book.author_id)
    if not book:
        return {"error": "Книга не найдена"}
    return book

class AuthorCreate(BaseModel):
    name: str

@app.post("/authors")
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return crud_sql.create_author_sql(db, name=author.name)


import asyncio

@app.get("/async-test")
async def async_test():

    await asyncio.sleep(10) 
    return {"message": "Прошло 10 секунд, но сервер не завис!"}


import time

import time

@app.get("/sync-test")
async def sync_test():  # <-- Обрати внимание: async def!
    time.sleep(10)       # <-- Синхронный сон внутри асинхронной функции
    return {"message": "Прошло 3 секунды"}
        

