from pygame import K_BACKSPACE

from sudokuGenerator import Sudoku
import pygame
import sys

# Размеры окна и сетки
WIDTH, HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
EMPTY_CELLS = 50

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
SELECTED_COLOR = (150, 150, 255)  # Цвет для подсвеченной ячейки
INPUT_COLOR_CORRECT = GREY  # Цвет для правильно введенного числа
INPUT_COLOR_INCORRECT = (255, 0, 0)  # Цвет для неправильно введенного числа

sudoku = Sudoku(GRID_SIZE)
sudoku.fill_grid(EMPTY_CELLS)


def draw_grid(screen, selected_cell=None):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            # Подсвечиваем выбранную ячейку
            if selected_cell == (i, j):
                pygame.draw.rect(screen, SELECTED_COLOR, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)

            pygame.draw.rect(screen, BLACK, rect, 1)

            # Отображение чисел
            if sudoku.grid[i][j].is_original:
                color = BLACK
            else:
                if sudoku.grid[i][j].number == sudoku.filled_grid[i][j]:
                    color = INPUT_COLOR_CORRECT
                else:
                    color = INPUT_COLOR_INCORRECT

            if sudoku.grid[i][j].number != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(sudoku.grid[i][j].number), True, color)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")

    selected_cell = None

    while True:
        screen.fill(GREY)
        draw_grid(screen, selected_cell)

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
                    if len(cur_num) > 3:
                        continue
                    sudoku.grid[row][col].number = int(cur_num + event.unicode)
                elif event.key == K_BACKSPACE:
                    sudoku.grid[row][col].number = 0

        pygame.display.flip()


if __name__ == "__main__":
    main()