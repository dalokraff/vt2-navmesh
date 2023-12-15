from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.dependacny import get_db

from .models import Point
from .schemas import Point as p_schema, PointCreate

router = APIRouter(
    prefix="/points",
    tags=["points"]
    )

@router.get("/")
def create_point(db: Session=Depends(get_db)):
    
    return 'point'

@router.post("/create/", response_model=p_schema)
def create_point(point: PointCreate, db: Session=Depends(get_db)):
    point = Point.create_point(db, point=point)
    return point