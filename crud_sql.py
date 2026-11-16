from sqlalchemy.orm import Session
from sqlalchemy import text
from auth import get_password_hash

def get_book_sql(db: Session, book_id: int):
    result = db.execute(
        text("SELECT books.id, books.title, authors.name AS author_name FROM books JOIN authors ON books.author_id = authors.id WHERE books.id = :book_id"),
        {"book_id": book_id}
    )
    row = result.fetchone()
    if row:
        return {"id": row[0], "title": row[1], "author": row[2]}
    return None


def get_books_sql(db: Session, skip: int = 0, limit: int = 10, author: str = None):
    
    query = """
        SELECT books.id, books.title, authors.name AS author_name 
        FROM books 
        JOIN authors ON books.author_id = authors.id
    """
    
    
    params = {"limit": limit, "skip": skip}
    
    
    if author:
        query += " WHERE authors.name = :author"
        params["author"] = author
        
    
    query += " LIMIT :limit OFFSET :skip"
    

    result = db.execute(text(query), params)
    rows = result.fetchall()
    

    books = []
    for row in rows:
        books.append({"id": row[0], "title": row[1], "author": row[2]})
    return books

def create_book_sql(db: Session, title: str, author_id: int):
    
    result = db.execute(
        text("INSERT INTO books (title, author_id) VALUES (:title, :author_id) RETURNING id"),
        {"title": title, "author_id": author_id}
    )
    
    new_id = result.fetchone()[0]
    
    db.commit()
    
    return get_book_sql(db, new_id)

def update_book_sql(db: Session, book_id: int, title: str, author_id: int):
    result = db.execute(
        text("UPDATE books SET title = :title, author_id = :author_id WHERE id = :book_id"),
        {"title": title, "author_id": author_id, "book_id": book_id}
    )
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



def create_author_sql(db: Session, name: str):
    result = db.execute(
        text("INSERT INTO authors (name) VALUES (:name) RETURNING id"),
        {"name": name}
    )
    new_id = result.fetchone()[0]
    db.commit()
    return {"id": new_id, "name": name}

def create_user_sql(db: Session, username: str, password: str):
    hashed_password = get_password_hash(password)
    result = db.execute(
            text("INSERT INTO users (username, hashed_password) VALUES (:username, :hashed_password) RETURNING id"),
            {"username": username, "hashed_password": hashed_password}
        )
    new_id = result.fetchone()[0]
        
    db.commit()
        
    return {"id": new_id, "username": username}

def get_user_by_username_sql(db: Session, username:str):
    result = db.execute(
                text("SELECT id, username, hashed_password FROM users WHERE username = :username"),
                {"username": username}
            )

    row = result.fetchone()
    if row:
        return {"id": row[0], "username": row[1], "hashed_password": row[2]}
    return None




