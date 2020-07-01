import sys
from PIL import Image
from astar import AStar


def is_blocked(p):
    x, y = p
    pixel = path_pixels[x, y]
    if any(c < 225 for c in pixel):
        return True


def von_neumann_neighbors(p):
    x, y = p
    neighbors = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
    return [p for p in neighbors if not is_blocked(p)]


def manhattan(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])


def squared_euclidean(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2


start = (400, 984)
goal = (398, 25)

# invoke: python mazesolver.py <mazefile> <outputfile>[.jpg|.png|etc.]

path_img = Image.open(sys.argv[1])
path_pixels = path_img.load()
print(path_img, path_pixels)

distance = manhattan
heuristic = manhattan
print(distance, heuristic)

path = AStar(start, goal, von_neumann_neighbors, distance, heuristic)

# for position in path:
#     x, y = position
#     path_pixels[x, y] = (255, 0, 0)  # red

path_img.save(sys.argv[2])
