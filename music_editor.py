import pygame
import pygame.midi

CELL_SIZE = 32
ROWS = 8
COLS = 16
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

# Initialize pygame and midi
pygame.init()
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)

# Grid representing notes
notes = [[False for _ in range(COLS)] for _ in range(ROWS)]

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pixel Music Editor")
clock = pygame.time.Clock()

NOTE_BASE = 60  # Middle C


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = (255, 255, 255) if notes[row][col] else (40, 40, 40)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)


def play_sequence():
    for col in range(COLS):
        for row in range(ROWS):
            if notes[row][col]:
                player.note_on(NOTE_BASE + row, 127)
        pygame.time.wait(150)
        for row in range(ROWS):
            if notes[row][col]:
                player.note_off(NOTE_BASE + row, 127)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            c = x // CELL_SIZE
            r = y // CELL_SIZE
            if 0 <= r < ROWS and 0 <= c < COLS:
                notes[r][c] = not notes[r][c]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play_sequence()

    screen.fill((20, 20, 20))
    draw_grid()
    pygame.display.flip()
    clock.tick(60)

player.close()
pygame.midi.quit()
pygame.quit()
