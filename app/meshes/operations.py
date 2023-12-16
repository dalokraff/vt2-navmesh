import numpy as np
import triangle as tr
from sqlalchemy.orm import Session

from app.meshes.schemas import LuaMeshRespone, Mesh as Mesh_Schema
from app.triangles.models import Triangle
from app.triangles.schemas import TriangleCreate
from .models import Mesh

# navmesh generation calculation functions
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


def interpolate_meshes(mesh_one: Mesh_Schema, mesh_two: Mesh_Schema):
    return