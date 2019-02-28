import pandas as pd
import numpy as np

def calc_distance(coord_1, coord_2):
    return np.linalg.norm(coord_1 - coord_2)

def calc_sse(points, centroid):
    sse = 0
    for i in range(0, points.shape[0]):
        sse += calc_distance(points[i], centroid)

def k_mean(data, k, repeat = 3):
    centroids = coordinates[np.random.randint(0, data.shape[0] - 1, k)]
    #centroids = sorted(centroids, key=lambda a: a[1])
    dist = np.zeros(k)
    centroids_diff = 1

    while centroids_diff > 1e-10:
        new_centroids = np.zeros((k, data.shape[1]))
        cluster = {}
        for i in range(0, k):
            cluster[i] = set()

        for i in range(0, data.shape[0]):        
            for j in range(0, k):
                dist[j] = calc_distance(data[i], centroids[j])
            cluster_id = np.argmin(dist)
            cluster[cluster_id].add(i)
            new_centroids[cluster_id] += data[i]
        
        for i in range(0, k):
            new_centroids[i] = new_centroids[i] / len(cluster[i])

        centroids_diff = np.sum(np.abs(centroids - new_centroids))
        #print(centroids_diff)
        centroids = new_centroids
        
        sse = 0
        for i in range(0, k):
            sse += calc_sse(data[list(cluster[i]),], centroids[i])
        sse = sse
        #print(sse)
        
        return cluster

coordinates = np.array(pd.read_csv('places.csv',header=None))
a=k_mean(coordinates, 3)