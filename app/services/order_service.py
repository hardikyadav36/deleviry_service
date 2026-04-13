from sqlalchemy.orm import Session
from app.repositories import order_repository
from app.utils.distance import calculate_distance
from app.repositories import worker_repository


# ✅ Create Order
def create_order(db: Session, order_data):
    return order_repository.create_order(db, order_data.dict())


# ✅ Get All Orders
def get_orders(db: Session):
    return order_repository.get_all_orders(db)


# ✅ Get Single Order
def get_order_by_id(db: Session, order_id: int):
    return order_repository.get_order_by_id(db, order_id)


def assign_nearest_worker(db: Session, order_id: int):
    order = order_repository.get_order_by_id(db, order_id)

    if not order:
        return None

    workers = worker_repository.get_available_worker(db)

    if not workers:
        return order

    nearest_worker = None
    min_distance = float("inf")

    for worker in workers:
        dist = calculate_distance(
            order.pickup_latitude,
            order.pickup_longitude,
            worker.latitude,
            worker.longitude
        )

        if dist < min_distance:
            min_distance = dist
            nearest_worker = worker

    if nearest_worker:
        order = order_repository.assign_worker(db, order, nearest_worker.id)
        worker_repository.update_worker_availability(db, nearest_worker, False)

    return order

def assign_worker(db: Session, order):
    return order_repository.assign_worker(db, order)