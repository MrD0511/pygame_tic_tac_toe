import pygame
from button import Button
import sys

pygame.init()

SCREEN_SIZE = 300
GRID_SIZE = 3
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
X_PLAYER = 'X'
O_PLAYER = 'O'
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 150, 200)
BUTTON_CLICK_COLOR = (40, 100, 160)
QUIT_BUTTON_COLOR = (211, 211, 211)  # Light Gray (Normal)
QUIT_BUTTON_HOVER_COLOR = (169, 169, 169)  # Darker Gray (Hover)
QUIT_BUTTON_CLICK_COLOR = (105, 105, 105)  # Even Darker Gray (Click)
font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 18)
board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = X_PLAYER
last_winner = "NO Winner"
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
screen2 = pygame.Surface((200, 100))

restart_button = Button(
    text="Restart",
    pos=(140, 50),  # Position within screen2
    size=(50, 30),
    colors={
        'normal': BUTTON_COLOR,
        'hover': BUTTON_HOVER_COLOR,
        'click': BUTTON_CLICK_COLOR
    },
    font=button_font
)

quit_button = Button(
    text = "Quit",
    pos=(10,50),
    size= ( 50, 30),
    colors={
        'normal': QUIT_BUTTON_COLOR,
        'hover': QUIT_BUTTON_HOVER_COLOR,
        'click': QUIT_BUTTON_CLICK_COLOR
    },
    font= button_font
)

pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 24)
sub_display = False

def draw_board():
    screen.fill(BG_COLOR)
    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE * row), (SCREEN_SIZE, CELL_SIZE * row), 2)
        pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE * row, 0), (CELL_SIZE * row, SCREEN_SIZE), 2)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == X_PLAYER:
                pygame.draw.line(screen, LINE_COLOR, (col * CELL_SIZE, row * CELL_SIZE),
                                 ((col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE), 3)
                pygame.draw.line(screen, LINE_COLOR, ((col + 1) * CELL_SIZE, row * CELL_SIZE),
                                 (col * CELL_SIZE, (row + 1) * CELL_SIZE), 3)
            if board[row][col] == O_PLAYER:
                pygame.draw.circle(screen, LINE_COLOR,
                                   (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - 10, 2)  
        if sub_display:
            draw_sub_display(last_winner)

def draw_sub_display(msg: str):
    screen2_pos = ((SCREEN_SIZE - screen2.get_width()) // 2, (SCREEN_SIZE - screen2.get_height()) // 2)
    screen2.fill(BG_COLOR)
    pygame.draw.rect(screen2, 'black', screen2.get_rect(), 3)
    text_surface = font.render(msg, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(screen2.get_width() // 2, screen2.get_height() // 4))
    screen2.blit(text_surface, text_rect)
    restart_button.draw(screen2)
    quit_button.draw(screen2)
    screen.blit(screen2, screen2_pos)

def get_cell(x, y):
    return x // CELL_SIZE, y // CELL_SIZE

def check_winner():
    for i in range(GRID_SIZE):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    
    if all(board[row][col] is not None for row in range(GRID_SIZE) for col in range(GRID_SIZE)):
        return 'DRAW'

    return None

while running:
    draw_board()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if sub_display:
            screen2_pos = ((SCREEN_SIZE - screen2.get_width()) // 2, (SCREEN_SIZE - screen2.get_height()) // 2)
            translated_event = event

            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                translated_event = pygame.event.Event(
                    event.type,
                    { "pos" : (event.pos[0] - screen2_pos[0], event.pos[1] - screen2_pos[1]) }
                )

            if restart_button.handle_event(translated_event):
                print("Restart Clicked")                                    #Restart The game
                won = False
                board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

            if quit_button.handle_event(translated_event):                  #Quit Game
                print("quit Clicked")
                pygame.quit()
                sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row, col = get_cell(y, x)  

            if board[row][col] is None:                               #Game Logic
                board[row][col] = current_player
                current_player = O_PLAYER if current_player == X_PLAYER else X_PLAYER
                
                winner = check_winner() 
                if winner == 'DRAW':
                    last_winner = "It's a Draw!"
                    sub_display = True
                elif winner != None:
                    sub_display = True
                    last_winner = f"Player {winner} wins!"
    pygame.display.flip()
    
    dt = clock.tick(25) / 1000

pygame.quit()
