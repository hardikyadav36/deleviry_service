from sqlalchemy.orm import Session
from app.repositories import worker_repository
from app.repositories import order_repository
from app.services.geo_instance import geo_service

def create_worker(db: Session, worker_data):
    return worker_repository.create_worker(db, worker_data)

def get_all_workers(db: Session):
    return worker_repository.get_all_workers(db)
def get_available_worker(db: Session):
    return worker_repository.get_available_worker(db)





def update_worker_location(db, worker_id, lat, lng):
    worker = worker_repository.get_worker_by_id(db, worker_id)

    if not worker:
        return None

    # update DB
    worker.latitude = lat
    worker.longitude = lng

    # update Redis GEO
    try:
        geo_service.upsert_worker(worker.id, lat, lng)
    except Exception as e:
        print(f"Error in adding worker location in redis {e}")
    return worker

