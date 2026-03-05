from sqlalchemy.orm import Session
from src.models import Task

class TaskRepository:

    """
    Repository for handling all DB operations for tasks
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    # -------- CRUD Operations --------
    # ------------- Read --------------

    def get_all(self) -> list[Task]:
        """Fetch all tasks from the database"""
        return self.db.query(Task).all()
    
    def get_by_id(self, task_id: str) -> Task | None:
        """Fetch a single task by its ID"""
        return self.db.query(Task).filter(Task.id == task_id).first()

    #------------- Write --------------

    def add(self, task: Task) -> Task:
        """Add a new task to the database and return the DB generated task"""
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task) # to get the updated Id into the payload
        return task
    
    def update(self, task: Task) -> Task | None:
        """
        Merge and Commit in-place mutations to an already-tracked Task instance
        in lieu of SQLAlchemy's change tracking 

        The caller (service layer) is responsible for modifying the task's
        fields before calling this method
        """
        merged_task = self.db.merge(task)
        self.db.commit()
        self.db.refresh(merged_task) # to get the updated task from the DB
        return merged_task
    
    def remove(self, task: Task) -> bool:
        """
        Delete an existing Task instance from the database

        Returns True if the delete and commit succeeded, False otherwise

        The caller is responsible for ensuring the task exists before
        calling this method
        """
        try:
            self.db.delete(task)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False