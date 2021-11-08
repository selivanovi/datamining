import cmath
import math
import random
import sys

import numpy as np
from numpy import sqrt


class Data:
    def __init__(self):
        self.df = None

    def set_data(self, df):
        self.df = df


class Cluster:
    def __init__(self, point):
        self.center = point
        self.old_center = None
        self.array_points = []
        self.array_old_points = []

    def set_center(self, point):
        self.center = point

    def new_center(self):
        sum_x = 0
        sum_y = 0
        length = len(self.array_points)
        for point in self.array_points:
            sum_x += point.x
            sum_y += point.y
        return Point(sum_x / length, sum_y / length)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def get_distance_between_points(point1, point2):
    return math.sqrt(pow(point1.x - point2.x, 2) + pow(point1.y - point2.y, 2))


class ArrayPoint:
    def __init__(self):
        self.points = []


class KMeans:
    def __init__(self, n_clusters):
        self.n_clusters = n_clusters
        self.array_points = []
        self.array_clusters = []

    def get_clusters_x(self):
        array = []
        for cluster in self.array_clusters:
            array.append(cluster.center.x)
        return array

    def get_clusters_y(self):
        array = []
        for cluster in self.array_clusters:
            array.append(cluster.center.y)
        return array

    def fit(self, x):
        self.array_points.clear()
        self.array_clusters.clear()
        for i in x:
            self.array_points.append(Point(int(i[0]), int(i[1])))

        self.__create_cluster(x)
        self.__distribute_points_in_clusters(self.array_points, self.array_clusters)
        while self.__check_cluster(self.array_clusters):
            self.__create_new_center(self.array_clusters)
            self.__distribute_points_in_clusters(self.array_points, self.array_clusters)

    def getWCSS(self):
        sum = 0
        for cluster in self.array_clusters:
            for point in cluster.array_points:
                sum += pow(get_distance_between_points(point, cluster.center), 2)
        return sum

    def __create_cluster(self, x):

        max_x = max(x[0])
        max_y = max(x[1])
        for i in range(self.n_clusters):
            self.array_clusters.append(Cluster(self.__create_random_point(max_x=max_x, max_y=max_y)))

    def __create_random_point(self, max_x, max_y):
        random_x = random.randint(0, max_x)
        random_y = random.randint(0, max_y)
        return Point(random_x, random_y)

    def __distribute_points_in_clusters(self, array_points, array_clusters):
        for point in array_points:
            self.__distribute_point(point, array_clusters)

    def __distribute_point(self, point, array_clusters):
        distance = sys.maxsize
        cluster_index = 0
        for i in range(len(array_clusters)):
            cluster = array_clusters[i].center
            length = get_distance_between_points(point, cluster)
            if distance > length:
                distance = length
                cluster_index = i
            array_clusters[cluster_index].array_points.append(point)

    def __check_cluster(self, array_clusters):
        result = True
        for cluster in array_clusters:
            if cluster.old_center is None:
                return True
            if abs(cluster.center.x - cluster.old_center.x) < 1e-5 and abs(cluster.center.y - cluster.old_center.y) < 1e-5:
                result = False
        return result

    def __create_new_center(self, array_clusters):
        for cluster in array_clusters:
            cluster.old_center = cluster.center
            cluster.center = cluster.new_center()
            cluster.array_points.clear()
