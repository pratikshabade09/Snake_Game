import turtle as t
import random
import time

w = 500
h = 500
food_size = 10
delay = 100

offsets = {
    "up": (0, 20),
    "down": (0,-20),
    "left": (-20,0),
    "right": (20,0)
}

SCORE = 0

def reset():
    global snake, snake_dir, food_position, SCORE
    SCORE = 0
    snake = [[0,0],[0,20],[0,40],[0,60],[0,80]]
    snake_dir = "up"
    food_position = get_random_food_position()
    food.goto(food_position)
    snake_turtle.clearstamps()
    move_snake()

def move_snake():
    global snake_dir, SCORE
    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_dir][0]
    new_head[1] += offsets[snake_dir][1]
    
    if new_head in snake[:-1]:
        print("Final Score:", SCORE)
        time.sleep(1)
        reset()
        return
    
    snake.append(new_head)

    if not food_collision():
        snake.pop(0)

    # Wrapping
    if snake[-1][0] > w/2: snake[-1][0] -= w
    elif snake[-1][0] < -w/2: snake[-1][0] += w
    elif snake[-1][1] > h/2: snake[-1][1] -= h
    elif snake[-1][1] < -h/2: snake[-1][1] += h

    snake_turtle.clearstamps()
    for segment in snake:
        snake_turtle.goto(segment[0], segment[1])
        snake_turtle.stamp()

    screen.update()
    t.ontimer(move_snake, delay)

def food_collision():
    global food_position, SCORE
    if get_distance(snake[-1], food_position) < 20:
        SCORE += 10
        food_position = get_random_food_position()
        food.goto(food_position)
        return True
    return False

def get_random_food_position():
    x = random.randint(-w//2 + food_size, w//2 - food_size)
    y = random.randint(-h//2 + food_size, h//2 - food_size)
    return (x, y)

def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return ((y2 - y1)**2 + (x2 - x1)**2)**0.5

def go_up():
    global snake_dir
    if snake_dir != "down": snake_dir = "up"
def go_down():
    global snake_dir
    if snake_dir != "up": snake_dir = "down"
def go_left():
    global snake_dir
    if snake_dir != "right": snake_dir = "left"
def go_right():
    global snake_dir
    if snake_dir != "left": snake_dir = "right"

screen = t.Screen()
screen.setup(w, h)
screen.title("Snake Game")
screen.bgcolor("lightgrey")
screen.tracer(0)

snake_turtle = t.Turtle("square")
snake_turtle.penup()

food = t.Turtle("circle")
food.color("red")
food.shapesize(food_size / 20)
food.penup()

screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")

reset()
try:
    t.done()
except KeyboardInterrupt:
    print("Game closed by user.")
