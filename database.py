from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:vps1111@localhost:3306/parking_db"

engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()
