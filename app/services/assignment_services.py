# app/services/assignment_service.py

from app.services.geo_instance import geo_service
from app.utils.distance import calculate_distance
from app.repositories.worker_repository import get_workers_by_ids
from sqlalchemy import update
from app.repositories.worker_repository import Worker


class AssignmentService:

    def assign_batch(self, db, orders):

        for order in orders:
            radius_km = 2.0  # could be dynamic based on order urgency, etc.
            worker_ids = []
            while radius_km <= 20:  # max search radius
                worker_ids = geo_service.get_nearby_workers(
                    order.pickup_lat,
                    order.pickup_lng,
                    radius_km
                )
                if worker_ids:
                    break
               
                radius_km *= 2  # exponential backoff
            

            # ✅ single DB query
            workers = get_workers_by_ids(db, worker_ids)

            # sort by distance (so we try closest first)
            workers.sort(
                key=lambda w: calculate_distance(
                    w.latitude,
                    w.longitude,
                    order.pickup_lat,
                    order.pickup_lng
                )
            )

            # 🔥 try assigning in order
            for worker in workers:

                if self.try_assign(db, worker.id, order):
                    break  # success → move to next order

    # ------------------ SAFE ASSIGN ------------------

    def try_assign(self, db, worker_id, order):
        """
        Atomic assignment to avoid race condition
        """

        result = db.execute(
            update(Worker)
            .where(
                Worker.id == worker_id,
                Worker.current_load < Worker.max_capacity
            )
            .values(current_load=Worker.current_load + 1)
        )

        if result.rowcount == 0:
            return False  # worker full → try next

        # assign order
        order.worker_id = worker_id
        order.status = "ASSIGNED"
        db.commit()

        return True