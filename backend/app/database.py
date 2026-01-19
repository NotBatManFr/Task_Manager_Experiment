import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DB_PATH = os.path.join(BASE_DIR, "..", "tasks.db")

# SQL_ALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
# engine = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# DEFAULT_DB_URL = 'postgresql+psycopg://user:password@db:5432/task_db'
SQL_ALCHEMY_DB_URL = os.getenv('DATABASE_URL')

engine = None
for i in range(5):
    try:
        engine = create_engine(SQL_ALCHEMY_DB_URL)
        # Attempting a dummy connecion to verify if DB is listening
        with engine.connect() as conn:
            break
    except OperationalError:
        print(f"Database not ready yet.... retrying in 2 seconds (Attempt {i+1}/5)")
        time.sleep(2)

if not engine:
    raise Exception("Could not connect to the database. Please check the database instance for any faults.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()