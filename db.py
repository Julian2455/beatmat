from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import sys
import shutil

def get_app_data_dir():
    return os.path.dirname(os.path.abspath(__file__))

def setup_database():
    app_data_dir = get_app_data_dir()
    db_path = os.path.join(app_data_dir, 'beatmat.db')
    if not os.path.exists(db_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        source_db = os.path.join(base_path, "beatmat.db")
        if os.path.exists(source_db):
            shutil.copy2(source_db, db_path)
        else:
            print(f"No la encuentra: {source_db}")
    
    return db_path

db_path = setup_database()
DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()