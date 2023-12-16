from typing import List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, Session

from app.database import Base
from app.points.schemas import PointCreate, Point
from app.triangles.models import Triangle
from app.triangles.schemas import Triangle as tri_schema, TriangleCreate


class Mesh(Base):
    """
    
    """
    __tablename__ = "meshes"

    id = Column(Integer, primary_key=True, index=True)
    triangles = relationship(Triangle, backref='triangles', uselist=True)
    # points = relationship(Point, backref='points', uselist=True)
    # holes = relationship(Point, backref='points', uselist=True)
    level_id = Column(Integer, index=True, nullable=True)
    
    def __init__(self,
                 triangles: List[tri_schema]|List[TriangleCreate],
                #  points: List[Point]| List[PointCreate],
                 level_id=None):
        
        self.level_id = level_id

        for tri in triangles:
            self.triangles.append(tri)

        # for point in points:
        #     self.points.append(point)

    def save(self, db: Session):
        """
        adds a point to the database
        """

        db.add(self)
        db.commit()
        db.refresh(self)

        return self