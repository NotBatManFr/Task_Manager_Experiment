from sqlalchemy.orm import Session
from app.models import Task
import uuid

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self):
        return self.db.query(Task).all()
    
    def add(self, title: str, status: str):
        db_task = Task(id=str(uuid.uuid4()), title=title, status=status)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task) # to get the updated Id into the payload
        return db_task
    
    def remove(self, task_id: str):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if task:
            self.db.delete(task)
            self.db.commit()
            return "Task Deleted"
        return "No Task Found"