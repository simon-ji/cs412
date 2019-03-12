import math

def getAHC(points, K, similarity_method):
    point_count = len(points)
    point_dim = len(points[0])
    cluster_count = point_count
    clusters = [[i] for i in range(cluster_count)]
    similarity_matrix = [[0] * point_count for i in range(point_count)]

#   Calcuate similarity between each point
    for i in range(point_count - 1):
        for j in range(i + 1, point_count):
            s = 0
            for d in range(point_dim):
                s += (points[i][d] - points[j][d]) ** 2
            s = math.sqrt(s)
            similarity_matrix[i][j] = s
            similarity_matrix[j][i] = s

    while cluster_count > K:
        min_distance = math.inf
        min_x = 0
        min_y = 0
        for x in range(cluster_count - 1):
            for y in range((x + 1), cluster_count):
                cluster_similarity = [0] * (len(clusters[x]) * len(clusters[y]))
                i = 0
                for c1 in clusters[x]:
                    for c2 in clusters[y]:
                        cluster_similarity[i] = similarity_matrix[c1][c2]
                        i += 1
                
                if similarity_method == 0:
                    d = min(cluster_similarity)
                elif similarity_method == 1:
                    d = max(cluster_similarity)
                elif similarity_method == 2:
                    d = sum(cluster_similarity) / len(cluster_similarity)
                else:
                    raise Exception('Bad Similarity Method!')

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
# Cluster_Similarity_Method = 0
# Coordinates_Count = len(coordinates)

head = [int(i) for i in input().split()] 
Coordinates_Count = head[0]
Cluster_K = head[1]
Cluster_Similarity_Method = head[2]
coordinates = [0 for i in range(Coordinates_Count)]
for i in range(Coordinates_Count):
    pt = [float(i) for i in input().split()] 
    coordinates[i] = pt

clusters = getAHC(coordinates, Cluster_K, Cluster_Similarity_Method)

output =  [0 for i in range(Coordinates_Count)]
for cluster_id in range(Cluster_K):
    for e in clusters[cluster_id]:
        output[e] = cluster_id

for i in range(Coordinates_Count):
    print(output[i])