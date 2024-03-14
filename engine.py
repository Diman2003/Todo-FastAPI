from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session

# SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite"  # DB for Sqlite
SQLALCHEMY_DATABASE_URL = "mysql://username:password@localhost/todo_list"  # DB for MySQL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))