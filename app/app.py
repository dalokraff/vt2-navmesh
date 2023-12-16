from fastapi import FastAPI

from . import models
from app.database import engine

from .triangles import resources as tri_route
from .points import resources as point_route
from .meshes import resources as mesh_route


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tri_route.router)
app.include_router(point_route.router)
app.include_router(mesh_route.router)
