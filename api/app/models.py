from sqlalchemy import Column, String
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    status = Column(String, default="pending")
