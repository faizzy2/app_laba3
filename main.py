from sudokuGenerator import Sudoku


if __name__ == "__main__":
    sudoku = Sudoku(9)
    sudoku.fill_grid(50)
    sudoku.print_grid()