import math

def get_cluster_distrance(cluster1, cluster2, distance_method):
    cluster1_size = len(cluster1)
    cluster2_size = len(cluster2)
    point_dim = len(cluster1[0])
    all_distances = [0] * (cluster1_size * cluster2_size)

    k = 0
    for i in range(cluster1_size):
        for j in range(cluster2_size):
            #sub = [(x1 - x2) ** 2 for (x1, x2) in zip(cluster1[i], cluster2[j])]            
            #all_distances[k] = math.sqrt(sum(sub))
            sq = 0
            for d in range(point_dim):
                sq += (cluster1[i][d] - cluster2[j][d]) ** 2
            all_distances[k] = math.sqrt(sq)
            #all_distances[k] = sq

            k += 1

    if distance_method == 0:
        return min(all_distances)
    elif distance_method == 1:
            return max(all_distances)
    elif distance_method == 2:
        return sum(all_distances) / len(all_distances)
    else:
        raise Exception('Bad Distance Method!')

def getAHC(points, K, distance_method):
    point_count = len(points)
    cluster_count = point_count
    clusters = [[i] for i in range(cluster_count)]

    while cluster_count > K:
        min_distance = 1e20 #math.inf
        min_x = 0
        min_y = 0
        for x in range(cluster_count - 1):
            for y in range((x + 1), cluster_count):
                cluster1_points = [points[i] for i in clusters[x]]
                cluster2_points = [points[i] for i in clusters[y]]
                d = get_cluster_distrance(cluster1_points, cluster2_points, distance_method)
                if d < min_distance:
                    min_x = x
                    min_y = y
                    min_distance = d

        clusters[min_x] = clusters[min_x] + clusters[min_y]
        del clusters[min_y]

        cluster_count -= 1

    return clusters

# coordinates = [[51.5217, 30.1140],
#                 [27.9698, 27.0568],
#                 [10.6233, 52.4207],
#                 [122.1483, 6.9586],
#                 [146.4236, -41.3457]]
# coordinates = [[1, 1],
#                 [100, 200],
#                 [2, 2],
#                 [101, 201],
#                 [3, 2]]

# Cluster_K = 2
# Cluster_Distance_Method = 0
# Coordinates_Count = len(coordinates)

head = [int(i) for i in input().split()] 
Coordinates_Count = head[0]
Cluster_K = head[1]
Cluster_Distance_Method = head[2]
coordinates = [0 for i in range(Coordinates_Count)]
for i in range(Coordinates_Count):
    pt = [float(i) for i in input().split()] 
    coordinates[i] = pt

clusters = getAHC(coordinates, Cluster_K, Cluster_Distance_Method)

output =  [0 for i in range(Coordinates_Count)]
for cluster_id in range(Cluster_K):
    for e in clusters[cluster_id]:
        output[e] = cluster_id

for i in range(Coordinates_Count):
    print(output[i])