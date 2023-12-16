from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.dependacny import get_db

from .models import Triangle
from .schemas import Triangle as tri_schema, TriangleCreate


router = APIRouter(
    prefix="/triangles",
    tags=["triangles"]
    )

@router.get("/")
def get_triangles(db: Session=Depends(get_db)):
    """get triangles"""
    return 'triangle'

@router.post("/create/", response_model=tri_schema)
def create_triangle(tri_info: TriangleCreate, db: Session=Depends(get_db)):
    """
    endpoint to create  new triangle
    """
    tri = Triangle(tri_info)
    tri.save(db)
    return tri