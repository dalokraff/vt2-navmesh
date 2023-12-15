from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from enum import Enum
import numpy as np
from pydantic import BaseModel
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri
from scipy.spatial import Delaunay
import requests
import triangle as tr
import json
import sqlite3

from app.utils import converters
from app.utils.dependacny import get_db

from . import resources, models, schemas
from app.database import SessionLocal, engine

from .points import resources as point_route

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(point_route.router)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = resources.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return resources.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = resources.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = resources.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return resources.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = resources.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/mesh/cjson/{level_id}")
async def create_mesh_from_cjson(lua_data: Request, level_id: int):
    mesh_data = await lua_data.body()
    mesh_str = mesh_data.decode('utf-8')
    #this mnavmesh json needs to be parsed and have it's triangles and points added to the database
    navmesh_json = converters.mesh_from_cjson(mesh_str)
    return navmesh_json

# navmesh calculations
def vector_to_hieght_dict(hieght_dict: dict, three_vec):
    hieght_dict[three_vec[:2]] = three_vec[2]

@app.post("/traingle_calc/")
async def save_triangle(lua_data: Request):    
    '''
    The recieved data is assumed to be a string that containes 3 distinct data types.
        An array of 3-D points representing the nodes of the mesh to be triangluated.
        An array of 2-D points representing line segments of the aforementioned 3-D points,
            denoting the boundry regions of the mesh
        An array of 3-D points used to denote which of the aforementioned boundry regions
            are "holes". 
    '''
    
    mesh_data = await lua_data.body()

    mesh_str = mesh_data.decode('utf-8')
    lua_tri_data = json.loads(mesh_str)
    tri_data = {
        'vertices': np.delete(lua_tri_data['vertices'], 2, 1),
        'holes': np.delete(lua_tri_data['holes'], 2, 1),
        'segments': lua_tri_data['segments']
    }

    vertex_arr = np.array(lua_tri_data['vertices'])
    print(vertex_arr)

    print(vertex_arr.shape)
    

    points_tuple = tuple(tuple(point) for point in vertex_arr.transpose()[:2].transpose())
    print(points_tuple)
    hieght_vals = np.round(vertex_arr.transpose()[2], decimals=2)
    hieght_dict = dict(zip(points_tuple, hieght_vals))

    print(hieght_dict)
    
    triangulation_data = tr.triangulate(tri_data, 'p')

    print(triangulation_data)

    triangles = triangulation_data['triangles'].tolist()
    point_arr = triangulation_data['vertices'].tolist()
    return_data = []
    for tri in triangles:
        triang = []
        for point_index in tri:
            point = point_arr[point_index]
            hieght = hieght_dict[(point[0], point[1])]
            point_with_hieght = np.append(point, hieght).tolist()
            triang.append(point_with_hieght)
        return_data.append(triang)
        
        
    print(return_data)

    return return_data
