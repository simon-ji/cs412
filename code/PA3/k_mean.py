import pandas as pd
import numpy as np

def calc_distance(coord_1, coord_2):
    return np.linalg.norm(coord_1 - coord_2)

def calc_sse(points, centroid):
    sse = 0
    for i in range(0, points.shape[0]):
        sse += calc_distance(points[i], centroid) ** 2
    
    return sse

def k_mean(data, k, repeat = 10):
    centroids = data[np.random.randint(0, data.shape[0] - 1, k)]
    #centroids = sorted(centroids, key=lambda a: a[1])
    clusters = []
    SSEs = []
    dist = np.zeros(k)
    
    for r in range(0, repeat):
        #print("Repeat:", r)
        clusters.append({})
        SSEs.append(-1)
        sse_change = 100

        while sse_change > 1e-10:
            new_centroids = np.zeros((k, data.shape[1]))
            clusters[r] = {}
            for i in range(0, k):
                clusters[r][i] = set()

            for i in range(0, data.shape[0]):        
                for j in range(0, k):
                    dist[j] = calc_distance(data[i], centroids[j])
                cluster_id = np.argmin(dist)
                clusters[r][cluster_id].add(i)
                new_centroids[cluster_id] += data[i]

            for i in range(0, k):
                new_centroids[i] = new_centroids[i] / len(clusters[r][i])

            #centroids_diff = np.sum(np.abs(centroids - new_centroids))
            #print(centroids_diff)
            centroids = new_centroids

            new_sse = 0
            for i in range(0, k):
                new_sse += calc_sse(data[list(clusters[r][i]),], centroids[i])

            if SSEs[r] < 0:
                sse_change = new_sse
            else:
                sse_change = SSEs[r] - new_sse

            SSEs[r] = new_sse
            #print('sse:', SSEs[r], 'sse_change', sse_change)
    
    return clusters[np.argmin(SSEs)]

coordinates = np.array(pd.read_csv('places.csv',header=None))
K = 3
clusters=k_mean(coordinates, K)

for i in range(0, coordinates.shape[0]):
    for j in range(0, K):
        if i in clusters[j]:
            print("%d %d"%(i, j))
            break