from sqlalchemy.orm import Session
from app.models.order_model import Order
from app.services.batch_service import batch_processor


def create_order(db: Session, order_data: dict):
    order = Order(**order_data)
    db.add(order)
    db.commit()
    db.refresh(order)

    batch_processor.add_order(order)

    return order


def get_all_orders(db: Session):
    return db.query(Order).all()


def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def assign_worker(db: Session, order: Order, worker_id: int):
    order.worker_id = worker_id
    order.status = "ASSIGNED"
    db.commit()
    db.refresh(order)
    return order