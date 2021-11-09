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
        self.__create_cluster(x)

        return self.__predicate(self.points, self.clusters)

    def __predicate(self, points, clusters):
        print("distribute point")
        self.__distribute_point(points, clusters)
        print("create new center")
        if self.__create_new_center(points, clusters):
            print("True")
            return points
        print("False")
        return self.__predicate(points, clusters)

    def __create_cluster(self, x):
        max_x = max(x[0])
        max_y = max(x[1])
        array_point = []
        for i in range(self.n_clusters):
            array_point.append([random.randint(0, max_x), random.randint(0, max_y)])
        self.clusters = DataFrame(array_point, columns=['x', 'y'])

    def __distribute_point(self, points, clusters):
        for index, row in points.iterrows():
            cluster = self.__check_cluster(row['x'], row['y'], clusters)
            row['cluster'] = cluster

    def __check_cluster(self, x, y, clusters):
        min_distance = sys.maxsize
        с = 0
        for index, cluster in clusters.iterrows():
            distance = math.sqrt(pow(x - cluster['x'], 2) + pow(y - cluster['y'], 2))
            if distance < min_distance:
                min_distance = distance
                с = index
        return с

    def __create_new_center(self, points, clusters):
        result = False
        for index, cluster in clusters.iterrows():
            newX = points[points['cluster'] == index]['x'].sum() / len(points[points['cluster'] == index]['x'])
            newY = points[points['cluster'] == index]['y'].sum() / len(points[points['cluster'] == index]['y'])
            if (abs(cluster['x'] - newX) < 1) and (abs(cluster['y'] - newY) < 1):
                result = True
            else:
                cluster['x'] = newX
                cluster['y'] = newY

        return result

    def getSumOfSquareDistance(self):
        sum = 0
        for i, cluster in self.clusters.iterrows():
            x = self.points[self.points['cluster'] == i]
            for j, point in x.iterrows():
                sum += pow(point['x'] - cluster['x'], 2) + pow(point['y'] - cluster['y'], 2)
        return sum
