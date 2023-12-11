from enum import Enum
import numpy as np
from fastapi import Request, FastAPI
from pydantic import BaseModel
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri
from scipy.spatial import Delaunay
import requests
import triangle as tr
import json

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

def convert_vector_str(vector_str: str, dim:int):
    '''
    "Vector3(x,y,z)Vector3(x,y,z)Vector3(x,y,z)" -> ["x,y,z", "x,y,z", "x,y,z"]
    '''
    list_of_vectors_as_str = vector_str.replace(')', '').split(f'Vector{dim}(')
    list_of_vectors_as_str.pop(0) #leading "Vector3(" gives an empty string
    return list_of_vectors_as_str

def format_vector_str_list(list_of_vectors_as_str: [str]):
    '''
    ["x,y,z", "x,y,z", "x,y,z"] -> 
            np.array([x,y],[x,y],[x,y]) , avg(z, z, z)
    '''
    vec_list = []
    og_hieght_dict = {}
    hieght_total = 0
    for vec in list_of_vectors_as_str:
        new_vec = np.fromstring(vec, dtype=float, sep=', ')
        vec_list.append(new_vec[:2])
        hieght_total += new_vec[2]
    vec_arr = np.array(vec_list)
    avg_hieght = hieght_total/(len(vec_list)+0.00001)

    return vec_arr, avg_hieght

@app.post("/traingle/")
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
    
    triangulation_data = tr.triangulate(tri_data, 'p')

    print(triangulation_data)

    triangles = triangulation_data['triangles'].tolist()
    point_arr = triangulation_data['vertices'].tolist()
    return_data = []
    for tri in triangles:
        triang = []
        for point_index in tri:
            point = point_arr[point_index]
            hieght = np.mean(vertex_arr[:, 2])
            point_with_hieght = np.append(point, hieght).tolist()
            triang.append(point_with_hieght)
        return_data.append(triang)
        
        
    print(return_data)

    return return_data
