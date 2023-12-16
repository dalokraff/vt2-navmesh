from typing import List
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship, Session

from app.database import Base
from app.points.models import Point
from app.triangles.models import Triangle
from app.triangles.schemas import Triangle as tri_schema, TriangleCreate
from .schemas import Mesh as Mesh_Schema


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
            # self.points = self.points + tri.points
            # for point in tri.points:
            #     point.mesh_id = self.id
            #     point.save

        # for point in points:
        #     self.points.append(point)

    def save(self, db: Session):
        """
        adds a point to the database
        """

        db.add(self)
        db.commit()
        db.refresh(self)

        # update point tbale with mesh ids
        for triangle in self.triangles:
            for point in triangle.points:
                point.mesh_id = self.id
                point.save(db)
            triangle.mesh_id = self.id
            triangle.save(db)

        return self
    
    @staticmethod
    def get_all(db:Session):
        return db.query(Mesh).all()
    
    @staticmethod
    def get_mesh_by_id(mesh_id:int, db:Session):
        query = db.query(Mesh)
        query_filter = query.filter(Mesh.id == mesh_id)
        results = query_filter.first()
        return results

    @staticmethod
    def concat_meshes(mesh_1: Mesh_Schema, mesh_2: Mesh_Schema, db: Session):

        if mesh_1.level_id != mesh_2.level_id:
            raise TypeError(f'Mesh 1 is from level {mesh_1.level_id}, while Mesh 2 is from level {mesh_2.level_id}')
        
        combined_tris = mesh_1.triangles + mesh_2.triangles
        new_mesh = Mesh(combined_tris, level_id=mesh_1.level_id)
        new_mesh.save(db)
        
        return new_mesh
    
    @staticmethod
    def merge_meshes(mesh_1: Mesh_Schema, mesh_2: Mesh_Schema, db: Session):
        """
        Starting from mesh one, combines the two meshes by finding the smallest area plane between their respective boundry points
        """
        if mesh_1.level_id != mesh_2.level_id:
            raise TypeError(f'Mesh 1 is from level {mesh_1.level_id}, while Mesh 2 is from level {mesh_2.level_id}')
        
        merged_tris = mesh_1.triangles + mesh_2.triangles

        new_mesh = Mesh(merged_tris, level_id=mesh_1.level_id)
        new_mesh.save(db)
        
        return new_mesh