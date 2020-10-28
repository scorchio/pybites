from math import inf
from operator import itemgetter
import heapq


def calculate_parents(graph, start):
    distances = {vertex: inf for vertex in graph}
    parents = {vertex: None for vertex in graph}
    distances[start] = 0
    heap = [(0, start)]

    while len(heap) > 0:
        current_distance, current_vertex = heapq.heappop(heap)
        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parents[neighbor] = current_vertex
                heapq.heappush(heap, (distance, neighbor))
    return parents


def shortest_path(graph, start, end):
    """
       Input: graph: a dictionary of dictionary
              start: starting city   Ex. a
              end:   target city     Ex. b

       Output: tuple of (distance, [path of cites])
       Ex.   (distance, ['a', 'c', 'd', 'b])
    """
    parents = calculate_parents(graph, start)
    current = end
    next = parents[current]
    total_distance = 0
    path = [end]
    while current != start:
        total_distance += graph[current][next]
        path.append(next)
        current = next
        next = parents[current]
    shortest_path = list(reversed(path))
    return total_distance, shortest_path
