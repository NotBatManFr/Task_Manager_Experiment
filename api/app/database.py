import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.pool import QueuePool

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

engine = create_engine(DATABASE_URL)

engine = None
max_retries = 5
retry_delay = 2

for attempt in range(max_retries):
    try:
        engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_size=5,  # Number of connections to maintain
            max_overflow=10,  # Max connections beyond pool_size
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=3600,  # Recycle connections after 1 hour
            echo=False,  # Set to True for SQL query logging in development
        )
        
        # Test the connection
        with engine.connect() as conn:
            print("✓ Database connection established successfully")
            break
            
    except OperationalError as e:
        if attempt < max_retries - 1:
            print(f"⚠ Database not ready yet, retrying in {retry_delay}s (Attempt {attempt + 1}/{max_retries})")
            time.sleep(retry_delay)
        else:
            print(f"✗ Failed to connect to database after {max_retries} attempts")
            raise Exception(
                "Could not connect to the database. "
                "Please check your DATABASE_URL and ensure the database is accessible."
            ) from e

if not engine:
    raise Exception("Database engine initialization failed")


# for i in range(5):
#     try:
#         engine = create_engine(DATABASE_URL)
#         # Attempting a dummy connecion to verify if DB is listening
#         with engine.connect() as conn:
#             break
#     except OperationalError:
#         print(f"Database not ready yet.... retrying in 20 seconds (Attempt {i+1}/5)")
#         time.sleep(20)

# if not engine:
#     raise Exception("Could not connect to the database. Please check the database instance for any faults.")

# # Test the connection
# try:
#     with engine.connect() as connection:
#         print("Connection successful!")
# except Exception as e:
#     print(f"Failed to connect: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
