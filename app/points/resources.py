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
def get_point(db: Session=Depends(get_db)):
    """
    return points
    """
    return 'point'

@router.post("/create/", response_model=p_schema)
def create_point(point: PointCreate, db: Session=Depends(get_db)):
    """
    creates a point but doesn't work rn
    """
    point = Point(point)
    point.save(db)
    return point