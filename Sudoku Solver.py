import tkinter as tk
from tkinter import messagebox


class Board:
    def __init__(self, board):
        self.board = board

    def find_empty_cell(self):
        for row, contents in enumerate(self.board):
            try:
                col = contents.index(0)
                return row, col
            except ValueError:
                pass
        return None

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return all(
            self.board[row][col] != num
            for row in range(9)
        )

    def valid_in_square(self, row, col, num):
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        for row_no in range(row_start, row_start + 3):
            for col_no in range(col_start, col_start + 3):
                if self.board[row_no][col_no] == num:
                    return False
        return True

    def is_valid(self, empty, num):
        row, col = empty
        valid_in_row = self.valid_in_row(row, num)
        valid_in_col = self.valid_in_col(col, num)
        valid_in_square = self.valid_in_square(row, col, num)
        return all([valid_in_row, valid_in_col, valid_in_square])

    def solver(self):
        if (next_empty := self.find_empty_cell()) is None:
            return True
        else:
            for guess in range(1, 10):
                if self.is_valid(next_empty, guess):
                    row, col = next_empty
                    self.board[row][col] = guess
                    if self.solver():
                        return True
                    self.board[row][col] = 0

        return False


class SudokuGUI:
    def __init__(self, root, puzzle):
        self.root = root
        self.root.title("Sudoku Solver")
        self.board = Board(puzzle)
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=450, height=450)
        self.canvas.pack()
        self.draw_grid()
        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        self.solve_button.pack()

    def draw_grid(self):
        for i in range(10):
            color = "black" if i % 3 == 0 else "gray"
            self.canvas.create_line(50 * i, 0, 50 * i, 450, fill=color)
            self.canvas.create_line(0, 50 * i, 450, 50 * i, fill=color)

        for row in range(9):
            for col in range(9):
                value = self.board.board[row][col]
                if value != 0:
                    x = col * 50 + 25
                    y = row * 50 + 25
                    self.canvas.create_text(x, y, text=value, font=("Helvetica", 20))

    def solve(self):
        if self.board.solver():
            self.canvas.delete("all")
            self.draw_grid()
            messagebox.showinfo("Sudoku Solver", "Puzzle solved successfully!")
        else:
            messagebox.showerror("Sudoku Solver", "The provided puzzle is unsolvable.")


if __name__ == "__main__":
    root = tk.Tk()
    puzzle = [
        [0, 0, 2, 0, 0, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 7, 6, 2],
        [4, 3, 0, 0, 0, 0, 8, 0, 0],
        [0, 5, 0, 0, 3, 0, 0, 9, 0],
        [0, 4, 0, 0, 0, 0, 0, 2, 6],
        [0, 0, 0, 4, 6, 7, 0, 0, 0],
        [0, 8, 6, 7, 0, 4, 0, 0, 0],
        [0, 0, 0, 5, 1, 9, 0, 0, 8],
        [1, 7, 0, 0, 0, 6, 0, 0, 5]
    ]
    gui = SudokuGUI(root, puzzle)
    root.mainloop()
