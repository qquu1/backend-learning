from sqlalchemy.orm import Session
import models

# 1. Получить все книги
def get_books(db: Session):
    return db.query(models.Book).all()

# 2. Получить книгу по ID
def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

# 3. Создать книгу
def create_book(db: Session, title: str, author: str):
    new_book = models.Book(title=title, author=author)
    db.add(new_book)
    db.commit()
    db.refresh(new_book) 
    return new_book

# 4. Обновить книгу
def update_book(db: Session, book_id: int, title: str, author: str):
    book = get_book(db, book_id)
    if book:
        book.title = title
        book.author = author
        db.commit()
        db.refresh(book)
    return book

# 5. Удалить книгу
def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if book:
        db.delete(book)
        db.commit()
    return book