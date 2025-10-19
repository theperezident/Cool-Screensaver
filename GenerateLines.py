# For building cool random lines

import random, time, config, os
from enum import Enum

# 2D coordinate system because nested lists are annoying

class Point:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def lookup(self, matrix):
        return matrix[self.y][self.x]
    
    def update(self, matrix, update):
        matrix[self.y][self.x] = update
        return matrix

def clear_console():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux (POSIX systems)
    else:
        _ = os.system('clear')

class Icons(Enum):
    EMPTY = ' '
    LINEV = '|'
    LINEH = '-'
    LINEX = '+'
    SPAWN = 'O'
    DEATH = 'X'
    WALL = '*'

class Direction(Enum):
    UP = 'up'
    LEFT = 'left'
    DOWN = 'down'
    RIGHT = 'right'

def showMatrix(matrix):
    for row in matrix:
        for cell in row:
            print(cell + ' ', end='')
        print()

def cycle(matrix, step_pause):
    clear_console()
    showMatrix(matrix)
    time.sleep(step_pause)


def checkDirections(matrix, point) -> list[Direction]:
    dim = len(matrix)
    possibilities = []

    if point.y < dim - 1 and not matrix[point.y + 1][point.x]:
        possibilities.append(Direction.DOWN)
    if point.y > 0 and not matrix[point.y - 1][point.x]:
        possibilities.append(Direction.UP)
    if point.x < dim - 1 and not matrix[point.y][point.x + 1]:
        possibilities.append(Direction.RIGHT)
    if point.x > 0 and not matrix[point.y][point.x - 1]:
        possibilities.append(Direction.LEFT)
    
    return possibilities

def buildPaths(split_steps, dim, end_pause):

    # Initialize matrix
    matrix = [[Icons.WALL.value for _ in range(dim)]]
    for i in range(dim - 2):
        matrix.append([Icons.WALL.value] + [Icons.EMPTY.value] * (dim - 2) + [Icons.WALL.value])
    matrix.append([Icons.WALL.value for _ in range(dim)])

    dibsMatrix = [[True for _ in range(dim)]]
    for i in range(dim - 2):
        dibsMatrix.append([True] + [False] * (dim - 2) + [True])
    dibsMatrix.append([True for _ in range(dim)])

    # Pick initial spawn
    spawn = Point(random.randint(1,dim-2),random.randint(1,dim-2))
    matrix = spawn.update(matrix, Icons.SPAWN.value)
    dibsMatrix = spawn.update(dibsMatrix, True)

    currentPoint = [spawn]
    nextPoint = [spawn]
    prevPoint = [spawn]
    cycleCount = 0

    while True:

        cycle(matrix, config.STEP_PAUSE)

        allDeath = []
        for point in currentPoint:
            allDeath.append(point.lookup(matrix) == Icons.DEATH.value)
        # print(allDeath) # DEBUG ONLY
        if all(allDeath):
            time.sleep(end_pause)
            break

        for i in range(len(currentPoint)):
            
            if currentPoint[i].lookup(matrix) == Icons.DEATH.value: continue

            directions = checkDirections(dibsMatrix,nextPoint[i])

            if len(directions) > 0:
                direction = random.choice(directions)
            else:
                nextPoint[i].update(matrix, Icons.DEATH.value)
                currentPoint[i] = nextPoint[i]
                prevPoint[i] = nextPoint[i]
                continue

            match direction:
                case Direction.UP:
                    nextPoint[i] = Point(nextPoint[i].x, nextPoint[i].y - 1)
                    nextPoint[i].update(dibsMatrix,True)
                case Direction.DOWN:
                    nextPoint[i] = Point(nextPoint[i].x, nextPoint[i].y + 1)
                    nextPoint[i].update(dibsMatrix,True)
                case Direction.LEFT:
                    nextPoint[i] = Point(nextPoint[i].x - 1, nextPoint[i].y)
                    nextPoint[i].update(dibsMatrix,True)
                case Direction.RIGHT:
                    nextPoint[i] = Point(nextPoint[i].x + 1, nextPoint[i].y)
                    nextPoint[i].update(dibsMatrix,True)

            if currentPoint[i].lookup(matrix) != Icons.EMPTY.value:
                pass
            elif cycleCount == config.SPLIT_STEPS:
                currentPoint.append(Point(currentPoint[i].x,currentPoint[i].y))
                prevPoint.append(Point(prevPoint[i].x,prevPoint[i].y))
                nextPoint.append(Point(nextPoint[i].x,nextPoint[i].y))
                currentPoint[i].update(matrix,Icons.SPAWN.value)
            elif prevPoint[i].x == currentPoint[i].x - 1 and nextPoint[i].x == currentPoint[i].x + 1:
                currentPoint[i].update(matrix,Icons.LINEH.value)
            elif prevPoint[i].x == currentPoint[i].x + 1 and nextPoint[i].x == currentPoint[i].x - 1:
                currentPoint[i].update(matrix,Icons.LINEH.value)
            elif prevPoint[i].y == currentPoint[i].y - 1 and nextPoint[i].y == currentPoint[i].y + 1:
                currentPoint[i].update(matrix,Icons.LINEV.value)
            elif prevPoint[i].y == currentPoint[i].y + 1 and nextPoint[i].y == currentPoint[i].y - 1:
                currentPoint[i].update(matrix,Icons.LINEV.value)
            else:
                currentPoint[i].update(matrix,Icons.LINEX.value)

            prevPoint[i] = currentPoint[i]
            currentPoint[i] = nextPoint[i]
        
        cycleCount += 1
        if cycleCount > config.SPLIT_STEPS: cycleCount -= config.SPLIT_STEPS