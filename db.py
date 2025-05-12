from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import sys
import shutil
#Cuando terminemos hay que cambiar el directorio donde se guarda a uno mas seguro

def get_app_data_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def setup_database():
    app_data_dir = get_app_data_dir()
    os.makedirs(app_data_dir, exist_ok=True)
    db_path = os.path.join(app_data_dir, 'beatmat.db')
    if not os.path.exists(db_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        source_db = os.path.join(base_path, "beatmat.db")
        try:
            if os.path.exists(source_db):
                shutil.copy2(source_db, db_path)
            else:
                print(f"Base de datos de origen no encontrada: {source_db}")
        except Exception as e:
            print(f"Error al copiar la base de datos: {e}")
    return db_path

db_path = setup_database()
DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL, echo=True, connect_args={'check_same_thread': False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()