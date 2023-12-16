from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.dependacny import get_db

from .models import Point
from .schemas import Point as Point_Schema, PointCreate


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

@router.get("/mesh_id", response_model=Point_Schema)
def get_point_by_mesh_id(mesh_id: int, db: Session=Depends(get_db)):
    points = Point.get_points_by_mesh(mesh_id, db)
    return points

@router.get("/all")
def get_points(db: Session=Depends(get_db)):
    """get all points"""
    results = Point.get_all(db)
    return results

@router.post("/create/", response_model=Point_Schema)
def create_point(point: PointCreate, db: Session=Depends(get_db)):
    """
    creates a point but doesn't work rn
    """
    point = Point(point)
    point.save(db)
    return point