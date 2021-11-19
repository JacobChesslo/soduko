class Base(object):
    def _store_rows_and_columns(self) -> tuple:
        """
        Stores the rows and columns of an n x n list of lists

        :return: tuple
            rows (list), column (list)
        """
        self.rows = self.grid
        self.columns = [[row[i] for row in self.grid] for i, _ in enumerate(self.grid)]

        return self.rows, self.columns


class Grid(Base):
    def __init__(self, board_grid: list) -> object:
        """
        Dunder init function that verifies that the passed argument
        is a valid Soduko game grid through:
            - It is a list of lists
            - It has 9 columns and 9 rows
            - It has only integers or NoneType inside of the list of lists
            - All integers are between 0 and 9

        Stores rows, columns, and subgrids of the soduko board grid

        Example Grid:
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]

        :param board_grid: list
            list (len 9) of lists (len 9 each) of ints or NoneType
        """
        # Stores checked grid
        self.grid = self.check(board_grid)

        # Stores rows and columns and subgrids
        self.rows, self.columns, self.subgrids = None, None, [None] * 9
        self.store()

    def check(self, grid) -> list:
        # Checks if passed argument is a list
        if not isinstance(grid, list):
            raise TypeError('Soduko game grid must be a list')

        # Checks if passed argument is a list of 9 elements
        if len(grid) != 9:
            raise ValueError('Soduko game grid must have 9 rows and 9 columns')

        # Checks if passed argument is a list of 9 lists
        if not all(isinstance(row, list) for row in grid):
            raise TypeError('Soduko game grid must be a list of lists')

        # Temporarily flattens game grid
        temp = [element for row in grid for element in row]

        # Checks if there is exactly 81 elements in the game grid
        if len(temp) != 81:
            raise ValueError('Soduko game grid must have 9 rows and 9 columns')

        # Checks if all elements are NoneType or int, checks further otherwise
        if not all(isinstance(element, int) or element is None for element in temp):

            # Checks if all elements are NoneType, int, or float, raises TypeError otherwise
            if not all(isinstance(element, (int, float)) or element is None for element in temp):
                raise TypeError('Soduko game grid must be filled with integers')

            # Checks if float elements are equal to ints, raises TypeError otherwise
            if not all(int(element) == element for element in temp if element is not None):
                raise TypeError('Soduko game grid must be filled with integers')

            # Converts types to int
            temp = [int(element) if isinstance(element, (int, float)) else None for element in temp]

        # Checks if non-NoneType elements are between 0 and 9 (inclusive)
        if not all((0 <= element <= 9) or element is None for element in temp if element is not None):
            raise ValueError('Sudoku game grid must be filled with integers between 0 and 9, or None')

        # Resets to 9-element list of 9-element lists of (int, None)
        grid = [temp[i: i + 9] for i in range(0, len(temp), 9)]

        return grid

    def store(self) -> list:
        self._store_rows_and_columns()
        self._store_subgrids()

        return self.grid

    def refresh(self, board_grid) -> list:
        self.grid = self.check(board_grid)
        self.store()

        return self.grid

    def _store_subgrids(self) -> list:
        x_lowers = y_lowers = [0, 3, 6]
        x_uppers = y_uppers = [3, 6, 9]

        for i, (xi, xf) in enumerate(zip(x_lowers, x_uppers)):
            for j, (yi, yf) in enumerate(zip(y_lowers, y_uppers)):
                subgrid = [grid[xi:xf] for grid in self.grid[yi:yf]]
                index = i + 3 * j
                if not hasattr(self.subgrids[index], 'subgrid'):
                    self.subgrids[index] = SubGrid(subgrid)
                elif hasattr(self.subgrids[index], 'refresh'):
                    self.subgrids[index].refresh(subgrid)
                else:
                    raise TypeError('Cannot determine if subgrid list contains an object or NoneType')

        return self.subgrids

    def print(self) -> bool:
        for i, row in enumerate(self.grid):
            if (not i % 3) and i:
                print('- - - - - - - - -')

            for j, column in enumerate(row):

                if not j % 3:
                    print(' | ', end='')

                if j == 8:
                    print(f'{self.grid[i][j]}', end='\n')
                else:
                    print(f'{self.grid[i][j]}', end='')

        return True


class SubGrid(Base):
    def __init__(self, board_subgrid: list) -> object:
        """
        Dunder init function that verifies that the passed argument
        is a valid Soduko game subgrid through:
            - It is a list of lists
            - It has 3 columns and 3 rows
            - It has only integers or NoneType inside of the list of lists
            - All integers are between 0 and 9

        :param board_subgrid:
        """

        self.grid = self.check(board_subgrid)
        self.rows, self.columns = None, None
        self.store()

    def check(self, subgrid: list) -> list:

        # Checks if passed argument is a list
        if not isinstance(subgrid, list):
            raise TypeError('Soduko game subgrid must be a list')

        # Checks if passed argument is a list of 3 elements
        if len(subgrid) != 3:
            raise ValueError('Soduko game subgrid must have 3 rows and 3 columns')

        # Checks if passed argument is a list of lists
        if not all(isinstance(row, list) for row in subgrid):
            raise TypeError('Soduko game subgrid must be a list of lists')

        # Temporarily flattens game subgrid
        temp = [element for row in subgrid for element in row]

        # Checks if there is exactly 9 elements in the game subgrid
        if len(temp) != 9:
            raise ValueError('Soduko game subgrid must have 9 rows and 9 columns')

        # Checks if all elements are NoneType or int, checks further otherwise
        if not all(isinstance(element, int) or element is None for element in temp):

            # Checks if all elements are NoneType, int, or float, raises TypeError otherwise
            if not all(isinstance(element, (int, float)) or element is None for element in temp):
                raise TypeError('Soduko game subgrid must be filled with integers')

            # Checks if float elements are equal to ints, raises TypeError otherwise
            if not all(int(element) == element for element in temp if element is not None):
                raise TypeError('Soduko game subgrid must be filled with integers')

            # Converts types to int
            temp = [int(element) if isinstance(element, (int, float)) else None for element in temp]

        # Checks if non-NoneType elements are between 0 and 9 (inclusive)
        if not all((0 <= element <= 9) or element is None for element in temp if element is not None):
            raise ValueError('Sudoku game subgrid must be filled with integers between 0 and 9, or None')

        # Resets to 3-element list of 3-element lists of (int, None)
        subgrid = [temp[i: i + 3] for i in range(0, len(temp), 3)]

        return subgrid

    def store(self) -> list:
        self._store_rows_and_columns()

        return self.grid

    def refresh(self, board_subgrid: list) -> list:
        self.grid = self.check(board_subgrid)
        self.store()

        return self.grid
