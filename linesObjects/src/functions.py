class Line:
    def __init__(self, x1_, y1_, x2_, y2_):
        from math import atan
        self.x1 = x1_
        self.y1 = y1_
        self.x2 = x2_
        self.y2 = y2_
        y21 = self.y2-self.y1
        x21 = self.x2-self.x1
        if y21*x21 > 0:
            self.m  = atan(y21/x21)
        else:
            self.m  = -atan(y21/x21)
        self.q = self.y2 - self.m*self.x2

    def show(self, screen):
        import pygame
        white = (255, 255, 255)
        pygame.draw.line(screen, white, (self.x1, self.y1), (self.x2, self.y2))


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
    m1 = l1.m
    m2 = l2.m
    q1 = l1.q
    q2 = l2.q
    if m1 == m2:
        return (l2.x2, l2.y2)
    x = (q2-q1) / (m1-m2)
    y = m1*x + q1
    if ((l1.x1 < x and l1.x2 < x) or (l1.x1 > x and l1.x2 > x)):
        return (l2.x2, l2.y2)
    # if ((l2.x1 < x and l2.x2 < x) or (l2.x1 > x and l2.x2 > x)):
    #     return (l2.x2, l2.y2)

    if ((l1.y1 < y and l1.y2 < y) or (l1.y1 > y and l1.y2 > y)):
        return (l2.x2, l2.y2)
    return (x, y)

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
    from numpy import pi, cos, sin, sqrt
    black = (  0,  0,  0)
    white = (255,255,255)
    n = 20
    delta = pi/n*2
    pygame.init()
    WIDTH  = 800
    HEIGHT = 800
    r      = 800*sqrt(2)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lines")
    running = True
    l = Line(200,300,400,360)
    print(l.m, l.q)
    while running:
        window = pygame.Surface((WIDTH, HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                (xMouse, yMouse) = pygame.mouse.get_pos()
                for i in range(1, 2):
                    ll  = Line(xMouse, yMouse, xMouse + r*cos(delta*i), yMouse + r*sin(delta*i))
                    print(ll.m, ll.q)
                    (x, y) = check_intersection(l, ll)
                    pygame.draw.line(window, white, (xMouse, yMouse), (x, y))
                screen.blit(window, (0,0))
                l.show(screen)
        pygame.display.update()
