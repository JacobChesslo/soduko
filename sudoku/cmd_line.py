from sudoku.grid import Grid


class CommandLineSolver(Grid):
    def __init__(self, board_grid: list) -> object:
        super().__init__(board_grid)

    def solve(self):
        temp = self._search_for_empty_cell()
        if temp is None:
            return True

        empty_row, empty_column = temp

        for number in range(1, 10):
            if self._is_valid(empty_row, empty_column, number):
                self.grid[empty_row][empty_column] = number

                if self.solve():
                    return True

                self.grid[empty_row][empty_column] = 0

        return False

    def _search_for_empty_cell(self):
        for i, row in enumerate(self.grid):
            for j, column in enumerate(row):
                if self.grid[i][j] == 0:
                    return i, j

        return None

    def _is_valid(self, empty_row, empty_column, number):

        for j, _ in enumerate(self.grid):
            if self.grid[empty_row][j] == number and empty_column != j:
                return False

        for i, row in enumerate(self.grid):
            if self.grid[i][empty_column] == number and empty_row != i:
                return False

        subgrid = [empty_column // 3, empty_row // 3]

        for i in range(subgrid[1] * 3, subgrid[1] * 3 + 3):
            for j in range(subgrid[0] * 3, subgrid[0] * 3 + 3):
                if self.grid[i][j] == number and ((i, j) != (empty_row, empty_column)):
                    return False

        return True

    def show(self):
        for i, row in enumerate(self.grid):
            if (not i % 3) and i:
                print(' - - - - - - - - - ')

            for j, column in enumerate(row):

                if not j % 3:
                    print(' | ', end='')

                if j == 8:
                    print(f'{self.grid[i][j]}', end='\n')
                else:
                    print(f'{self.grid[i][j]}', end='')

        return True


def simple_solver(board_grid: list, show: bool = False) -> object:
    puzzle = CommandLineSolver(board_grid)
    puzzle.solve()
    if show:
        puzzle.show()

    return puzzle
