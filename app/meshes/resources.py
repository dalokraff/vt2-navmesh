import json
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.utils.dependacny import get_db
from .models import Mesh
from .schemas import LuaMeshRespone, Mesh as MeshSchema, LuaMeshGrid
from .operations import triangulate_and_save_results

router = APIRouter(
    prefix="/meshes",
    tags=["meshes"]
    )

@router.get("/", response_model=MeshSchema)
def get_mesh_by_id(mesh_id: int, db: Session=Depends(get_db)):
    mesh = Mesh.get_mesh_by_id(mesh_id, db)
    return mesh

@router.get("/all")
def get_meshes(db: Session=Depends(get_db)):
    """get all meshes"""
    results = Mesh.get_all(db)
    return results

@router.post("/triangulate_mesh_example/", response_model=LuaMeshRespone)
async def gen_mesh_in_api(lua_data: LuaMeshGrid, db: Session=Depends(get_db)): 
    '''
    The recieved data is assumed to be a json that containes 3 distinct data types.
        An array of 3-D points representing the nodes of the mesh to be triangluated.
        An array of 2-D points representing line segments of the aforementioned 3-D points,
            denoting the boundry regions of the mesh
        An array of 3-D points used to denote which of the aforementioned boundry regions
            are "holes". 
    '''
    
    mesh_data = dict(lua_data)

    # mesh_str = mesh_data.decode('utf-8')
    # lua_tri_data = json.loads(mesh_data)
    
    response,_ = triangulate_and_save_results(mesh_data, db)

    return response

@router.post("/triangulate_mesh_ingame/", response_model=MeshSchema)
async def gen_mesh_ingame(lua_data: Request, db: Session=Depends(get_db)): 
    '''
    The recieved data is assumed to be a json that containes 3 distinct data types.
        An array of 3-D points representing the nodes of the mesh to be triangluated.
        An array of 2-D points representing line segments of the aforementioned 3-D points,
            denoting the boundry regions of the mesh
        An array of 3-D points used to denote which of the aforementioned boundry regions
            are "holes". 
    '''
    
    mesh_data = await lua_data.body()

    mesh_str = mesh_data.decode('utf-8')
    lua_tri_data = json.loads(mesh_str)
    
    _, mesh_obj = triangulate_and_save_results(lua_tri_data, db)

    return mesh_obj


@router.get("/concat/", response_model=MeshSchema)
async def concat_meshes(start_id:int , end_id: int, db: Session=Depends(get_db)):
    """
    Merges the triangles from Mesh 1 and Mesh 2.\n
    NOTE: Does not connect the triangle vertices!!!
    """
    if start_id == end_id:
        msg = f'Can not combine mesh {start_id} with itself!'
        return PlainTextResponse(msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    start_mesh = Mesh.get_mesh_by_id(start_id, db)
    stop_mesh = Mesh.get_mesh_by_id(end_id, db)

    new_mesh = Mesh.concat_meshes(start_mesh, stop_mesh, db)

    return new_mesh

@router.get("/merge/", response_model=MeshSchema)
async def merge_meshes(start_id: int, end_id: int, db: Session=Depends(get_db)):

    if start_id == end_id:
        msg = f'Can not combine mesh {start_id} with itself!'
        return PlainTextResponse(msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    start_mesh = Mesh.get_mesh_by_id(start_id, db)
    stop_mesh = Mesh.get_mesh_by_id(end_id, db)

    new_mesh = Mesh.merge_meshes(start_mesh, stop_mesh, db)

    return new_mesh
