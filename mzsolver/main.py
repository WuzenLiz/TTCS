import pygame
import random
import time
from Spot import Spot
from Button import Button


def current_milli_time(): return int(round(time.time()))


pygame.init()

width = height = 600
width_tot = width + 200

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
pathway = (69, 69, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BUTTON_Algo = (163, 96, 185)

WINDOW_SIZE = [width_tot, height]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Mo phong thuat toan A*")

done = False
clock = pygame.time.Clock()

# Thiết lập và vẽ lưới mô phỏng
cols = rows = 50

allow_diagonals = True
show_visited = False

grid = []
openSet = []
closedSet = []
path = []

saved_path = []

w = width / cols
h = height / rows

for i in range(cols):
    grid.append([])

for i in range(cols):
    for j in range(rows):
        grid[i].append(Spot(i, j, w, h, rows, cols))

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid, allow_diagonals)

start = grid[0][0]
end = grid[cols - 1][rows - 1]
start.wall = False
end.wall = False

# Hiển thị các nút
randomize = Button(width + 25, 30 + 0 * 55, 150, 50, 'Random',RED)
clear = Button(width + 25, 30 + 1 * 55, 150, 50, 'Clear',BLUE)
start = Button(width + 25, 30 + 3 * 55, 150, 50, 'A*',BUTTON_Algo)
start_path = Button(width + 25, 30 + 4 * 55, 150,
                    50, 'A* + PATH',  BUTTON_Algo)


def clear_grid():
    global openSet
    global closedSet
    global saved_path
    saved_path = []
    for i in range(rows):
        for j in range(cols):
            grid[i][j].wall = False
    openSet = []
    closedSet = []
    show_path = False


def randomize_grid():
    """Tạo ngẫu nhiên tường trong grid"""
    clear_grid()
    for i in range(rows):
        for j in range(cols):
            if random.random() < 0.4:
                grid[i][j].wall = True
    grid[0][0].wall = False #Xử lý nếu điểm khởi đầu bị đặt thành tường #Log_code_dev: 25/6/2020
    grid[rows - 1][cols - 1].wall = False  #Xử lý nếu điểm kết thúc bị đặt thành tường #Log_code_dev: 25/6/2020


start_enable = False
start_enable_rec = False


def start_general():
    global openSet
    global closedSet
    global path
    openSet = []
    closedSet = []
    path = []
    start = grid[0][0]
    openSet.append(start)
    end = grid[cols - 1][rows - 1]
    start.wall = False
    end.wall = False


def start_grid():
    start_general()

    global start_enable
    start_enable = True


time_start = 0

hold = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            clicked_sprites = [
                sprite for r in grid for sprite in r if sprite.rect.collidepoint(pos)]

            if clear.rect.collidepoint(pos) > 0:
                hold = False
                clear_grid()

            if randomize.rect.collidepoint(pos) > 0:
                hold = False
                randomize_grid()

            if start.rect.collidepoint(pos) > 0:
                time_start = current_milli_time()
                hold = False
                show_visited = False
                start_grid()

            if start_path.rect.collidepoint(pos) > 0:
                time_start = current_milli_time()
                hold = False
                show_visited = True
                start_grid()

            if len(clicked_sprites) > 0:
                # print(pos)
                clicked_sprites[0].wall = True
        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            clicked_sprites = [
                sprite for r in grid for sprite in r if sprite.rect.collidepoint(pos)]

            if len(clicked_sprites) > 0:
                clicked_sprites[0].wall = False

    if hold:
        continue

    if start_enable_rec:
        if len(openSet) > 0:
            current = openSet[0]

            if current == end:
                print('Tìm thấy đường đi khỏi mê cung trong trong ', (current_milli_time() -
                                   time_start), ' giây!')
                hold = True
                start_enable_rec = False
                saved_path = path

            openSet.remove(current)

            neighbors = current.neighbors
            for i in range(len(neighbors)):
                neighbor = neighbors[i]
                if neighbor not in closedSet and not neighbor.wall:
                    if neighbor not in openSet:
                        openSet.append(neighbor)
                        closedSet.append(neighbor)
                    neighbor.previous = current
            closedSet.append(current)
        else:
            print('Không có lời giải!')
            pygame.event.wait()
            break

    if start_enable:
        if len(openSet) > 0:
            winner = 0
            for i in range(len(openSet)):
                if openSet[i].f < openSet[winner].f:
                    winner = i

            current = openSet[winner]

            if current == end:
                print('Tìm thấy đường đi khỏi mê cung trong trong ', (current_milli_time() -
                                   time_start), ' giây!')
                hold = True
                start_enable = False
                saved_path = path

            openSet.remove(current)
            closedSet.append(current)

            neighbors = current.neighbors
            for i in range(len(neighbors)):
                neighbor = neighbors[i]
                if neighbor not in closedSet and not neighbor.wall:
                    tempG = current.g + 1

                    newPath = False
                    if neighbor in openSet:
                        if tempG < neighbor.g:
                            neighbor.g = tempG
                            newPath = True
                    else:
                        neighbor.g = tempG
                        openSet.append(neighbor)
                        newPath = True
                    if newPath:
                        neighbor.h = Spot.heuristic(neighbor, end)
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.previous = current
        else:
            print('Không có lời giải!')
            pygame.event.wait()
            break

    screen.fill(BLACK)

    randomize.show(screen)
    clear.show(screen)
    start.show(screen)
    start_path.show(screen)

    for i in range(cols):
        for j in range(rows):
            grid[i][j].show(screen, WHITE)

    if show_visited:
        for i in range(len(closedSet)):
            closedSet[i].show(screen, RED)

        for i in range(len(openSet)):
            openSet[i].show(screen, GREEN)

    if start_enable_rec or start_enable:
        # Find path
        path = []
        temp = current
        path.append(temp)
        while temp.previous:
            path.append(temp.previous)
            temp = temp.previous
        path.append(temp)
        temp.show(screen, BLUE)
        for i in range(len(path)):
            path[i].show(screen, BLUE)
    else:
        for i in range(len(saved_path)):
            saved_path[i].show(screen, BLUE)

    # clock.tick(60)
    pygame.display.flip()

pygame.quit()
