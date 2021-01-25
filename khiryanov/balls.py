import random as rn
import tkinter as tk

WIDTH = 800
HEIGHT = 600
GRAVITY = 5
FRICTION = 0.995
TICK_DELAY = 50
BALLS_NUMBER = 10

root = None
canvas = None
balls = None

class Ball:
    def __init__(self):
        self.r = rn.randint(WIDTH // 100, WIDTH // 20)
        self.x = rn.randint(self.r, WIDTH - self.r)
        self.y = rn.randint(self.r, HEIGHT - self.r)
        dx = rn.randint(WIDTH // 100, WIDTH // 20)
        dy = rn.randint(HEIGHT // 100, HEIGHT // 20)
        self.dx = rn.choice([dx, -dx])
        self.dy = rn.choice([dy, -dy])
        self.color = rn.choice(['red','blue','yellow'])
        
        self.id = canvas.create_oval(
            self.x - self.r, self.y - self.r, 
            self.x + self.r, self.y + self.r, fill=self.color)

    def move(self):
        
        self.dy += GRAVITY
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
            self.dy = int(self.dy * FRICTION)
            self.dx = int(self.dx * FRICTION)

        canvas.coords(self.id, 
            self.x - self.r, self.y - self.r, 
            self.x + self.r, self.y + self.r)


def tick():
    for ball in balls: 
        ball.move()

    root.after(TICK_DELAY, tick)


def main():
    
    global balls, root, canvas

    root = tk.Tk()
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()
    
    balls = [Ball() for i in range(BALLS_NUMBER)]

    tick()
    tk.mainloop()
    
main()
