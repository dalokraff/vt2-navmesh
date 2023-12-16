import json
from fastapi import APIRouter, Depends, Request
import numpy as np
from sqlalchemy.orm import Session
import triangle as tr

from app.utils.dependacny import get_db
from app.triangles.models import Triangle
from app.triangles.schemas import TriangleCreate
from .models import Mesh
from .schemas import Mesh as MeshSchema, MeshCreate

router = APIRouter(
    prefix="/meshes",
    tags=["meshes"]
    )

@router.get("/")
def get_meshes(db: Session=Depends(get_db)):
    """get meshes"""
    return 'mesh'

# @router.post("/triangulate_mesh/", response_model=tri_schema)
# def create_triangle(tri_info: TriangleCreate, db: Session=Depends(get_db)):
#     """
#     endpoint to create mesh from lua data
#     """
#     tri = Triangle(tri_info)
#     tri.save(db)
#     return tri


# navmesh calculations
def vector_to_hieght_dict(hieght_dict: dict, three_vec):
    hieght_dict[three_vec[:2]] = three_vec[2]

@router.post("/triangulate_mesh/", response_model=MeshSchema)
async def save_triangle(lua_data: Request, db: Session=Depends(get_db)):    
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

    point_dict_keys = ['x', 'y', 'z']
    triangle_list = []
    for tri in triangles:
        point_list = []
        for point_index in tri:
            point = point_arr[point_index]
            hieght = hieght_dict[(point[0], point[1])]
            point_with_hieght = np.append(point, hieght).tolist()
            # triang.append(point_with_hieght)
            point_dict = dict(zip(point_dict_keys, point_with_hieght))
            point_dict['is_boundry'] = False
            point_dict['is_hole'] = False
            point_list.append(point_dict)
        # return_data.append(triang)
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
        
    print(return_data)

    return mesh_obj