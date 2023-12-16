import numpy as np
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float
from sqlalchemy.orm import Session

from app.database import Base
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
    mesh_id = Column(Integer, ForeignKey("meshes.id"), nullable=True)
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

    def vector(self):
        vec = np.array([self.x, self.y, self.z])
        return vec
    
    @staticmethod
    def as_vectors(func):
        def vectorize(*args, **kwargs):
            result = func(*args, **kwargs)
            if ('as_vec' in kwargs) and (kwargs['as_vec']):
                new_result = []
                for point in result:
                    new_result.append(point.vector())
                result = new_result
            return result
        
        return vectorize

    @staticmethod
    @as_vectors
    def get_all(db:Session, as_vec: bool=False):
        return db.query(Point).all()
    
    @staticmethod
    @as_vectors
    def get_points_by_mesh(mesh_id:int, db:Session, as_vec: bool=False):
        query = db.query(Point)
        query_filter = query.filter(Point.mesh_id == mesh_id)
        results = query_filter
        return results