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

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# table_template = f''' local traingle_table = {{  }}'''
# point_table_template = f'{{{x},{y},{z}}},'
def format_triangles_to_lua_table(triangulation_data, hieght: float|int):
    '''
    Turns the triangle simplices into their coresponding 3-D points. Then turns those points
    into a string representing a lua table of the triangles' points; to be used in `loadstring()`

    `return {
        {1,2,3},
        {2,3,4},
        {3,4,1}
    }`
    '''
    triangles = triangulation_data['triangles'].tolist()
    point_arr = triangulation_data['vertices'].tolist()
    tris = ''
    for tri in triangles:
        print(tuple(tri))
        points = []
        for point_index in tri:
            point = point_arr[point_index]
            point_table_template = f'{{ {point[0]}, {point[1]}, {hieght} }},'
            points.append(point_table_template)
        triangle_table_template = f'{{ {points[0]} {points[1]} {points[2]} }},'
        print(triangle_table_template)
        tris = tris + triangle_table_template

    lua_string = "return {" + tris + "}"
    return lua_string

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
    
    #find mesh points'/vertices' string
    points_start = mesh_str.find('$b') + 1
    points_end = mesh_str.find('$e')
    if points_end < 0:
        points_end = 0
    point_str = mesh_str[points_start:points_end]

    #find mesh boundries' string
    boundry_start = mesh_str.find('&b') + 1
    boundry_end = mesh_str.find('&e')
    if boundry_end < 0:
        boundry_end = 0
    boundry_str = mesh_str[boundry_start:boundry_end]

    #find holes' string
    hole_start = mesh_str.find('^b') + 1
    hole_end = mesh_str.find('^e')
    if hole_end < 0:
        hole_end = 0
    hole_str = mesh_str[hole_start:hole_end]

    #format mesh points' string into numpy array
    list_of_points_as_str = convert_vector_str(point_str, 3)
    point_arr,new_hiegth = format_vector_str_list(list_of_points_as_str)

    #format boundries' string into numpy array
    list_boundry_lines_as_str = convert_vector_str(boundry_str, 3)
    segements,_ = format_vector_str_list(list_boundry_lines_as_str)
    if segements.size < 0:
        segements = tr.convex_hull(point_arr)
    rounded_segements = (np.round(segements)).astype(int)

    #format holes' string into numpy array
    list_of_holes_as_str = convert_vector_str(hole_str, 3)
    hole_arr,_ = format_vector_str_list(list_of_holes_as_str)

    print(point_arr)
    print(segements)
    print(hole_arr)

    #this where the actual triangualtion happens
    tri_data = {'vertices':point_arr, 'segments': rounded_segements, 'holes':hole_arr}
    triangulation_data = tr.triangulate(tri_data, 'p')

    print(triangulation_data)

    lua_table = format_triangles_to_lua_table(triangulation_data, new_hiegth)

    return lua_table
