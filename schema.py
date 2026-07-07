from pydantic import BaseModel, Field

class ParkingSlotCreate(BaseModel):
    slot_code: str = Field(..., min_length=1)
    zone_name: str = Field(..., min_length=3)
    max_weight: int = Field(..., gt=0)

class ParkingSlotResponse(BaseModel):
    id: int
    slot_code: str
    zone_name: str
    max_weight: int
    is_available: bool

    class Config:
        from_attributes = True
