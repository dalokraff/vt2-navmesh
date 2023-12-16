from typing import List
from pydantic import BaseModel, conlist
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

class LuaMeshGrid(BaseModel):
    vertices: conlist(
                conlist(float, min_length=3, max_length=3),
                min_length=4
            )

    holes: conlist(
                conlist(float, min_length=3, max_length=3),
                min_length=1
            )
    
    segments: conlist(
                conlist(float, min_length=2, max_length=2),
                min_length=4
            ) | None
    
class LuaMeshRespone(BaseModel):
    num_triangels: int
    mesh_id:int