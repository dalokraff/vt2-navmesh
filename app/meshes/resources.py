import json
from fastapi import APIRouter, Depends, Request
import numpy as np
from sqlalchemy.orm import Session
import triangle as tr

from app.utils.dependacny import get_db
from app.triangles.models import Triangle
from app.triangles.schemas import TriangleCreate
from .models import Mesh
from .schemas import LuaMeshRespone, Mesh as MeshSchema, LuaMeshGrid

router = APIRouter(
    prefix="/meshes",
    tags=["meshes"]
    )

@router.get("/")
def get_meshes(db: Session=Depends(get_db)):
    """get meshes"""
    return 'mesh'

# navmesh calculation functions
def vector_to_hieght_dict(hieght_dict: dict, three_vec):
    hieght_dict[three_vec[:2]] = three_vec[2]

def triangulate_and_save_results(tri_dict, db: Session):
    tri_data = {
        'vertices': np.delete(tri_dict['vertices'], 2, 1),
        'holes': np.delete(tri_dict['holes'], 2, 1),
        'segments': tri_dict['segments']
    }

    vertex_arr = np.array(tri_dict['vertices'])
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

    point_dict_keys = ['x', 'y', 'z']
    triangle_list = []
    for tri in triangles:
        point_list = []
        for point_index in tri:
            point = point_arr[point_index]
            hieght = hieght_dict[(point[0], point[1])]
            point_with_hieght = np.append(point, hieght).tolist()
            point_dict = dict(zip(point_dict_keys, point_with_hieght))
            point_dict['is_boundry'] = False
            point_dict['is_hole'] = False
            point_list.append(point_dict)

        tri_init = {
            'mesh_id': 1,
            'level_id':1,
            'points': point_list
        }
        print(tri_init)
        tri_obj = Triangle(
            TriangleCreate(mesh_id=1, level_id=1, points=point_list)
        )
        tri_obj.save(db)
        triangle_list.append(tri_obj)
    
    mesh_obj = Mesh(triangle_list, level_id=1)
    mesh_obj.save(db)      

    resp = LuaMeshRespone(num_triangels=len(triangle_list), mesh_id=mesh_obj.id)

    return resp, mesh_obj


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
