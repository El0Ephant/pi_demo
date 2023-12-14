import math
import random

import pandas as pd
import matplotlib.pyplot as plt


class Point:
    def __init__(self, coord, val=-1, clust=-1, noise=None):
        self.coord = coord
        self.clust = clust
        self.val = val
        self.noise = noise

    def dist(self, point):
        res = 0.0
        for i in range(4):
            res += (float(self.coord[i]) - float(point.coord[i])) ** 2
        return math.sqrt(res)


class Cluster(Point):
    def __init__(self, coord, clust):
        super().__init__(coord, clust)
        self.n = 0


def reeval_clusters(points, clusters):
    for cluster in clusters:
        cluster.coord = [0.0, 0.0, 0.0, 0.0]
        cluster.n = 0
    for point in points:
        clusters[point.clust].n += 1
        for i in range(4):
            clusters[point.clust].coord[i] += point.coord[i]
    for cluster in clusters:
        if cluster.n != 0:
            for i in range(4):
                cluster.coord[i] /= cluster.n


def draw_points(points, clust_colors, val=False):
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))

    n = 0
    for i in range(4):
        for j in range(i + 1, 4):
            ix = int(n / 3)
            iy = int(n % 3)
            for k in range(0, len(points)):
                if val:
                    axes[ix][iy].scatter(points[k].coord[i], points[k].coord[j], c=clust_colors[points[k].val], s=20)
                else:
                    axes[ix][iy].scatter(points[k].coord[i], points[k].coord[j], c=clust_colors[points[k].clust], s=20)

            axes[ix][iy].set_xlabel('$Axis: (' + str(i) + ',' + str(j) + ')$', fontsize=10)
            axes[ix][iy].set_xticks([])
            axes[ix][iy].set_yticks([])
            n += 1
        fig.tight_layout()
    plt.show()


def k_means(points, clusters):
    for point in points:
        min_dist = clusters[0].dist(point)
        res_clust = 0
        for i in range(1, len(clusters)):
            if clusters[i].dist(point) < min_dist:
                res_clust = i
        point.clust = res_clust


def max_count(points):
    clusters_no = list(map(lambda x: x.clust, points))
    return max(set(clusters_no), key=clusters_no.count)


def neighbours(point: Point, points: list):
    return sorted(filter(lambda x: x.clust != -1, points), key=lambda p: point.dist(p))[0:5]


def k_nearest(points):
    while len(list(filter(lambda x: x.clust == -1, points))) > 0:
        for point in points:
            neighs = neighbours(point, points)
            cluster = max_count(neighs)
            point.clust = cluster


def quality_to_clust(quality):
    return 0 if quality <= 5 else 1


if __name__ == '__main__':
    frame = pd.read_csv('wine.csv')
    print(frame)

    # points = [
    #     Point([frame["density"][i], frame["citric acid"][i], frame["residual sugar"][i], frame["chlorides"][i]],
    #           quality_to_clust(frame["quality"][i]))
    #     for i in range(len(frame))]

    points = [
        Point([frame["density"][i], frame["citric acid"][i], frame["residual sugar"][i], frame["chlorides"][i]],
              quality_to_clust(frame["quality"][i]), clust=quality_to_clust(frame["quality"][i]) if i < 30 else -1)
        for i in range(len(frame))]

    min_coord = [100, 100, 100, 100]
    max_coord = [0, 0, 0, 0]
    for point in points:
        for i in range(4):
            if point.coord[i] < min_coord[i]:
                min_coord[i] = point.coord[i]
            if point.coord[i] > max_coord[i]:
                max_coord[i] = point.coord[i]

    clusters = [Cluster(min_coord, 0), Cluster(max_coord, 1)]
    # clusters = []
    clust_colors = {-1: "black", 0: "blue", 1: "red"}
    # clust_colors = {-1: "black"}
    val_colors = {-1: "black", 0: "blue", 1: "red"}

    for n in range(5):
        k_nearest(points)
        # k_means(points, clusters)
        # reeval_clusters(points, clusters)
    draw_points(points, clust_colors)

    success_n = 0
    for point in points:
        if point.clust == point.val:
            success_n += 1
    point_n = 200
    print("Accuracy")
    print(success_n / point_n)
