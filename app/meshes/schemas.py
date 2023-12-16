from typing import List
from pydantic import BaseModel
# from app.points.schemas import Point
from app.triangles.schemas import Triangle

class MeshBase(BaseModel):
    triangles: List[Triangle]
    # points: List[Point]
    # holes: List[Point]
    level_id: int|None

class MeshCreate(MeshBase):
    pass

class Mesh(MeshBase):
    id: int
    class Config:
        orm_mode = True