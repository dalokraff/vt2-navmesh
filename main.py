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
def format_triangles_to_lua_table(triangles: np.ndarray, hieght_dict: dict):
    tris = ''
    for tri in triangles:
        points = []
        for point in tri:
            hieght = hieght_dict[tuple(point)]
            point_table_template = f'{{ {point[0]}, {point[1]}, {hieght} }},'
            points.append(point_table_template)
        triangle_table_template = f'{{ {points[0]} {points[1]} {points[2]} }},'
        print(triangle_table_template)
        tris = tris + triangle_table_template

    lua_string = "return {" + tris + "}"
    return lua_string

@app.post("/traingle/")
async def save_triangle(triangle: Request):
    body = await triangle.body()
    body_str = body.decode('utf-8')
    vec_strs = body_str.replace(')', '').split('Vector3(')
    vec_strs.pop(0) #leading "Vector3(" gives an empty string

    vec_list = []
    og_hieght_dict = {}
    for vec in vec_strs:
        new_vec = np.fromstring(vec, dtype=float, sep=', ')
        vec_list.append(new_vec[:2])
        og_hieght_dict[tuple(new_vec[:2])] = new_vec[2]
    vec_arr = np.array(vec_list)
    tri = Delaunay(vec_arr)
    triangles = vec_arr[tri.simplices]

    # for tri1 in triangles:
    #     for point in tri1:
    #         hieght = og_hieght_dict[tuple(point)]
    #         print(str(point[0],point[1], hieght))



    # print(og_hieght_dict)
    # print(vec_strs)
    # print(triangles)

    lua_table = format_triangles_to_lua_table(triangles, og_hieght_dict)
    print(lua_table)

    return lua_table
