from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import sys
import shutil
#Cuando terminemos hay que cambiar el directorio donde se guarda a uno mas seguro

def get_app_data_dir():
    app_name = "BeatmatApp"
    if sys.platform.startswith('win'):
        app_data_path = os.path.join(os.getenv('LOCALAPPDATA'), app_name)
    else:
        app_data_path = os.path.join(os.path.expanduser('~'), '.local', 'share', app_name)
    return app_data_path

def setup_database():
    app_data_dir = get_app_data_dir()
    os.makedirs(app_data_dir, exist_ok=True)
    db_path = os.path.join(app_data_dir, 'beatmat.db')
    if not os.path.exists(db_path):
        source_db = None
        if getattr(sys, 'frozen', False):
            try:
                base_path = sys._MEIPASS
                source_db = os.path.join(base_path, "beatmat.db")
            except AttributeError:
                base_path = os.path.dirname(sys.executable)
                source_db = os.path.join(base_path, "beatmat.db")
        else:
            base_path = os.path.abspath(os.path.dirname(__file__))
            source_db = os.path.join(base_path, "beatmat.db")
        try:
            if source_db and os.path.exists(source_db):
                shutil.copy2(source_db, db_path)
                print(f"Base de datos copiada de {source_db} a {db_path}")
            else:
                print(f"Base de datos de origen no encontrada: {source_db}. Se crea una nueva")
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