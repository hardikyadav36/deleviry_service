from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.depends import get_db
from app.schemas.order_schema import OrderCreate, OrderResponse
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["Orders"])


# ✅ Create Order
@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db, order)


# ✅ Get All Orders
@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return order_service.get_orders(db)


# ✅ Get Order by ID
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = order_service.get_order_by_id(db, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


# ✅ Assign Worker to Order (Manual trigger)
@router.post("/{order_id}/assign", response_model=OrderResponse)

def assign_worker(order_id: int, db: Session = Depends(get_db)):
    return order_service.assign_nearest_worker(db, order_id)



