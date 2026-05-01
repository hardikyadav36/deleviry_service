import os
import redis

class RedisGeoService:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.r = redis.Redis.from_url(redis_url, decode_responses=True)

        self.worker_key = "geo:workers"

    # ------------------ WORKERS ------------------

    def upsert_worker(self, worker_id: int, lat: float, lng: float):
        """
        Add or update worker location
        """
        self.r.geoadd(self.worker_key, (lng, lat, worker_id))

    def remove_worker(self, worker_id: int):
        self.r.zrem(self.worker_key, worker_id)

    # ------------------ QUERY ------------------

    def get_nearby_workers(self, lat: float, lng: float, radius_km: float ):
        """
        Returns nearby worker IDs
        """
        ids = self.r.georadius(
            self.worker_key,
            lng,
            lat,
            radius_km,
            unit="km"
        )
        return [int(i) for i in ids]