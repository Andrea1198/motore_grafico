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
            if y21*x21 > 0:
                self.m  = atan(y21/x21)
            else:
                self.m  = -atan(y21/x21)
        else:
            self.m = sys.max_int
        self.q = self.y2 - self.m*self.x2

    def show(self, screen):
        import pygame
        white = (255, 255, 255)
        pygame.draw.line(screen, white, (self.x1, self.y1), (self.x2, self.y2))

# class Ray:
#

class Box:
    def __init__(self, l1_, l2_, l3_, l4_):
        self.l1 = l1_
        self.l2 = l2_
        self.l3 = l3_
        self.l4 = l4_
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
    if den == 0:
        return (x4, y4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4))/den
    u =-((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))/den
    if t > 0 and t < 1 and u > 0:
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return (x, y)
    else:
        return (x4, y4)

def check_dist(x1, x2, y1, y2):
    from numpy import sqrt
    dist = (x2-x1)**2 + (y2-y1)**2
    dist = sqrt(dist)
    return dist

def start():
    import pygame
    from numpy import pi, cos, sin, sqrt
    black = (  0,  0,  0)
    white = (255,255,255)
    n = 100
    delta = pi/n*2
    pygame.init()
    WIDTH  = 800
    HEIGHT = 800
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
                for i in range(n):
                    ll  = Line(xMouse, yMouse, xMouse + r*cos(delta*i), yMouse + r*sin(delta*i))
                    (x, y) = check_intersection(l, ll)
                    pygame.draw.line(window, white, (xMouse, yMouse), (x, y))
                screen.blit(window, (0,0))
                l.show(screen)
        pygame.display.update()

def tr():
    import pygame
    import sys
    from pygame.time import delay
    from random import randint
    from numpy import pi, cos, sin, sqrt
    black = (  0,  0,  0)
    white = (255,255,255)
    n = 200
    delta = pi/n*2
    pygame.init()
    WIDTH  = 800
    HEIGHT = 800
    r      = 800*sqrt(2)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lines")
    running = True
    nObstacles = 5
    obstacles = [Line(randint(0,WIDTH),randint(0,HEIGHT),randint(0,WIDTH),randint(0,HEIGHT)) for i in range(nObstacles)]
    while running:
        window = pygame.Surface((WIDTH, HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                screen.fill(0)
                (xMouse, yMouse) = pygame.mouse.get_pos()
                # (xMouse, yMouse) = (200,330)
                for i in range(n):
                    x = xMouse + r*cos(delta*i)
                    y = yMouse + r*sin(delta*i)
                    ll  = Line(xMouse, yMouse, xMouse + r*cos(delta*i), yMouse + r*sin(delta*i))
                    minDist = r
                    indexDist = -1
                    for i, l in enumerate(obstacles):
                        (x1, y1) = check_intersection(l, ll)
                        dist = check_dist(xMouse, x1, yMouse, y1)
                        if dist < minDist:
                            minDist = dist
                            indexDist = i
                            (x, y) = (x1, y1)
                        pygame.draw.line(screen, white, (l.x1, l.y1), (l.x2, l.y2))
                    pygame.draw.line(screen, white, (xMouse, yMouse), (x, y))

        pygame.display.update()
