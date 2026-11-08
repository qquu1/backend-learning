from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Привет, это мой первый API!"}

def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list) # Проверяем, что вернулся список

def test_get_nonexistent_book():
    response = client.get("/books/99999")
    assert response.status_code == 404 # Проверяем, что сработал HTTPException
    assert response.json()["detail"] == "Книга не найдена"

def test_create_author_and_book():
    # 1. Создаем автора
    author_response = client.post("/authors", json={"name": "Тестовый Автор"})
    assert author_response.status_code == 200
    author_id = author_response.json()["id"]

    # 2. Создаем книгу
    book_response = client.post("/books", json={"title": "Тестовая Книга", "author_id": author_id})
    assert book_response.status_code == 200
    book_data = book_response.json()
    assert book_data["title"] == "Тестовая Книга"
    assert book_data["author"] == "Тестовый Автор" # Проверяем работу JOIN!