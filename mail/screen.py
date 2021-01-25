from math import sqrt
from time import sleep
from random import uniform
import pygame


CAPTION = "~~~"
SCREEN_W = 800
SCREEN_H = 600
ACCURACY = 5
MIN_SPEED = 1
MAX_SPEED = 2


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = uniform(MIN_SPEED, MAX_SPEED)
        self.dy = uniform(MIN_SPEED, MAX_SPEED)

    def __eq__(self, other):
        near_x = abs(self.x - other.x) < ACCURACY
        near_y = abs(self.y - other.y) < ACCURACY
        return near_x and near_y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __mul__(self, number):
        x = self.x * number
        y = self.y * number
        return Point(x, y)

    def __len__(self):
        return int(sqrt(self.x**2 + self.y**2))

    def pair(self):
        return int(self.x), int(self.y)


class Polyline:

    def __init__(self):
        self.points = []

    def toggle_point(self, x, y):
        point = Point(x, y)
        if point in self.points: self.points.remove(point)
        else: self.points.append(point)

    def del_last_point(self):
        if len(self.points): del self.points[-1]

    def set_points(self):
        for i in range(len(self.points)):
            self.points[i].x += self.points[i].dx
            self.points[i].y += self.points[i].dy
            if self.points[i].x > SCREEN_W: self.points[i].dx *= -1
            if self.points[i].y > SCREEN_H: self.points[i].dy *= -1
            if self.points[i].x < 0: self.points[i].dx *= -1
            if self.points[i].y < 0: self.points[i].dy *= -1

    def get_avg_dx(self):
        a = [abs(point.dx) for point in self.points]
        return sum(a) / len(a) if len(a) else 0

    def get_avg_dy(self):
        a = [abs(point.dy) for point in self.points]
        return sum(a) / len(a) if len(a) else 0

    def change_speed(self, percent):
        for i in range(len(self.points)):
            coeff = (100 + percent) / 100
            self.points[i].dx *= coeff
            self.points[i].dy *= coeff

    @staticmethod
    def draw_line(gamedisplay, points, color):
        for i in range(-1, len(points) - 1):
            curr_p = points[i].pair()
            next_p = points[i+1].pair()
            pygame.draw.line(gamedisplay, color, curr_p, next_p, 3)
    
    @staticmethod
    def draw_points(gamedisplay, points, color):
        for p in points:
            pygame.draw.circle(gamedisplay, color, p.pair(), 3)


class Knot(Polyline):

    def get_point(self, points, alpha, deg=None):
        if deg == 0: return points[0]
        if deg is None: deg = len(points) - 1
        return points[deg] * alpha + self.get_point(points, alpha, deg-1) * (1 - alpha)

    def get_points(self, base_points, count):
        points = []
        alpha = 1 / count
        
        for i in range(count):
            points.append(self.get_point(base_points, i * alpha))
        
        return points

    def get_knot(self, count):
        
        knot = []

        if len(self.points) < 3: return knot
        
        for i in range(-2, len(self.points) - 2):

            base_points = [
                (self.points[i] + self.points[i+1]) * 0.5, 
                 self.points[i+1],
                (self.points[i+1] + self.points[i+2]) * 0.5
            ]
            knot.extend(self.get_points(base_points, count))
        
        return knot


class MyScreenSaver:

    def __init__(self):
        
        self.steps = 35
        self.show_help = True
        self.show_info = True
        self.working = True
        self.pause = True
        self.hue = 0
        self.knot = Knot()
        
        pygame.init()
        pygame.display.set_caption(CAPTION)
        self.color = pygame.Color(0)
        self.gameDisplay = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    def handle_keydown(self, event):
        if event.key == pygame.K_h:
            self.show_help = not self.show_help
        if event.key == pygame.K_i:
            self.show_info = not self.show_info
        if event.key == pygame.K_r:
            self.pause = True
            self.knot = Knot()
        if event.key == pygame.K_p:
            self.pause = not self.pause
        if event.key == pygame.K_w:
            self.steps += 1
        if event.key == pygame.K_s:
            self.steps -= 1 if self.steps > 1 else 0
        if event.key == pygame.K_q:
            self.knot.change_speed(5)
        if event.key == pygame.K_a:
            self.knot.change_speed(-5)
        if event.key == pygame.K_ESCAPE:
            self.working = False

    def handle_mousebuttondown(self, event):
        if event.button == 1:
            x, y = event.pos
            self.knot.toggle_point(x, y)
        if event.button == 3:
            self.knot.del_last_point()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.working = False
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mousebuttondown(event)

    def draw_frame(self):
        self.gameDisplay.fill((0, 0, 0))
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)
        self.knot.draw_points(self.gameDisplay, self.knot.points, (255, 255, 255))
        self.knot.draw_line(self.gameDisplay, self.knot.get_knot(self.steps), self.color)

    def draw_text(self, x, y, text):
        color = (255, 255, 255)
        font = pygame.font.SysFont("serif", 14)
        self.gameDisplay.blit(font.render(text, True, color), (x, y))

    def draw_info(self):

        lines = [
            f'[dx] {self.knot.get_avg_dx():.2f}',
            f'[dy] {self.knot.get_avg_dy():.2f}',
            f'[hue] {self.hue}',
            f'[steps] {self.steps}',
            f'[points] {len(self.knot.points)}',
            '[pause]' if self.pause else ''
        ]

        for i in range(len(lines)):
            self.draw_text(10, 10 + 30 * i, lines[i])

    def draw_help(self):

        lines = [
            '[esc] exit',
            '[h] show help',
            '[i] show info',
            '[p] pause',
            '[r] restart',
            '[q] speed up',
            '[a] slow down',
            '[w] more steps',
            '[s] less steps',
            '[left click]  add / delete point',
            '[right click] delete last point'
        ]

        for i in range(len(lines)):
            self.draw_text(10, 220 + 30 * i, lines[i])

    def run(self):
        
        while self.working:
            
            for event in pygame.event.get():
                self.handle_event(event)

            if not self.pause: 
                self.knot.set_points()
            
            self.draw_frame()

            if self.show_info:
                self.draw_info()

            if self.show_help: 
                self.draw_help()

            pygame.display.flip()
            sleep(0.01)

        pygame.display.quit()
        pygame.quit()
        exit(0)


if __name__ == "__main__":
    screen_saver = MyScreenSaver()
    screen_saver.run()
