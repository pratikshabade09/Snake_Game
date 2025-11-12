import turtle as t
import random
import time

# Game window setup
w = 500
h = 500
food_size = 10
delay = 100
offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}

# Colors and visuals
BG_COLOR = "#1a1a2e"
SNAKE_HEAD_COLOR = "#00ff41"
SNAKE_BODY_COLOR = "#0ad664"
FOOD_COLOR = "#ff6b6b"
BORDER_COLOR = "#00ff41"
TEXT_COLOR = "#ffffff"

SCORE = 0
HIGH_SCORE = 0
game_running = False

# ---------------- Functions ---------------- #

def create_border():
    """Draw game border"""
    border = t.Turtle()
    border.hideturtle()
    border.penup()
    border.color(BORDER_COLOR)
    border.pensize(3)
    border.goto(-w//2, -h//2)
    border.pendown()
    for _ in range(4):
        border.forward(w)
        border.left(90)
    border.penup()

def update_score_display():
    """Update score on screen"""
    score_display.clear()
    score_display.goto(-w//2 + 20, h//2 + 20)
    score_display.write(f"Score: {SCORE}", align="left", font=("Courier", 18, "bold"))
    score_display.goto(w//2 - 20, h//2 + 20)
    score_display.write(f"High Score: {HIGH_SCORE}", align="right", font=("Courier", 16, "normal"))

def get_random_food_position():
    """Return a random food position"""
    x = random.randint(-w//2 + 20, w//2 - 20)
    y = random.randint(-h//2 + 20, h//2 - 20)
    return (x, y)

def reset():
    """Reset the game"""
    global snake, snake_dir, food_position, SCORE, HIGH_SCORE, game_running

    if SCORE > HIGH_SCORE:
        HIGH_SCORE = SCORE

    SCORE = 0
    game_running = True
    snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
    snake_dir = "up"
    food_position = get_random_food_position()
    food.goto(food_position)
    snake_turtle.clearstamps()
    update_score_display()
    move_snake()

def move_snake():
    """Main snake movement"""
    global snake_dir, SCORE, game_running

    if not game_running:
        return

    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_dir][0]
    new_head[1] += offsets[snake_dir][1]

    # Collision with itself
    if new_head in snake[:-1]:
        print("Final Score:", SCORE)
        time.sleep(1)
        show_game_over()
        return

    snake.append(new_head)

    if not food_collision():
        snake.pop(0)

    # Wrapping (boundary crossing)
    if snake[-1][0] > w/2: snake[-1][0] -= w
    elif snake[-1][0] < -w/2: snake[-1][0] += w
    elif snake[-1][1] > h/2: snake[-1][1] -= h
    elif snake[-1][1] < -h/2: snake[-1][1] += h

    snake_turtle.clearstamps()
    for i, segment in enumerate(snake):
        snake_turtle.goto(segment[0], segment[1])
        if i == len(snake) - 1:
            snake_turtle.color(SNAKE_HEAD_COLOR)
        else:
            snake_turtle.color(SNAKE_BODY_COLOR)
        snake_turtle.stamp()

    screen.update()
    t.ontimer(move_snake, delay)

def food_collision():
    """Check food collision"""
    global food_position, SCORE
    if get_distance(snake[-1], food_position) < 20:
        SCORE += 10
        food_position = get_random_food_position()
        food.goto(food_position)
        update_score_display()
        return True
    return False

def get_distance(pos1, pos2):
    """Calculate distance"""
    x1, y1 = pos1
    x2, y2 = pos2
    return ((y2 - y1)**2 + (x2 - x1)**2)**0.5

def show_game_over():
    """Display Game Over"""
    global game_running
    game_running = False
    game_over = t.Turtle()
    game_over.hideturtle()
    game_over.penup()
    game_over.color(FOOD_COLOR)
    game_over.goto(0, 50)
    game_over.write("GAME OVER!", align="center", font=("Courier", 36, "bold"))
    game_over.goto(0, 0)
    game_over.color(TEXT_COLOR)
    game_over.write(f"Final Score: {SCORE}", align="center", font=("Courier", 20, "normal"))
    game_over.goto(0, -40)
    game_over.write("Press SPACE to restart", align="center", font=("Courier", 14, "italic"))
    screen.update()

def restart_game():
    """Restart game"""
    screen.clear()
    setup_screen()
    reset()

def show_instructions():
    """Show control guide"""
    instructions = t.Turtle()
    instructions.hideturtle()
    instructions.penup()
    instructions.color(TEXT_COLOR)
    instructions.goto(0, -h//2 - 30)
    instructions.write("Arrow Keys: Move | SPACE: Restart",
                      align="center", font=("Courier", 12, "normal"))

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

def setup_screen():
    """Setup game window and controls"""
    global screen, snake_turtle, food, score_display

    screen = t.Screen()
    screen.setup(w + 100, h + 100)
    screen.title("Snake Game")
    screen.bgcolor(BG_COLOR)
    screen.tracer(0)

    create_border()
    show_instructions()

    snake_turtle = t.Turtle("square")
    snake_turtle.penup()

    food = t.Turtle("circle")
    food.color(FOOD_COLOR)
    food.shapesize(food_size / 20)
    food.penup()

    score_display = t.Turtle()
    score_display.hideturtle()
    score_display.penup()
    score_display.color(TEXT_COLOR)

    screen.listen()
    screen.onkey(go_up, "Up")
    screen.onkey(go_right, "Right")
    screen.onkey(go_down, "Down")
    screen.onkey(go_left, "Left")
    screen.onkey(restart_game, "space")

# ---------------- Start Game ---------------- #
setup_screen()
reset()

try:
    t.done()
except KeyboardInterrupt:
    print("Game closed by user.")
