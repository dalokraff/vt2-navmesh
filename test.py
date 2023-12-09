import matplotlib.pyplot as plt

import triangle as tr

# box = tr.get_data('box')

pts = [[0, 0], [0, 1], [1, 1], [1, 0], [0.3, 0.4], [0.3, 0.1], [0.1, 0.2], [0.8, 0.1], [0.8, 0.3], [0.6, 0.2]]
holes = [[0.25,0.26], [0.76, 0.25]]
segments = tr.convex_hull(pts)
segs = segments.tolist()

# t = tr.delaunay(pts)
# print(t)
# print(box)
pnt_dicts = {'vertices':pts, 'holes':holes}
t = tr.triangulate(pnt_dicts, 'CCD')

print(t)
tr.compare(plt,pnt_dicts,t)
plt.show()