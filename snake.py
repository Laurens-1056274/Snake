from tkinter import *
import random

GAME_WIDTH = 1440
GAME_HEIGHT = 600
SPEED = 90
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = '#00FF00'
SNAKE_HEAD = '#CF9FFF'
FOOD_COLOR = '#FF0000'
BACKGROUND_COLOR = '#000000'


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
        self.food_item = canvas.create_rectangle(x, y, x + SPACE_SIZE - 10, y + SPACE_SIZE - 10, fill=FOOD_COLOR, tags="food")

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
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_HEAD)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
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

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/3, font=('Arial', 70),
                       text="Game Over", fill='red', tags="Game Over")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('Arial', 30),
                       text="Press space bar to try again", fill='blue', tags="try again")

    window.bind('<space>', reset_game)

def reset_game(event):
    global snake, food, score, direction

    window.bind('<space>', 'NULL')

    canvas.delete(ALL)
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))

    snake = Snake()
    food = Food()

    next_turn(snake, food)

window = Tk()
window.title("Snake Game!")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text='Score:{}'.format(score), font=('Arial', 40))
label.pack()

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

for key in ('<Left>', 'a', 'A'): window.bind(key, lambda event: change_direction('left'))
for key in ('<Right>', 'd', 'D'): window.bind(key, lambda event: change_direction('right'))
for key in ('<Up>', 'w', 'W'): window.bind(key, lambda event: change_direction('up'))
for key in ('<Down>', 's', 'S'): window.bind(key, lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
