from pydantic import BaseModel

class PointBase(BaseModel):
    x: float|int
    y: float|int
    z: float|int
    is_hole: bool
    is_boundry: bool
    level_id: int

class PointCreate(PointBase):
    pass

class Point(PointBase):
    id: int
    class Config:
        orm_mode = True