from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.depends import get_db
from app.schemas.worker_schema import WorkerCreate, WorkerResponse
from app.services import worker_service

router = APIRouter(prefix="/workers", tags=["Workers"])

@router.post("/", response_model=WorkerResponse)
def create_worker(worker: WorkerCreate, db: Session = Depends(get_db)):
    return worker_service.create_worker(db, worker.dict())

@router.get("/", response_model=list[WorkerResponse])
def get_workers(db: Session = Depends(get_db)):
    return worker_service.get_all_workers(db)

@router.get("/available", response_model=list[WorkerResponse])
def get_available_workers(db: Session = Depends(get_db)):
    return worker_service.get_available_worker(db)

