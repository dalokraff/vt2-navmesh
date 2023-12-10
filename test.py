"""
Probably need to turn this into unittests instead of a scratchpad.
Depends on how expansive the main app becomes.
"""
import matplotlib.pyplot as plt
import numpy as np
import triangle as tr

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

segs = [[ 0.,  1.],
 [ 1.,  2.],
 [ 2.,  3.],
 [ 3.,  4.],
 [ 4.,  5.],
 [ 5.,  6.],
 [ 6.,  7.],
 [ 7.,  8.],
 [ 8.,  9.],
 [ 9., 10.],
 [11.,  0.],
 [12., 13.],
 [13., 14.],
 [14, 15],
 [15., 12.]]
holes =[[-164.473 ,   81.1742]]

rnd_segs = (np.round(segs)).astype(int)

pnt_dicts = {'vertices':pts, 'segments': rnd_segs,'holes':holes}
t = tr.triangulate(pnt_dicts, 'p')

print(t)

tr.compare(plt,pnt_dicts,t)
plt.show()