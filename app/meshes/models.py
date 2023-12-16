import numpy as np
import triangle as tr
from scipy.spatial import ConvexHull
from typing import List
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship, Session

from app.database import Base
from app.points.models import Point
from app.triangles.models import Triangle
from app.triangles.schemas import Triangle as tri_schema, TriangleCreate
from .schemas import Mesh as Mesh_Schema
# from .operations import interpolate_meshes

# the below two funciton sneed to be optimized, their for loopps are not ideal for findind and tracking
# which points form the smallest area plane between the two meshes
def min_distance(point:np.ndarray, point_list: List[np.ndarray]):
    min_dist = float('inf')

    for index, point_two in enumerate(point_list):
        dist = np.linalg.norm(point - point_two)
        if dist < min_dist:
            min_dist = dist
            closest_point = point_two
            closest_index = index

    return min_dist, closest_point, closest_index

def interpolate_meshes(mesh_one: Mesh_Schema, mesh_two: Mesh_Schema, db: Session):
    start_points = Point.get_points_by_mesh(mesh_one.id, db, as_vec=True)
    end_points = Point.get_points_by_mesh(mesh_two.id, db, as_vec=True)
    
    #first find the closest boundry point in mesh 1 to the bounry points in mesh two
    smalles_dist = float('inf')
    closest_start_point = start_points[0]
    for index, point in enumerate(start_points):
        dist_to_nearest_ednpoint, near_point_m2, closest_index_end_points = min_distance(point, end_points)
        if dist_to_nearest_ednpoint < smalles_dist:
            smalles_dist = dist_to_nearest_ednpoint
            closest_start_point = point
            closest_end_point = near_point_m2
            closest_index = index

    right_side_hull = ConvexHull(
        np.array([closest_start_point,
         closest_end_point,
         start_points[(closest_index+1)%len(start_points)],
         end_points[(closest_index_end_points+1)%len(end_points)]
         ]),
         qhull_options = 'QJ'
        )
    
    left_side_hull = ConvexHull(
        np.array([closest_start_point,
         closest_end_point,
         start_points[(closest_index-1)%len(start_points)],
         end_points[closest_index_end_points-1]
         ]),
         qhull_options = 'QJ'
        )
  
    closest_start_point_2 = start_points[(closest_index-1)%len(start_points)]
    closest_end_point_2 = end_points[(closest_index_end_points+1)%len(end_points)]
    if right_side_hull.area < left_side_hull.area:
        closest_start_point_2 = start_points[(closest_index+1)%len(start_points)]
        closest_end_point_2 = end_points[(closest_index_end_points-1)%len(end_points)]


    centroid  = np.mean([closest_start_point, closest_end_point, closest_start_point_2, closest_end_point_2], axis=0)
    # vertex_arr = np.array([closest_start_point, closest_end_point, closest_start_point_2, closest_end_point_2, centroid])
    # print(vertex_arr)

    # print(vertex_arr.shape)

    # points_tuple = tuple(tuple(point) for point in vertex_arr.transpose()[:2].transpose())
    # print(points_tuple)
    # hieght_vals = np.round(vertex_arr.transpose()[2], decimals=2)
    # hieght_dict = dict(zip(points_tuple, hieght_vals))

    # tri_data = {
    #     'vertices':np.delete(vertex_arr, 2, 1),
    #     'segments': [
    #         [0,1],[1,2],[2,3],[3,0]
    #     ]
    # }

    # print(tri_data)
    
    # triangulation_data = tr.triangulate(tri_data, 'pICDq')

    # print('+++++++++++++++++++++++++++++++++++')
    # print(triangulation_data)

    # triangles = triangulation_data['triangles'].tolist()
    # point_arr = triangulation_data['vertices'].tolist()

    # point_dict_keys = ['x', 'y', 'z']
    # triangle_list = []
    # for tri in triangles:
    #     point_list = []
    #     for point_index in tri:
    #         point = point_arr[point_index]
    #         hieght = hieght_dict.get((point[0], point[1]), np.mean(vertex_arr[:, 2]))
    #         point_with_hieght = np.append(point, hieght).tolist()
    #         point_dict = dict(zip(point_dict_keys, point_with_hieght))
    #         point_dict['is_boundry'] = False
    #         point_dict['is_hole'] = False
    #         point_list.append(point_dict)

    #     tri_init = {
    #         'mesh_id': 1,
    #         'level_id':1,
    #         'points': point_list
    #     }
    #     print(tri_init)
    #     tri_obj = Triangle(
    #         TriangleCreate(mesh_id=1, level_id=1, points=point_list)
    #     )
    #     tri_obj.save(db)
    #     triangle_list.append(tri_obj)
    
    # mesh_obj = Mesh(triangle_list, level_id=1)
    # mesh_obj.save(db)



    #couldn't get triangulate to make triangles i like so just defined my own with a centroid
    
    point_dict_keys = ['x', 'y', 'z']

    points_one = [closest_start_point, centroid, closest_end_point_2]
    tri_points_one = []
    for point in points_one:
        point_dict = dict(zip(point_dict_keys, point))
        point_dict['is_boundry'] = False
        point_dict['is_hole'] = False
        tri_points_one.append(point_dict)
    tri_one = Triangle(
        TriangleCreate(
            mesh_id=mesh_one.id,
            level_id=mesh_one.level_id,
            points=tri_points_one
            )
    )
    tri_one.save(db)

    points_two = [closest_end_point_2, centroid, closest_end_point]
    tri_points_two = []
    for point in points_two:
        point_dict = dict(zip(point_dict_keys, point))
        point_dict['is_boundry'] = False
        point_dict['is_hole'] = False
        tri_points_two.append(point_dict)

    tri_two = Triangle(
        TriangleCreate(
            mesh_id=mesh_one.id,
            level_id=mesh_one.level_id,
            points=tri_points_two
            )
    )
    tri_two.save(db)

    points_three= [closest_end_point, centroid, closest_start_point_2]
    tri_points_three = []
    for point in points_three:
        point_dict = dict(zip(point_dict_keys, point))
        point_dict['is_boundry'] = False
        point_dict['is_hole'] = False
        tri_points_three.append(point_dict)

    tri_three = Triangle(
        TriangleCreate(
            mesh_id=mesh_one.id,
            level_id=mesh_one.level_id,
            points=tri_points_three
            )
    )
    tri_three.save(db)

    points_four= [closest_start_point_2, centroid, closest_start_point]
    tri_points_four = []
    for point in points_four:
        point_dict = dict(zip(point_dict_keys, point))
        point_dict['is_boundry'] = False
        point_dict['is_hole'] = False
        tri_points_four.append(point_dict)

    tri_four = Triangle(
        TriangleCreate(
            mesh_id=mesh_one.id,
            level_id=mesh_one.level_id,
            points=tri_points_four
            )
    )
    tri_four.save(db)
    
    # # mesh_obj = Mesh([tri_one,tri_two], level_id=1)
    # # mesh_obj.save(db)
    
    return [tri_one,tri_two,tri_three,tri_four]
    # return triangle_list


class Mesh(Base):
    """
    
    """
    __tablename__ = "meshes"

    id = Column(Integer, primary_key=True, index=True)
    triangles = relationship(Triangle, backref='triangles', uselist=True)
    # points = relationship(Point, backref='points', uselist=True)
    # holes = relationship(Point, backref='points', uselist=True)
    level_id = Column(Integer, index=True, nullable=True)
    
    def __init__(self,
                 triangles: List[tri_schema]|List[TriangleCreate],
                #  points: List[Point]| List[PointCreate],
                 level_id=None):
        
        self.level_id = level_id

        for tri in triangles:
            self.triangles.append(tri)
            # self.points = self.points + tri.points
            # for point in tri.points:
            #     point.mesh_id = self.id
            #     point.save

        # for point in points:
        #     self.points.append(point)

    def save(self, db: Session):
        """
        adds a point to the database
        """

        db.add(self)
        db.commit()
        db.refresh(self)

        # update point tbale with mesh ids
        for triangle in self.triangles:
            for point in triangle.points:
                point.mesh_id = self.id
                point.save(db)
            triangle.mesh_id = self.id
            triangle.save(db)

        return self
    
    @staticmethod
    def get_all(db:Session):
        return db.query(Mesh).all()
    
    @staticmethod
    def get_mesh_by_id(mesh_id:int, db:Session):
        query = db.query(Mesh)
        query_filter = query.filter(Mesh.id == mesh_id)
        results = query_filter.first()
        return results

    @staticmethod
    def concat_meshes(mesh_1: Mesh_Schema, mesh_2: Mesh_Schema, db: Session):

        if mesh_1.level_id != mesh_2.level_id:
            raise TypeError(f'Mesh 1 is from level {mesh_1.level_id}, while Mesh 2 is from level {mesh_2.level_id}')
        
        combined_tris = mesh_1.triangles + mesh_2.triangles
        new_mesh = Mesh(combined_tris, level_id=mesh_1.level_id)
        new_mesh.save(db)
        
        return new_mesh
    
    @staticmethod
    def merge_meshes(mesh_1: Mesh_Schema, mesh_2: Mesh_Schema, db: Session):
        """
        Starting from mesh one, combines the two meshes by finding the smallest area plane between their respective boundry points
        """
        if mesh_1.level_id != mesh_2.level_id:
            raise TypeError(f'Mesh 1 is from level {mesh_1.level_id}, while Mesh 2 is from level {mesh_2.level_id}')
        
        connecting_tris = interpolate_meshes(mesh_1, mesh_2, db)

        print('======================================')
        print(connecting_tris)
        print(mesh_1.triangles)
        print(mesh_2.triangles)
        tri_list = mesh_1.triangles + mesh_2.triangles
        for old_tri in  tri_list:
            new_tri = old_tri.tri_copy(db)
            connecting_tris.append(new_tri)

        print(connecting_tris)
        print('======================================')
        new_mesh = Mesh(connecting_tris, level_id=mesh_1.level_id)
        new_mesh.save(db)
        
        return new_mesh