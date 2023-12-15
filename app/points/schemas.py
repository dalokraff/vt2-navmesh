from pydantic import BaseModel


class PointBase(BaseModel):
    x: float|int
    y: float|int
    z: float|int
    is_hole: bool
    is_boundry: bool

class PointCreate(PointBase):
    pass

class Point(PointBase):
    id: int
    triangle_id: int|None
    level_id: int|None
    mesh_id: int|None
    class Config:
        orm_mode = True