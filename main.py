from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from database import get_db, Base, engine
from model import ParkingSlotModel
from schema import ParkingSlotCreate, ParkingSlotResponse

app = FastAPI(
    title="Parking Lot Management"
)

Base.metadata.create_all(bind=engine)


def build_response(status_code, message, error, data, path):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


@app.post("/parking-slots")
def create_parking_slot(slot: ParkingSlotCreate, request: Request, db: Session = Depends(get_db)):
    existing = db.query(ParkingSlotModel).filter(ParkingSlotModel.slot_code == slot.slot_code).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=build_response(400, "Ma vi tri do da ton tai", "Bad Request", None, str(request.url.path))
        )

    try:
        new_slot = ParkingSlotModel(
            slot_code=slot.slot_code,
            zone_name=slot.zone_name,
            max_weight=slot.max_weight
        )
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=build_response(500, "Loi he thong khi them vi tri do xe", str(e), None, str(request.url.path))
        )

    data = ParkingSlotResponse.model_validate(new_slot).model_dump()
    return build_response(201, "Them vi tri do xe thanh cong", None, data, str(request.url.path))


@app.get("/parking-slots")
def get_parking_slots(request: Request, db: Session = Depends(get_db)):
    slots = db.query(ParkingSlotModel).all()
    data = [ParkingSlotResponse.model_validate(slot).model_dump() for slot in slots]
    return build_response(200, "Lay danh sach vi tri do xe thanh cong", None, data, str(request.url.path))


@app.get("/parking-slots/{slot_id}")
def get_parking_slot_detail(slot_id: int, request: Request, db: Session = Depends(get_db)):
    slot = db.query(ParkingSlotModel).filter(ParkingSlotModel.id == slot_id).first()
    if not slot:
        raise HTTPException(
            status_code=404,
            detail=build_response(404, "Parking slot not found", "Not Found", None, str(request.url.path))
        )

    data = ParkingSlotResponse.model_validate(slot).model_dump()
    return build_response(200, "Lay chi tiet vi tri do xe thanh cong", None, data, str(request.url.path))
