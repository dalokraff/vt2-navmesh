from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True

########################################################
class PointBase(BaseModel):
    x: float|int
    y: float|int
    z: float|int
    is_hole: bool
    is_boundry: bool
    triangle_id: int
    level_id: int

class PointCreate(PointBase):
    pass

class Point(PointBase):
    id: int
    class Config:
        orm_mode = True

class TriangleBase(BaseModel):
    # one: Point
    # two: Point
    # three: Point
    mesh_id: int
    level_id: int

class TriangleCreate(TriangleBase):
    pass

class Triangle(TriangleBase):
    id: int
    point_one_id: int
    point_two_id: int
    point_three_id: int
    class Config:
        orm_mode = True

class MeshBase(BaseModel):
    triangles: list[Triangle]
    points: list[Point]
    holes: list[Point]
    boundry: list[Point]
    level_id: int

class MeshCreate(MeshBase):
    pass

class Mesh(BaseModel):
    id: int
    class Config:
        orm_mode = True

class LevelBase(BaseModel):
    name: str
    meshes: list[Mesh]

class LevelCreate(LevelBase):
    pass

class Level(LevelBase):
    id: int
    class Config:
        orm_mod = True
