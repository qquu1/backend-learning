from sqlalchemy.orm import Session
from sqlalchemy import text

def get_books_sql(db: Session):
   
    result = db.execute(text("SELECT id, title, author FROM books"))
    
    # result.fetchall() возвращает список кортежей (например, [(1, '1984', 'Оруэлл')])
    rows = result.fetchall()
    
    # Превращаем кортежи в словари, чтобы FastAPI мог отдать их как JSON
    books = []
    for row in rows:
        books.append({"id": row[0], "title": row[1], "author": row[2]})
    return books




def get_book_sql(db: Session, book_id: int):
    result = db.execute(text("SELECT id, title, author FROM books WHERE id = :book_id"),{"book_id": book_id})
    row = result.fetchone()
    
    if row:
        return {"id": row[0], "title": row[1], "author": row[2]}
    return None

def create_book_sql(db: Session, title: str, author: str):
    
    result = db.execute(
        text("INSERT INTO books (title, author) VALUES (:title, :author) RETURNING id"),
        {"title": title, "author": author}
    )
    
    new_id = result.fetchone()[0]
    
    db.commit()
    
    return get_book_sql(db, new_id)

def update_book_sql(db: Session, book_id: int, title: str, author: str):
    result = db.execute(
        text("UPDATE books SET title = :title, author = :author WHERE id = :book_id"),
        {"title": title, "author": author, "book_id": book_id})
    db.commit()
    
    if result.rowcount == 0:
        return None  
        
    return get_book_sql(db, book_id)


def delete_book_sql(db: Session, book_id: int):
    result = db.execute(
        text("DELETE FROM books WHERE id = :book_id"),
        {"book_id": book_id})

    db.commit()
    if result.rowcount == 0:
        return None  
    else:
        return {"message": "Книга удалена"}




