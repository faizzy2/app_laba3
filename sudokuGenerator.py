import random
from random import shuffle


class Cell:
    def __init__(self, number, is_original: bool):
        self.number = number
        self.is_original = is_original


class Sudoku:
    def __init__(self, size=9):
        self.size = size
        self.subgrid_size = int(size ** 0.5)
        self.grid = [[Cell(0, True) for i in range(size)] for _ in range(size)]
        self.filled_grid = [[0 for i in range(size)] for _ in range(size)]

    def fill_grid(self, filled_count):
        self._fill_values()
        for row in range(self.size):
            for column in range(self.size):
                self.filled_grid[row][column] = self.grid[row][column].number
        remove_count = self.size ** 2 - filled_count
        self.remove_numbers(remove_count)

    def _fill_values(self, row=0, col=0):
        if row == self.size - 1 and col == self.size:
            return True
        if col == self.size:
            row += 1
            col = 0

        if self.grid[row][col].number != 0:
            return self._fill_values(row, col + 1)

        num_list = list(range(1, self.size + 1))
        random.shuffle(num_list)

        for num in num_list:
            if self.is_safe(row, col, num):
                self.grid[row][col].number = num
                self.grid[row][col].is_original = True
                print(f"{row * 9 + col} filled")
                if self._fill_values(row, col + 1):
                    return True
                self.grid[row][col].number = 0  # backtrack

        return False

    def is_safe(self, row, col, num):
        # Проверить строку
        for c in range(self.size):
            if self.grid[row][c].number == num:
                return False
        # Проверить колонку
        for r in range(self.size):
            if self.grid[r][col].number == num:
                return False
        # Проверить подматрицу
        box_row_start = row - row % self.subgrid_size
        box_col_start = col - col % self.subgrid_size
        for r in range(box_row_start, box_row_start + self.subgrid_size):
            for c in range(box_col_start, box_col_start + self.subgrid_size):
                if self.grid[r][c].number == num:
                    return False

        return True

    def remove_numbers(self, num_to_remove=40):
        filled = [i for i in range(self.size ** 2)]
        shuffle(filled)
        while num_to_remove > 0:
            if len(filled) == 0:
                break
            index = filled.pop(0)
            backup = self.grid[index // self.size][
                index % self.size].number  # сохраняем число для восстановления
            self.grid[index // self.size][
                index % self.size].number = 0  # удаляем число
            self.grid[index // self.size][
                index % self.size].is_original = False
            # Проверяем, есть ли еще одно уникальное решение
            if not self.has_unique_solution():
                self.grid[index // self.size][
                    index % self.size].number = backup  # восстанавливаем число
                self.grid[index // self.size][
                    index % self.size].is_original = True
            else:
                num_to_remove -= 1
                print(f"{num_to_remove} remained to remove")

    def has_unique_solution(self):
        count = [0]  # используем список для изменения в замыкании

        def solve_sudoku(row=0, col=0):
            if row == self.size - 1 and col == self.size:
                count[0] += 1
                return
            if col == self.size:
                row += 1
                col = 0

            if self.grid[row][col].number != 0:
                solve_sudoku(row, col + 1)
                return

            for num in range(1, self.size + 1):
                if self.is_safe(row, col, num):
                    self.grid[row][col].number = num
                    solve_sudoku(row, col + 1)
                    self.grid[row][col].number = 0  # backtrack

        # Запускаем поиск решений
        solve_sudoku()
        return count[0] == 1  # должны быть только одно решение

    def clear(self):
        for row in range(self.size):
            for col in range(self.size):
                self.grid[row][col].number = 0

    def print_grid(self):
        for row in range(self.size):
            for column in range(self.size):
                if self.grid[row][column].number != 0:
                    print(self.grid[row][column].number, end=" ")
                else:
                    print(".", end=" ")
            print()
        print("---------------------------------------")
        for row in range(self.size):
            for column in range(self.size):
                if self.filled_grid[row][column] != 0:
                    print(self.filled_grid[row][column], end=" ")
                else:
                    print(".", end=" ")
            print()
