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


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

BOOKS = [
    {"id": 1, "title": "1984", "author": "Джордж Оруэлл"},
    {"id": 2, "title": "Мастер и Маргарита", "author": "Михаил Булгаков"},
    {"id": 3, "title": "Преступление и наказание", "author": "Фёдор Достоевский"},
]




@app.get("/")
def read_root():
    return {"message": "Привет, это мой первый API!"}

@app.get("/books")
def books():
    return BOOKS

@app.get("/about")
def about():
    return {"message": "Книга о великом"}

#DAY 4


@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return {"error" : "Книга не найдена"}


@app.get("/search")
def search_books(author: str):
    newbooks = []
    for book in BOOKS:
        if book["author"] == author:
            newbooks.append(book)
    return newbooks

# DAY 5
class BookCreate(BaseModel):
    title: str
    author: str

@app.post("/books")
def create_book(book: BookCreate):
    if not BOOKS:
        new_id = 1
    else:
        new_id = max([b["id"] for b in BOOKS]) + 1
    new_book = {"id": new_id, "title": book.title, "author": book.author}
    BOOKS.append(new_book)
    return new_book

#DAY 6

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            BOOKS.remove(book)
            return {"message" : "книга удалена"}
    return {"error" : "книга не найдена"}


@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: BookCreate):
    for book in BOOKS:
            if book["id"] == book_id:
                book["title"] = updated_book.title
                book["author"] = updated_book.author
                return book
    return {"error" : "книга не найдена"}


        

