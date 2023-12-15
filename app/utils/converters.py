import json
import triangle as tr
import numpy as np


def vector_to_hieght_dict(hieght_dict: dict, three_vec):
    hieght_dict[three_vec[:2]] = three_vec[2]


def mesh_from_cjson(lua_cjson_str: str):
    '''
    The recieved data is assumed to be a string that containes 3 distinct data types.
        An array of 3-D points representing the nodes of the mesh to be triangluated.
        An array of 2-D points representing line segments of the aforementioned 3-D points,
            denoting the boundry regions of the mesh
        An array of 3-D points used to denote which of the aforementioned boundry regions
            are "holes". 
    '''
    lua_tri_data = json.loads(lua_cjson_str)
    
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