from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.vehicle import VehicleCreate, VehicleOut
from app.crud.vehicle import create_vehicle
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", response_model=VehicleOut)
def register_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_vehicle(db=db, vehicle=vehicle, driver_id=current_user.user_id)
