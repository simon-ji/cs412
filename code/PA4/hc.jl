head = parse.(UInt,split(readline(stdin)))
coordinates_count = head[1]
K = head[2]
distance_method = head[3]
coordinates = [[0.0, 0.0] for i in 1:coordinates_count]

for i in 1:coordinates_count
    pt = parse.(Float64, split(readline(stdin)))
    coordinates[i] = pt
end

println(coordinates)

function get_cluster_distrance(cluster1, cluster2, distance_method)
    cluster1_size = length(cluster1)
    cluster2_size = length(cluster2)
    all_distances = zeros(cluster1_size * cluster2_size)

    k = 1
    for i in 1:cluster1_size
        for j in 1:cluster2_size
            all_distances[k] = sqrt(sum((cluster1[i] .- cluster2[j]) .^ 2))
            k += 1
        end
    end
    if distance_method == 0
        return minimum(all_distances)
    elseif distance_method == 1
        return maximum(all_distances)
    elseif distance_method == 2
        return sum(all_distances) / length(all_distances)
    else
        error("Bad Distance Method!")
    end
end

function getAHC(points, K, distance_method)
    point_count = length(points)
    cluster_count = point_count
    clusters = [[i] for i in 1:cluster_count]

    while cluster_count > K
        min_distance = Inf
        min_x = 0
        min_y = 0
        for x in 1:cluster_count
            for y in (i + 1):cluster_count
                d = get_cluster_distrance(points[clusters[x]], points[clusters[y]], distance_method)
                if d < min_distance
                    min_x = x
                    min_y = y
                    min_distance = d
                end
            end
        end
        append!(clusters[min_x], clusters[min_y])
        clusters[min_y] = []
        clusters = filter(x -> length(x) > 0, clusters)

        cluster_count -= 1
    end

    return clusters
end

coordinates = [[51.5217, 30.1140],
                [27.9698, 27.0568],
                [10.6233, 52.4207],
                [122.1483, 6.9586],
                [146.4236, -41.3457]]
