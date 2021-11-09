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
        self.clusters = []
        self.points = []

    def fit(self, x):
        for i in x:
            self.points.append([int(i[0]), int(i[1]), 0])

        self.points = np.array(self.points)
        self.__create_cluster(self.points)

        return DataFrame(self.__predicate(self.points, self.clusters))

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
        for i in range(self.n_clusters):
            self.clusters.append([random.randint(0, max_x), random.randint(0, max_y)])
        self.clusters = np.array(self.clusters)

    def __distribute_point(self, points, clusters):
        for point in points:
            point[2] = self.__check_cluster(point[0], point[1], clusters)

    def __check_cluster(self, x, y, clusters):
        min_distance = sys.maxsize
        с = 0
        for i in range(self.n_clusters):
            distance =np.sqrt(pow(x - clusters[i][0], 2) + pow(y - clusters[i][1], 2))
            if distance < min_distance:
                min_distance = distance
                с = i
        return с

    def __create_new_center(self, points, clusters):
        result = False
        for i in range(self.n_clusters):
            arrayPoint = list(filter(lambda x: x[2] == i, points))
            arrayX = [row[0] for row in arrayPoint]
            arrayY = [row[1] for row in arrayPoint]
            newX = sum(arrayX) / len(arrayX)
            newY = sum(arrayY) / len(arrayY)
            if (abs(clusters[i][0] - newX) < 1) and (abs(clusters[i][1] - newY) < 1):
                result = True
            else:
                clusters[i][0] = newX
                clusters[i][1] = newY

        return result



    def getSumOfSquareDistance(self):
        sum = 0
        for i in range(self.n_clusters):
            x = list(filter(lambda x: x[2] == i, self.points))
            for point in x:
                sum += pow(point[0] - self.clusters[i][0], 2) + pow(point[1] - self.clusters[i][1], 2)
        return sum
