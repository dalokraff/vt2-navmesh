from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float, index=True)
    y = Column(Float, index=True)
    z = Column(Float, index=True)
    is_hole = Column(Boolean, index=True)
    is_boundry = Column(Boolean, index=True)
    triangle_id  = Column(Integer, ForeignKey("triangles.id"))
    level_id = Column(Integer, index=True)

class Triangle(Base):
    __tablename__ = "triangles"

    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("levels.id"))
    mesh_id = Column(Integer, ForeignKey("meshes.id"))
    point_one_id = Column(Integer, ForeignKey("points.id"))
    point_two_id = Column(Integer, ForeignKey("points.id"))
    point_three_id = Column(Integer, ForeignKey("points.id"))

class Mesh(Base):
    __tablename__ = "meshes"

    id = Column(Integer, primary_key=True, index=True)


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
