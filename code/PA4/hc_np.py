import numpy as np

def get_cluster_distrance(cluster1, cluster2, distance_method):
    cluster1_size = len(cluster1)
    cluster2_size = len(cluster2)
    all_distances = np.zeros(cluster1_size * cluster2_size)

    k = 0
    for i in range(cluster1_size):
        for j in range(cluster2_size):
            all_distances[k] = np.sqrt(np.sum((cluster1[i] - cluster2[j]) ** 2))
            k += 1

    if distance_method == 0:
        return np.min(all_distances)
    elif distance_method == 1:
            return np.max(all_distances)
    elif distance_method == 2:
        return np.mean(all_distances)
    else:
        raise Exception('Bad Distance Method!')

def getAHC(points, K, distance_method):
    point_count = len(points)
    cluster_count = point_count
    clusters = [[i] for i in range(cluster_count)]

    while cluster_count > K:
        min_distance = np.Inf
        min_x = 0
        min_y = 0
        for x in range(cluster_count - 1):
            for y in range((x + 1), cluster_count):
                d = get_cluster_distrance(points[clusters[x],], points[clusters[y],], distance_method)
                if d < min_distance:
                    min_x = x
                    min_y = y
                    min_distance = d

        clusters[min_x] = np.append(clusters[min_x], clusters[min_y])
        clusters = np.delete(clusters, min_y)
        # println(clusters)

        cluster_count -= 1

    return clusters

# coordinates = np.array([[1, 1],
#                 [100, 200],
#                 [2, 2],
#                 [101, 201],
#                 [3, 2]])

# Cluster_K = 2
# Cluster_Distance_Method = 0
# Coordinates_Count = len(coordinates)

head = np.array(input().split()).astype(np.integer)
Coordinates_Count = head[0]
Cluster_K = head[1]
Cluster_Distance_Method = head[2]
coordinates = np.array([np.zeros(2) for i in range(Coordinates_Count)])
for i in range(Coordinates_Count):
    pt = np.array(input().split()).astype(np.integer)
    coordinates[i] = pt

clusters = getAHC(coordinates, Cluster_K, Cluster_Distance_Method)

print(clusters)