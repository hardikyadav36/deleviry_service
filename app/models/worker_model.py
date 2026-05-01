from sqlalchemy import Column, Integer, String, Boolean, Float, Index
from sqlalchemy.orm import relationship
from app.database.session import Base

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    current_location = Column(String, nullable=False)

    is_available = Column(Boolean, default=True, index=True)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

   
    max_capacity = Column(Integer, default=3, nullable=False)
    current_load = Column(Integer, default=0, nullable=False)

    __table_args__ = (
        Index("idx_worker_location", "latitude", "longitude"),
    )

    orders = relationship("Order", back_populates="worker")

    # ------------------ HELPER PROPERTIES ------------------

    @property
    def available_capacity(self):
        return self.max_capacity - self.current_load

    @property
    def is_full(self):
        return self.current_load >= self.max_capacity