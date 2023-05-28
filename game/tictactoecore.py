class SquareState:
    def __init__(self, symbol=None):
        self.symbol = symbol

    def is_none(self):
        return self.symbol is None


class TurnState:
    Continue = 0
    Draw = 1
    Error = 2
    Victory = 3


class TicTacToe:

    def __init__(self, x_size=3, y_size=3, seq_to_win=3, empty_symbol=' ', horizontal_spacer='─', vertical_spacer='│',
                 cross_spacer="┼"):
        self.x_size = x_size
        self.y_size = y_size
        self.squares = [SquareState(None) for _ in range(x_size * y_size)]
        self.seq_to_win = seq_to_win
        self.filled = 0
        self.empty_symbol = empty_symbol
        self.horizontal_spacer = horizontal_spacer
        self.cross_spacer = cross_spacer
        self.vertical_spacer = vertical_spacer

    def __str__(self):
        def add_col_margin(s, col_margin):
            s += " " * col_margin
            return s

        def add_line_margin(s, line_margin):
            s += " " * (line_margin - 1)
            return s

        s = ""
        lane = 1
        col_margin = len(str(self.y_size)) + 4
        if col_margin % 2 == 0:
            col_margin += 1
        line_margin = len(str(self.x_size))
        col = 1
        s = add_col_margin(s, col_margin // 2)
        for i in range(self.x_size * 3):
            if i % 3 == 0:
                s += f" {col}"
                col += 1
            else:
                s += " "
        s += f"\n{lane}-"
        s = add_line_margin(s, line_margin)
        for i in range(len(self.squares)):
            if self.squares[i].is_none():
                s += f" {self.empty_symbol} "
            else:
                s += f" {self.squares[i].symbol} "
            if (i > 0) and ((i + 1) % self.x_size == 0) and not (lane == self.y_size):
                s += "\n"
                s = add_col_margin(s, col_margin // 2)
                for i in range(self.x_size * 3 + self.x_size - 1):
                    if (i + 1) % 4 == 0:
                        s += self.cross_spacer
                    else:
                        s += self.horizontal_spacer
                lane += 1
                s += f"\n{lane}-"
                s = add_line_margin(s, line_margin)
                if len(str(lane + 1)) > len(str(lane)):
                    line_margin -= 1
            elif i < len(self.squares) - 1:
                s += self.vertical_spacer
        return s

    def get_square(self, x, y) -> SquareState:
        return self.squares[self.get_coord_index(x, y)]

    def get_coord_index(self, x, y) -> int:
        return x + self.x_size * y

    def get_index_coord(self, index) -> (int, int):
        return index % self.x_size, index / self.x_size

    def set_square(self, x, y):
        pass

    def set_square_from_index(self, index, square_state):

        pass

    def check_game_over(self, x, y, state) -> TurnState:
        pass

    def all_lines_checker(self, x, y, state, stop_counting, check_x_axis, check_y_axis, inverted=False):
        pass

    def check_for_victory(self, x, y, state, x_axis, y_axis, stop_counting=False,
                          return_available_spaces=False, inverted_axis=False):
        pass

    def check_x(self, x, y, state, stop_counting=False, return_available_spaces=False):
        pass

    def check_y(self, x, y, state, stop_counting=False, return_available_spaces=False):
        pass

    def check_left_diag(self, x, y, state, stop_counting=False, return_available_spaces=False):
        pass

    def check_right_diag(self, x, y, state, stop_counting=False, return_available_spaces=False):
        pass

    def check_draw(self):
        return self.filled == len(self.squares)

    def size(self):
        return self.x_size * self.y_size

    def get_square_by_index(self, index):
        return self.squares[index]

    def clear(self):
        self.squares = [SquareState() for _ in range(self.x_size * self.y_size)]
        self.filled = 0

    def sum_squares_in_winnable_distance(self, index, square_state, return_highest=False) -> int:
        pass

    def check_n_of_available_axis(self, index, square_state) -> int:
        pass

    def spaces_of_around(self, index, square_state) -> int:
        pass
