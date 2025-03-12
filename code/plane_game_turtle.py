import turtle
import random

def change_direction(bounce):
    if bounce == 'left' or bounce == 'right':
        plane.setheading(180 - plane.heading())
    elif bounce == 'top' or bounce == 'bottom':
        plane.setheading(-plane.heading())

def move_plane():
    plane.forward(2)
    x, y = plane.position()
    
    bounce = None
    if x > 390:
        bounce = 'right'
    elif x < -390:
        bounce = 'left'
    if y > 290:
        bounce = 'top'
    elif y < -290:
        bounce = 'bottom'
    
    if bounce:
        change_direction(bounce)
    
    screen.update()
    screen.ontimer(move_plane, 50)

# 设置屏幕
screen = turtle.Screen()
screen.title('飞机小游戏')
screen.bgcolor('white')
screen.tracer(0)  # 关闭自动刷新

# 创建飞机
plane = turtle.Turtle()
plane.shape('triangle')
plane.penup()
plane.speed(0)
plane.goto(random.randint(-390, 390), random.randint(-290, 290))
plane.setheading(random.randint(0, 360))

move_plane()

# 退出条件
screen.mainloop()