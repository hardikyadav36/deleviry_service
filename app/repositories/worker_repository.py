from sqlalchemy.orm import Session
from app.models.worker_model import Worker

def create_worker(db: Session, data: dict):
    worker = Worker(**data)
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return worker

def get_all_workers(db: Session):
    return db.query(Worker).all()

def get_available_worker(db: Session):
    return db.query(Worker).filter(Worker.is_available == True).all()

def update_worker_availability(db: Session, worker: Worker, is_available: bool):
    worker.is_available = is_available
    db.commit()
    db.refresh(worker)
    return worker

def update_worker_location(db: Session, worker_id: int, lat: float, lng: float):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    worker.latitude = lat
    worker.longitude = lng
    db.commit()
    return worker



#           -----> For REDIS <-----
def get_worker_by_id(db: Session, worker_id: int):
    return db.query(Worker).filter(Worker.id == worker_id).first()


def get_workers_by_ids(db: Session, worker_ids: list[int]):
    return db.query(Worker).filter(Worker.id.in_(worker_ids)).all()