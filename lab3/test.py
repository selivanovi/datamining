import cmath
import math
import random
import sys

import numpy as np
from numpy import sqrt
from pandas import DataFrame


class Data:
    def __init__(self):
        self.df = None

    def set_data(self, df):
        self.df = df


class KMeans:
    def __init__(self, n_clusters):
        self.n_clusters = n_clusters
        self.clusters = None
        self.points = None

    def fit(self, x):
        points = []
        for i in x:
            points.append([int(i[0]), int(i[1]), 0])

        self.points = DataFrame(points, columns=['x', 'y', 'cluster'])
        print(self.points)

        self.__create_cluster(x)
        print(self.clusters)

        self.__distribute_point(self.points, self.clusters)
        # self.__distribute_points_in_clusters(self.array_points, self.array_clusters)
        # while self.__check_cluster(self.array_clusters):
        #     self.__create_new_center(self.array_clusters)
        #     self.__distribute_points_in_clusters(self.array_points, self.array_clusters)

    def __create_cluster(self, x):
        max_x = max(x[0])
        max_y = max(x[1])
        array_point = []
        for i in range(self.n_clusters):
            array_point.append([random.randint(0, max_x), random.randint(0, max_y)])
        self.clusters = DataFrame(array_point, columns=['x', 'y'])

    def __distribute_point(self, points, clusters):
        for index, row in points.iterrows():
            row['cluster'] = self.__check_cluster(row['x'], row['y'], clusters)
        print(points)

    def __check_cluster(self, x, y, clusters):
        min_distance = sys.maxsize
        cluster = 0
        for index, cluster in clusters.iterrows():
            distance = math.sqrt(pow(x - cluster['x'], 2) + pow(y - cluster['y'], 2))
            if distance < min_distance:
                min_distance = distance
                cluster = index
        return cluster

    # def __create_new_center(self, array_clusters):
    #     for cluster in array_clusters:
    #         cluster.old_center = cluster.center
    #         cluster.center = cluster.new_center()
    #         cluster.array_points.clear()
    #     for index, cluster in clusters.iterrows():
    #         if cluster.old_center is None:
    #             return True
    #         if abs(cluster.center.x - cluster.old_center.x) < 1e-5 and abs(
    #                 cluster.center.y - cluster.old_center.y) < 1e-5:
    #             result = False
