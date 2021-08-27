# Lines class, it has points, angolar coefficient and q of the line in case they are needed
class Line:
    def __init__(self, x1_, y1_, x2_, y2_):
        import sys
        from math import atan
        self.x1 = x1_
        self.y1 = y1_
        self.x2 = x2_
        self.y2 = y2_
        y21 = self.y2-self.y1
        x21 = self.x2-self.x1
        if x21 != 0:
            self.m  = y21/x21
            if y21*x21 > 0:
                self.a  = atan(self.m)
            else:
                self.a  = -atan(self.m)
        else:
            self.m = 1e6
        self.q = self.y2 - self.m*self.x2

    def show(self, screen):
        import pygame
        white = (255, 255, 255)
        pygame.draw.line(screen, white, (self.x1, self.y1), (self.x2, self.y2))

# class of Boxes in case you want to use boxes instead of lines
class Box:
    def __init__(self, l1_, l2_, l3_, l4_):
        self.l1 = l1_
        self.l2 = l2_
        self.l3 = l3_
        self.l4 = l4_
        # calculation for surface sizes
        self.edges = [self.l1, self.l2, self.l3, self.l4]
        self.minx  = min(self.l1.x1, self.l2.x1, self.l3.x1, self.l4.x1)
        self.minx  = min(self.minx, self.l1.x2, self.l2.x2, self.l3.x2, self.l4.x2)
        self.maxx  = max(self.l1.x1, self.l2.x1, self.l3.x1, self.l4.x1)
        self.maxx  = max(self.maxx, self.l1.x2, self.l2.x2, self.l3.x2, self.l4.x2)

        self.miny  = min(self.l1.y1, self.l2.y1, self.l3.y1, self.l4.y1)
        self.miny  = min(self.l1.y2, self.l2.y2, self.l3.y2, self.l4.y2, self.miny)
        self.maxy  = max(self.l1.y1, self.l2.y1, self.l3.y1, self.l4.y1)
        self.maxy  = max(self.l1.y2, self.l2.y2, self.l3.y2, self.l4.y2, self.maxy)

    def show(self, screen):
        import pygame
        for l in self.edges:
            pygame.draw.line(screen, white, (l.x1, l.y1), (l.x2, l.y2))

# Function to check if there is an intersection between 2 lines
def check_intersection(l1, l2):
    x1 = l1.x1
    x2 = l1.x2
    x3 = l2.x1
    x4 = l2.x2
    y1 = l1.y1
    y2 = l1.y2
    y3 = l2.y1
    y4 = l2.y2

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:                        # Parallel lines
        return (x4, y4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4))/den
    u =-((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))/den

    if t > 0 and t < 1 and u > 0:       # There's intersection
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return (x, y)
    else:                               # Out of boundaries of the lines
        return (x4, y4)

# Caluclate the distance between two points
def check_dist(x1, x2, y1, y2):
    from numpy import sqrt
    dist = (x2-x1)**2 + (y2-y1)**2
    dist = sqrt(dist)
    return dist

# class Player:
#     def __init__(self):


def start():
    import pygame
    from numpy import pi, cos, sin, sqrt
    black = (  0,  0,  0)
    white = (255,255,255)
    n = 100
    delta = pi/n*2
    pygame.init()
    WIDTH  = 1920
    HEIGHT = 1080
    r      = 800*sqrt(2)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lines")
    running = True
    l = Line(200,300,400,310)
    while running:
        window = pygame.Surface((WIDTH, HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                (xMouse, yMouse) = pygame.mouse.get_pos()
                for i in range(0,40):
                    ll  = Line(xMouse, yMouse, xMouse + r*cos(delta*i), yMouse + r*sin(delta*i))
                    (x, y) = check_intersection(l, ll)
                    pygame.draw.line(window, white, (xMouse, yMouse), (x, y))
                screen.blit(window, (0,0))
                l.show(screen)
        pygame.display.update()

# This works
def tr():
    import pygame
    from pygame.time import delay
    from random import randint
    from numpy import pi, cos, sin, sqrt
    from math import atan, tan
    black = (  0,  0,  0)
    white = (255,255,255)
    pygame.init()
    WIDTH  = 1920
    HEIGHT = 1080
    r      = max(WIDTH/2, HEIGHT)*sqrt(2)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lines")
    running = True
    nObstacles  = 10
    nRays       = 800
    delta       = pi/nRays/4
    obstacles = []
    lX = 100
    lY = 200
    for i in range(nObstacles):
        a = randint(0,WIDTH/2)
        b = randint(0,HEIGHT)

        obstacles.append(Line(a, b, a+randint(-lY, lY), b+randint(-lY, lY)))
    obstacles.append(Line(WIDTH/2, 0, WIDTH/2, HEIGHT))
    obstacles.append(Line(0, 0, 0, HEIGHT))
    obstacles.append(Line(0, 0, WIDTH/2, 0))
    obstacles.append(Line(0, HEIGHT, WIDTH/2, HEIGHT))
    distances   = [max(WIDTH/2, HEIGHT) for i in range(nRays)]
    boxes       = []
    direction   = 0
    xPlayer = WIDTH/4
    yPlayer = HEIGHT/2
    velocity= 1
    deltaX  = WIDTH/2/nRays
    maxTall= 200
    movementX  = 0
    while running:
        window = pygame.Surface((WIDTH/2, HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
                movementX = -1
            elif pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
                movementY = pi/2*3
            elif pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
                movementX = 1
            elif pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
                movementY = pi/2
            else:
                movementX = 0
                movementY = 0

        screen.fill(0)
        (xPlayer, yPlayer) = pygame.mouse.get_pos()

        # xMP = xPointing - xPlayer
        # yMP = yPointing - yPlayer

        # (xMouse, yMouse) = (200,330)
        # First screen
        direction += movementX*0.1
        for l in obstacles:
            pygame.draw.line(screen, white, (l.x1, l.y1), (l.x2, l.y2))
        for i in range(-int(nRays/2),int(nRays/2)):
            x           = xPlayer + r*cos(delta*i + direction)
            y           = yPlayer + r*sin(delta*i + direction)
            ll          = Line(xPlayer, yPlayer, x, y)
            minDist     = r
            indexDist   = -1
            for l in obstacles:
                (x1, y1)    = check_intersection(l, ll)
                dist        = check_dist(xPlayer, x1, yPlayer, y1)
                if dist < minDist:
                    minDist     = dist
                    (x, y)      = (x1, y1)
            pygame.draw.line(screen, white, (xPlayer, yPlayer), (x, y))
            distances[i+int(nRays/2)] = minDist
            # Second screen (3D)
        for i in range(nRays):
            x = deltaX*i + WIDTH/2
            h = HEIGHT-distances[i]/sqrt(2)
            surf    = pygame.Surface((1, h))
            surf.fill((255,255,255))
            surf.set_alpha(h*255/(HEIGHT*sqrt(2)))
            screen.blit(surf, (x, (HEIGHT-h)/2))
        pygame.display.flip()
