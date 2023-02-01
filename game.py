import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
grid_color = (128, 128, 128)

O = [[0, 0, 0, 0],
     [0, 1, 1, 0],
     [0, 1, 1, 0],
     [0, 0, 0, 0]]
T = [[0, 1, 0],
     [1, 1, 1],
     [0, 0, 0]]
S = [[0, 1, 1],
     [1, 1, 0],
     [0, 0, 0]]
Z = [[1, 1, 0],
     [0, 1, 1],
     [0, 0, 0]]
J = [[1, 0, 0],
     [1, 1, 1],
     [0, 0, 0]]
L = [[0, 0, 1],
     [1, 1, 1],
     [0, 0, 0]]
I = [[0, 0, 0, 0],
     [1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]

colors = {
    (255, 255, 0): 1,
    (200, 0, 200): 2,
    (0, 255, 0): 3,
    (255, 0, 0): 4,
    (0, 0, 255): 5,
    (255, 128, 0): 6,
    (0, 255, 255): 7,
}

color_mapping = {
    1: (255, 255, 0),
    2: (200, 0, 200),
    3: (0, 255, 0),
    4: (255, 0, 0),
    5: (0, 0, 255),
    6: (255, 128, 0),
    7: (0, 255, 255)
}

bag = [O, T, S, Z, J, L, I]
random.shuffle(bag)
index = 0

def next_piece():
    global index
    piece = bag[index]
    index += 1
    if index == 7:
        index = 0
        random.shuffle(bag)
    return piece

game_board = [[0 for _ in range(10)] for _ in range(20)]
block_size = 20
current_piece = next_piece()
current_color = colors[random.choice(list(colors.keys()))]
current_piece_x = 3
current_piece_y = -1
score = 0
current_rotation = 0
font = pygame.font.Font(None, 30)
text = font.render("Score: " + str(score), True, (255, 255, 255))

def check_collision(x, y):
    for i in range(len(current_piece)):
        for j in range(len(current_piece[0])):
            if current_piece[i][j] != 0:
                if (y+i >= 20) or (x+j < 0) or (x+j >= 10) or (game_board[y+i][x+j] != 0):  
                    return True
    return False

def lock_piece():
    global current_piece_x, current_piece_y, current_rotation
    for i in range(len(current_piece)):
        for j in range(len(current_piece[0])):
            if current_piece[i][j] != 0:
                game_board[current_piece_y + i][current_piece_x + j] = current_color
    current_rotation = 0

def new_piece():
    global current_piece, current_color, current_piece_x, current_piece_y, current_rotation
    current_piece_x = 3
    current_piece_y = -1
    current_piece = next_piece()
    current_color = colors[random.choice(list(colors.keys()))]
    for i in range(current_rotation):
        rotate(current_piece, 'left')
    if check_collision(current_piece_x, current_piece_y):
        game_over = True

def rotate(matrix, direction):
    global current_rotation
    N = len(matrix[0])
    if direction == 'right':
        current_rotation += 1
        for x in range(int(N/2)):
            for y in range(x, N-x-1):
                temp = matrix[x][y]
                matrix[x][y] = matrix[N-1-y][x]
                matrix[N-1-y][x] = matrix[N-1-x][N-1-y]
                matrix[N-1-x][N-1-y] = matrix[y][N-1-x]
                matrix[y][N-1-x] = temp
    elif direction == 'left':
        current_rotation -= 1
        for x in range(int(N/2)):
            for y in range(x, N-x-1):
                temp = matrix[N-1-y][x]
                matrix[N-1-y][x] = matrix[x][y]
                matrix[x][y] = matrix[y][N-1-x]
                matrix[y][N-1-x] = matrix[N-1-x][N-1-y]
                matrix[N-1-x][N-1-y] = temp

fall_interval = 1000
pygame.time.set_timer(pygame.USEREVENT + 1, fall_interval)
pygame.key.set_repeat(500, 100)

running = True
while running:

    prev_current_piece_x = current_piece_x
    prev_current_piece_y = current_piece_y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_piece_x -= 1
            if event.key == pygame.K_RIGHT:
                current_piece_x += 1
            if event.key == pygame.K_DOWN:
                current_piece_y += 1
                score += 1
            if event.key == pygame.K_UP:
                rotate(current_piece, 'right')
                if check_collision(current_piece_x, current_piece_y):
                    rotate(current_piece, 'left')
        if event.type == pygame.USEREVENT + 1:
            current_piece_y += 1


    if check_collision(current_piece_x, current_piece_y):
        current_piece_x = prev_current_piece_x
    if check_collision(current_piece_x, current_piece_y):
        current_piece_y = prev_current_piece_y
        lock_piece()
        new_piece()


    for row in range(-2, 20):
        complete = True
        for col in range(10):
            if game_board[row][col] == 0:
                complete = False
                break
        if complete:
            for r in range(row, 0, -1):
                game_board[r] = game_board[r-1]
            game_board[0] = [0] * 10


    screen.fill((0, 0, 0))

# Draw the game board
    for y in range(20):
         for x in range(10):
            if game_board[y][x] != 0:
                pygame.draw.rect(screen, color_mapping[game_board[y][x]], (x*block_size, y*block_size, block_size, block_size))

    for x in range(0, 10 * block_size, block_size):
        pygame.draw.line(screen, grid_color, (x, 0), (x, 20 * block_size))
    for y in range(0, 20 * block_size, block_size):
        pygame.draw.line(screen, grid_color, (0, y), (10 * block_size, y))
# Draw the current piece
    for y in range(len(current_piece)):
        for x in range(len(current_piece[y])):
            if current_piece[y][x] != 0:
                pygame.draw.rect(screen, color_mapping[current_color], ( (current_piece_x+x)*block_size, (current_piece_y+y)*block_size, block_size, block_size))



    screen.blit(text, (650, 550))
    pygame.display.flip()
    pygame.display.update()
    
    