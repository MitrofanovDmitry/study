import math
import random as rn
import tkinter as tk

WIDTH = 800
HEIGHT = 600
GRAVITY = 5
TICK_DELAY = 50

root = None
canvas = None

gun = None
bullets = None
targets = None

class Gun:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT - 50
        self.width = 20
        self.length = 100
        self.color = 'yellow'
        self.force = 0

        self.id = canvas.create_line(
                self.x, self.y, self.x + self.length, self.y, 
                width=self.width, fill=self.color)

    def direct(self, x, y):

        dx, dy = x - self.x, y - self.y
        k = math.sqrt(dx**2 + dy**2) / self.length
        self.dx, self.dy = dx//k, dy//k

        canvas.coords(self.id, self.x, self.y, 
                      self.x + self.dx, self.y + self.dy)

    def load(self):
        # timer
        pass

    def shoot(self):
        x = self.x + self.dx
        y = self.y + self.dy
        dx, dy = self.dx, self.dy
        bullets.append(Bullet(x, y, dx, dy))


class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.r = 10
        self.dx = dx
        self.dy = dy
        self.color = 'red'

        self.id = canvas.create_oval(
            self.x - self.r, self.y - self.r, 
            self.x + self.r, self.y + self.r, fill=self.color)

    def move(self):
        
        self.dy += GRAVITY
        self.x += self.dx
        self.y += self.dy

        canvas.coords(self.id, 
            self.x - self.r, self.y - self.r, 
            self.x + self.r, self.y + self.r)

    def is_outside(self):
        
        if (self.x - self.r) <= 0:
            return True

        if (self.x + self.r) >= WIDTH:
            return True

        if (self.y - self.r) <= 0:
            return True

        if (self.y + self.r) >= HEIGHT:
            return True

        return False

    def is_inside(self, target):
        dx = self.x - target.x
        dy = self.y - target.y
        dist = math.sqrt(dx**2 + dy**2)
        return dist <= (self.r + target.r)

    def destroy(self):
        canvas.delete(self.id)


class Target:
    def __init__(self):
        self.r = 30
        self.x = WIDTH - 50
        self.y = rn.randint(self.r, HEIGHT - self.r)
        self.dx = 0
        self.dy = rn.randint(5, 15)
        self.color = 'blue'

        self.id = canvas.create_oval(
            self.x - self.r, self.y - self.r, 
            self.x + self.r, self.y + self.r, fill=self.color)

    def move(self):
        
        self.x += self.dx
        self.y += self.dy

        if (self.x - self.r) <= 0:
            self.x = self.r
            self.dx = -self.dx

        if (self.x + self.r) >= WIDTH:
            self.x = WIDTH - self.r
            self.dx = -self.dx

        if (self.y - self.r) <= 0:
            self.y = self.r
            self.dy = -self.dy

        if (self.y + self.r) >= HEIGHT:
            self.y = HEIGHT - self.r
            self.dy = -self.dy

        canvas.coords(self.id, 
            self.x - self.r, self.y - self.r, 
            self.x + self.r, self.y + self.r)

    def destroy(self):
        canvas.delete(self.id)

def destroy_bullet(bullet):
    bullet.destroy()
    bullets.remove(bullet)

def destroy_target(target):
    target.destroy()
    targets.remove(target)

def tick():

    for target in targets:
        target.move()
        
    for bullet in bullets:    
        bullet.move()

        if bullet.is_outside():
            destroy_bullet(bullet)
        
        for target in targets:
            if bullet.is_inside(target):
                destroy_bullet(bullet)
                destroy_target(target)

    root.after(TICK_DELAY, tick)


def main():
    
    global root, canvas
    global gun, bullets, targets

    root = tk.Tk()
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)

    gun = Gun()
    targets = [Target() for _ in range(3)]
    bullets = []

    canvas.bind("<Button-1>", lambda ev: gun.load())
    canvas.bind("<ButtonRelease-1>", lambda ev: gun.shoot())
    canvas.bind("<Motion>", lambda ev: gun.direct(ev.x, ev.y))
    canvas.pack()

    tick()
    tk.mainloop()


main()
