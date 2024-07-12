from tkinter import *
import random

GAME_WIDTH = 800
GAME_HEIGHT = 600
SPEED = 90
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = '#00FF00'
SNAKE_HEAD = '#CF9FFF'
FOOD_COLOR = '#FF0000'
BACKGROUND_COLOR = '#000000'

ORIGINAL_SPEED = SPEED
ORIGINAL_SNAKE_COLOR = SNAKE_COLOR
ORIGINAL_SNAKE_HEAD = SNAKE_HEAD
ORIGINAL_FOOD_COLOR = FOOD_COLOR

slowed_active = False
slowed_timer = 3  # in seconds
cooldown_timer = 5  # in seconds

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for i, (x, y) in enumerate(self.coordinates):
            color = SNAKE_HEAD if i == 0 else SNAKE_COLOR
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=color, tags="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        self.place_new_food()

    def place_new_food(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        self.food_item = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    # Change the color of the new head to SNAKE_HEAD color
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_HEAD, tags="snake")
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        canvas.delete("score_text")
        canvas.create_text(10, 10, anchor="nw", text="Score: {}".format(score), fill="white", font=("Arial", 16),
                           tags="score_text")
        canvas.delete("food")
        food.place_new_food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Change the color of the previous head back to SNAKE_COLOR
    canvas.itemconfig(snake.squares[1], fill=SNAKE_COLOR)

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]
    global GAME_WIDTH, GAME_HEIGHT, SPACE_SIZE
    # Wrap horizontally
    if x < 0:
        x = GAME_WIDTH - SPACE_SIZE  # Wrap around to the right side
    elif x >= GAME_WIDTH:
        x = 0  # Wrap around to the left side

    # Wrap vertically
    if y < 0:
        y = GAME_HEIGHT - SPACE_SIZE  # Wrap around to the bottom
    elif y >= GAME_HEIGHT:
        y = 0  # Wrap around to the top

    # Update the coordinates in the snake object
    snake.coordinates[0] = (x, y)

    # Check for collisions with the snake's body
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def slowed():
    global SNAKE_COLOR, SNAKE_HEAD, FOOD_COLOR, SPEED, slowed_active, slowed_timer
    if not slowed_active:
        slowed_active = True
        SPEED = SPEED * 2
        SNAKE_COLOR = '#FF00FF'
        SNAKE_HEAD = '#306000'
        FOOD_COLOR = '#00FFFF'

        # Update snake colors
        for i, square in enumerate(snake.squares):
            color = SNAKE_HEAD if i == 0 else SNAKE_COLOR
            canvas.itemconfig(square, fill=color)

        # Update food color
        canvas.itemconfig(food.food_item, fill=FOOD_COLOR)

        # Display the timer on the canvas
        update_timer(slowed_timer, "Slowed")

        # Schedule the color reset after the slowed_timer duration
        window.after(slowed_timer * 1000, start_cooldown)


def update_timer(time_left, mode):
    if time_left > 0:
        canvas.delete("timer_text")
        canvas.create_text(GAME_WIDTH - 50, 10, anchor="ne", text="{}: {}".format(mode, time_left), fill="white",
                           font=("Arial", 16), tags="timer_text")
        window.after(1000, update_timer, time_left - 1, mode)


def start_cooldown():
    global slowed_active, cooldown_timer
    slowed_active = True  # Keep the flag true during cooldown
    reset_colors()  # Reset colors and speed
    update_timer(cooldown_timer, "Cooldown")
    window.after(cooldown_timer * 1000, end_cooldown)


def end_cooldown():
    global slowed_active
    slowed_active = False
    canvas.delete("timer_text")


def reset_colors():
    global SNAKE_COLOR, SNAKE_HEAD, FOOD_COLOR, SPEED
    SPEED = ORIGINAL_SPEED
    SNAKE_COLOR = ORIGINAL_SNAKE_COLOR
    SNAKE_HEAD = ORIGINAL_SNAKE_HEAD
    FOOD_COLOR = ORIGINAL_FOOD_COLOR

    # Update snake colors
    for i, square in enumerate(snake.squares):
        color = SNAKE_HEAD if i == 0 else SNAKE_COLOR
        canvas.itemconfig(square, fill=color)

    # Update food color
    canvas.itemconfig(food.food_item, fill=FOOD_COLOR)


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 3, font=('Arial', 70),
                       text="Game Over", fill='white', tags="Game Over")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('Arial', 30),
                       text="Press space bar to try again", fill='white', tags="try again")

    canvas.create_text(100, 50, font=('Arial', 16),
                       text=f'Score = {score}', fill='white', tags="your_score")

    window.bind('<space>', reset_game)


def reset_game(event):
    global snake, food, score, direction

    window.bind('<space>', 'NULL')

    canvas.delete(ALL)
    score = 0
    direction = 'down'

    snake = Snake()
    food = Food()

    next_turn(snake, food)


window = Tk()
window.title("Snake Game!")
window.resizable(False, False)

score = 0
direction = 'down'

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<j>', lambda event: slowed())
for key in ('<Left>', 'a', 'A'): window.bind(key, lambda event: change_direction('left'))
for key in ('<Right>', 'd', 'D'): window.bind(key, lambda event: change_direction('right'))
for key in ('<Up>', 'w', 'W'): window.bind(key, lambda event: change_direction('up'))
for key in ('<Down>', 's', 'S'): window.bind(key, lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
