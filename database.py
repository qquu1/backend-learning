from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Замени 'твой_пароль' на пароль от PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234aS@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()