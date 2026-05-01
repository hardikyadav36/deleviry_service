import asyncio
from app.database.depends import get_db
from app.database.session import SessionLocal
from app.services.batch_service import batch_processor
from app.services.assignment_services import AssignmentService 
import redis
r = redis.Redis(
    host="redis",   # ⚠️ important: use service name from docker-compose
    port=6379,
    decode_responses=True
)
assignment_service = AssignmentService()
async def run_batches():
    await asyncio.sleep(10)  # wait for app to start and db to be ready
    while True:
        # await asyncio.sleep(30)

        # 🔒 distributed lock
        lock = r.set("batch_lock", "1", nx=True, ex=25)

        if not lock:
            continue

        orders = batch_processor.get_batch()

        if not orders:
            continue

        db = SessionLocal()

        try:
            assignment_service.assign_batch(db, orders)
            db.commit()
            batch_processor.clear()

        except Exception as e:
            db.rollback()
            print("Batch failed:", e)

        finally:
            db.close()