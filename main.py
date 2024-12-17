from sudokuGenerator import Sudoku, Cell
import pygame
from pygame import K_BACKSPACE
from tkinter import messagebox
import sys


WIDTH = 800
HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
SELECTED_COLOR = (150, 150, 255)
INPUT_COLOR_CORRECT = GREY
INPUT_COLOR_INCORRECT = (255, 0, 0)
GRID_SIZE = 9
SUB_GRID_SIZE = int(GRID_SIZE ** 0.5)
CELL_SIZE = WIDTH // GRID_SIZE
FILLED_CELLS = 31

sudoku = Sudoku(GRID_SIZE)
sudoku.fill_grid(FILLED_CELLS)

def draw_grid(screen):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

def draw_numbers(screen):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if sudoku.grid[row][col].is_original:
                color = BLACK
            else:
                if sudoku.grid[row][col].number == sudoku.filled_grid[row][col]:
                    color = INPUT_COLOR_CORRECT
                else:
                    color = INPUT_COLOR_INCORRECT

            if sudoku.grid[row][col].number != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(sudoku.grid[row][col].number), True, color)
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

def draw_help_glow(screen, row, col):
    # Подсветка строки
    for c in range(GRID_SIZE):
        rect = pygame.Rect(c * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, SELECTED_COLOR, rect)
    # Подсветка столбца
    for r in range(GRID_SIZE):
        rect = pygame.Rect(col * CELL_SIZE, r * CELL_SIZE, CELL_SIZE,CELL_SIZE)
        pygame.draw.rect(screen, SELECTED_COLOR, rect)
    # Подсветка подсетки
    box_row_start = row - row % SUB_GRID_SIZE
    box_col_start = col - col % SUB_GRID_SIZE
    for r in range(box_row_start, box_row_start + SUB_GRID_SIZE):
        for c in range(box_col_start, box_col_start + SUB_GRID_SIZE):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, SELECTED_COLOR, rect)

def check_win():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if sudoku.grid[row][col].number != sudoku.filled_grid[row][col]:
                return False
    return True


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Sudoku")

    selected_cell = None

    while True:
        if check_win():
            replay = messagebox.askyesno("You won!", "Do you wish to play again?")
            if replay is False:
                pygame.quit()
            else:
                sudoku.clear()
                sudoku.fill_grid(FILLED_CELLS)

        screen.fill(WHITE)
        if selected_cell:
            draw_help_glow(screen, selected_cell[0], selected_cell[1])
        draw_grid(screen)
        draw_numbers(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                selected_cell = (y // CELL_SIZE, x // CELL_SIZE)

            if event.type == pygame.KEYDOWN and selected_cell:
                row, col = selected_cell
                if sudoku.grid[row][col].is_original:
                    continue
                if event.unicode.isdigit():
                    cur_num = str(sudoku.grid[row][col].number)
                    if len(cur_num) > GRID_SIZE//10 + 1:
                        continue
                    sudoku.grid[row][col].number = int(cur_num + event.unicode)
                elif event.key == K_BACKSPACE:
                    sudoku.grid[row][col].number = 0

        pygame.display.flip()


if __name__ == "__main__":
    main()