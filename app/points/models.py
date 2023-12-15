from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, Session

from app.database import Base
from app.utils.dependacny import get_db
from app.points.schemas import PointCreate


class Point(Base):
    """
    Point Object:
        x,y,z
        is_hole
        is_boundry
        level_id
        mesh_id
        triangle_id
    """
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float, index=True)
    y = Column(Float, index=True)
    z = Column(Float, index=True)
    is_hole = Column(Boolean, index=True)
    is_boundry = Column(Boolean, index=True)
    level_id = Column(Integer, index=True, nullable=True)
    mesh_id = Column(Integer, index=True, nullable=True)
    triangle_id = Column(Integer, ForeignKey("triangles.id"), nullable=True)
    
    def __init__(self, point_init: PointCreate, level_id=None, triangle_id=None, mesh_id=None):
        self.x = point_init.x
        self.y = point_init.y
        self.z = point_init.z
        self.is_boundry = point_init.is_boundry
        self.is_hole = point_init.is_hole
        self.level_id = level_id
        self.triangle_id = triangle_id
        self.mesh_id = mesh_id

    def save(self, db: Session):
        """
        adds a point to the database
        """

        db.add(self)
        db.commit()
        db.refresh(self)

        return self