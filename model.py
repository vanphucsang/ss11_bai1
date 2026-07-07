from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class ParkingSlotModel(Base):
    __tablename__ = 'parking_slots'

    id = Column(Integer, primary_key=True, index=True)
    slot_code = Column(String(50), nullable=False, unique=True, index=True)
    zone_name = Column(String(255), nullable=False)
    max_weight = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
