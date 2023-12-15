from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, Session

from app.database import Base
import app.points.schemas as schemas
from app.points.models import Point
from app.points.schemas import PointCreate
from app.triangles.schemas import TriangleCreate


class Triangle(Base):
    """
    Triangle Object:
        level_id
        mesh_id
        points = [
            
        ]
    """
    __tablename__ = "triangles"

    id = Column(Integer, primary_key=True, index=True)
    points = relationship(Point, backref='points', uselist=True)
    mesh_id = Column(Integer, index=True)
    level_id = Column(Integer, index=True)

    def __init__(self, tri_info: TriangleCreate):
        self.mesh_id = tri_info.mesh_id
        self.level_id = tri_info.level_id
        # required to initalize the Points
        self.point_json = tri_info.points

    def save(self, db: Session):
        """save triangle object to db"""
        db.add(self)
        db.commit()
        db.refresh(self)

        # iterate over pointCreate objects to initialize and associate them with this triangle 
        for point_obj in self.point_json:
            print(point_obj)
            print(*point_obj)
            point = Point(
                x= point_obj.x,
                y= point_obj.y,
                z= point_obj.z,
                is_hole= point_obj.is_hole,
                is_boundry= point_obj.is_boundry,
                level_id= self.level_id, 
                mesh_id= self.mesh_id,
                triangle_id= self.id
                )
            point.save(db)
            self.points.append(point)

        return self
    
    @staticmethod
    def find_triangle_by_id(triangle_id):
        """Find triangle by triangle id"""
        return Triangle.query.filter(Triangle.id == triangle_id).first()