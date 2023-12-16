from typing import List
from pydantic import conlist
from pydantic import BaseModel
from app.points.schemas import Point, PointCreate


class TriangleBase(BaseModel):
    mesh_id: int
    level_id: int
    points: List[Point]

class TriangleCreate(TriangleBase):
    points: conlist(PointCreate, min_length=3, max_length=3)
    pass

class Triangle(TriangleBase):
    id: int
    class Config:
        orm_mode = True