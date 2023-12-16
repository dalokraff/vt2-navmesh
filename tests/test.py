"""
Probably need to turn this into unittests instead of a scratchpad.
Depends on how expansive the main app becomes.
"""
import matplotlib.pyplot as plt
import numpy as np
import triangle as tr
import json

# box = tr.get_data('box')

# pts = [[1,0], [2,0], [1,1], [2,1], [2,2], [1,2], [3,1], [3,2]]
# holes = [[0.25,0.26], [0.76, 0.25]]

# segments = tr.convex_hull(pts)
# print(segments)
# segs = segments.tolist()
# segs = [[0, 1], [1, 3], [3, 6], [6, 7], [7, 4], [4, 5], [5, 2], [2, 0]]

# pnt_dicts = {'vertices':pts, 'holes':holes, 'segments': segs}
# t = tr.triangulate(pnt_dicts, 'p')
# print(t)
# if 'triangles' in t:
#     print (t['triangles'])



pts =[[-177.308  ,  79.0253],
 [-177.355  ,  82.1275],
 [-168.758  ,  82.3712],
 [-168.703  ,  85.6942],
 [-159.425  ,  85.3755],
 [-159.222  ,  82.4703],
 [-153.81   ,  82.2867],
 [-153.669  ,  79.098 ],
 [-159.292  ,  79.0223],
 [-159.224  ,  75.8528],
 [-168.375  ,  75.9135],
 [-168.324  ,  78.9298],
 [-165.4    ,  82.0718],
 [-162.554  ,  82.2257],
 [-162.659  ,  79.3007],
 [-165.275  ,  79.2427]]

segs = [[ 0,  1],
 [ 1,  2],
 [ 2,  3],
 [ 3,  4],
 [ 4,  5],
 [ 5,  6],
 [ 6,  7],
 [ 7,  8],
 [ 8,  9],
 [ 9, 10],
 [11,  0],
 [12, 13],
 [13, 14],
 [14, 15],
 [15, 12]]
holes =[[-164.473 ,   81.1742]]

# rnd_segs = (np.round(segs)).astype(int)

sample_data = '{"vertices":[[-0.93068152666092,42.904937744141,10.968893051147],[2.3840835094452,35.953079223633,10.913777351379],[-6.2436285018921,34.559043884277,10.938244819641],[-7.8259248733521,41.398212432861,10.968675613403],[-4.390908241272,38.853408813477,10.887317657471],[-1.9934171438217,39.217456817627,10.908308029175],[-1.1641374826431,37.46993637085,10.984676361084],[-4.2356686592102,36.457679748535,10.902195930481]],"holes":[[-2.6779396533966,37.937980651855,10.98713684082]],"segments":[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4]]}'
tri_data = json.loads(sample_data)
verts = np.array(tri_data['vertices'])
res = np.delete(verts, 2, 1)
print(verts[1])

print(np.append(verts[1], 10))

pnt_dicts = {'vertices':pts, 'segments': segs,'holes':holes}
# print(pnt_dicts)
t = tr.triangulate(pnt_dicts, 'p')

# print(t)

tr.compare(plt,pnt_dicts,t)
# plt.show()