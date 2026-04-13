from sqlalchemy.orm import Session
from app.repositories import worker_repository

def create_worker(db: Session, worker_data):
    return worker_repository.create_worker(db, worker_data)

def get_all_workers(db: Session):
    return worker_repository.get_all_workers(db)
def get_available_worker(db: Session):
    return worker_repository.get_available_worker(db)

