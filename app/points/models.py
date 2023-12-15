from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, Session

from app.database import Base
import app.points.schemas as schemas

class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float, index=True)
    y = Column(Float, index=True)
    z = Column(Float, index=True)
    is_hole = Column(Boolean, index=True)
    is_boundry = Column(Boolean, index=True)
    level_id = Column(Integer, index=True)
    
    @staticmethod
    def create_point(db: Session, point: schemas.PointCreate):
        """
        adds a point to the database
        """
        db_point = Point(
            x=point.x,
            y=point.y,
            z=point.z,
            is_hole=point.is_hole,
            is_boundry=point.is_boundry,
            level_id=point.level_id
            )
        db.add(db_point)
        db.commit()
        db.refresh(db_point)
        return db_point