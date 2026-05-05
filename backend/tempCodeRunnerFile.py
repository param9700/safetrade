SIZE = 60
grid = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]

def plot(x, y):
    if 0 <= x < SIZE and 0 <= y < SIZE:
        grid[y][x] = '█'

def drawCircle(xc, yc, r):
    x = 0
    y = r
    p = 1 - r

    while x <= y:
        plot(xc + x, yc + y)
        plot(xc - x, yc + y)
        plot(xc + x, yc - y)
        plot(xc - x, yc - y)
        plot(xc + y, yc + x)
        plot(xc - y, yc + x)
        plot(xc + y, yc - x)
        plot(xc - y, yc - x)

        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1


def drawLine(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    err = dx - dy

    while True:
        plot(x1, y1)
        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def display():
    for i in range(SIZE - 1, -1, -1):
        print("".join(grid[i]))


drawCircle(30, 30, 15)


drawCircle(25, 35, 2)
drawCircle(35, 35, 2)


drawLine(25, 25, 35, 25)
drawLine(25, 25, 23, 27)
drawLine(35, 25, 37, 27)


display()