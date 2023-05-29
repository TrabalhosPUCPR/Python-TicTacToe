class SquareState:
    def __init__(self, symbol=None):
        self.symbol = symbol

    def is_none(self):
        return self.symbol is None

    def __eq__(self, other):
        return self.symbol == other.symbol


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

        s = "\n"
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

    def get_square(self, x: int, y: int) -> SquareState:
        return self.squares[self.get_coord_index(x, y)]

    def get_coord_index(self, x, y) -> int:
        return int(x + self.x_size * y)

    def get_index_coord(self, index) -> (int, int):
        return index % self.x_size, int(index / self.x_size)

    def set_square(self, x: int, y: int, state: SquareState):
        i = self.get_coord_index(x, y)
        if not self.squares[i].is_none():
            return TurnState.Error
        self.squares[i] = state
        self.filled += 1
        return self.check_game_over(x, y, state)

    def set_square_from_index(self, index: int, square_state: SquareState):
        if not self.squares[index].is_none():
            return TurnState.Error
        self.squares[index] = square_state
        self.filled += 1
        coord = self.get_index_coord(index)
        return self.check_game_over(coord[0], coord[1], square_state)

    def check_game_over(self, x: int, y: int, state: SquareState):
        if self.filled >= self.seq_to_win + 2 and \
                ((self.check_x(x, y, state, True, False) >= self.seq_to_win) or
                 (self.check_y(x, y, state, True, False) == self.seq_to_win) or
                 (self.check_left_diag(x, y, state, True, False) == self.seq_to_win) or
                 (self.check_right_diag(x, y, state, True, False) == self.seq_to_win)):
            return TurnState.Victory
        if self.check_draw():
            return TurnState.Draw
        return TurnState.Continue

    def check_x(self, x: int, y: int, state: SquareState, stop_counting: bool, return_available_spaces: bool) -> int:
        available_spaces_count = 1
        seq_count = 1
        for i in [1, -1]:
            dist = i
            while 0 <= x + dist < self.x_size and dist * i  < self.seq_to_win:
                square_state = self.get_square(x + dist, y)
                if not square_state.is_none():
                    if square_state == state:
                        seq_count += 1
                    else:
                        break
                elif stop_counting:
                    break
                dist += i
                available_spaces_count += 1
        if return_available_spaces:
            return available_spaces_count
        elif not stop_counting or seq_count >= self.seq_to_win:
            return seq_count
        else:
            return 1

    def check_y(self, x: int, y: int, state: SquareState, stop_counting: bool, return_available_spaces: bool) -> int:
        available_spaces_count = 1
        seq_count = 1
        for i in [1, -1]:
            dist = i
            while 0 <= y + dist < self.y_size and dist * i  < self.seq_to_win:
                square_state = self.get_square(x, y + dist)
                if not square_state.is_none():
                    if square_state == state:
                        seq_count += 1
                    else:
                        break
                elif stop_counting:
                    break
                dist += i
                available_spaces_count += 1
        if return_available_spaces:
            return available_spaces_count
        elif not stop_counting or seq_count >= self.seq_to_win:
            return seq_count
        else:
            return 1

    def check_left_diag(self, x: int, y: int, state: SquareState, stop_counting: bool, return_available_spaces: bool) -> int:
        available_spaces_count = 1
        seq_count = 1
        for i in [1, -1]:
            dist = i
            while 0 <= y + dist < self.y_size and 0 <= x + dist < self.x_size and dist * i < self.seq_to_win:
                square_state = self.get_square(x + dist, y + dist)
                if not square_state.is_none():
                    if square_state == state:
                        seq_count += 1
                    else:
                        break
                elif stop_counting:
                    break
                dist += i
                available_spaces_count += 1
        if return_available_spaces:
            return available_spaces_count
        elif not stop_counting or seq_count >= self.seq_to_win:
            return seq_count
        else:
            return 1

    def check_right_diag(self, x: int, y: int, state: SquareState, stop_counting: bool, return_available_spaces: bool) -> int:
        available_spaces_count = 1
        seq_count = 1
        for i in [1, -1]:
            dist = i
            while 0 <= y + (dist*-1) < self.y_size and 0 <= x + dist < self.x_size and dist * i < self.seq_to_win:
                square_state = self.get_square(x + dist, y + dist*-1)
                if not square_state.is_none():
                    if square_state == state:
                        seq_count += 1
                    else:
                        break
                elif stop_counting:
                    break
                dist += i
                available_spaces_count += 1
        if return_available_spaces:
            return available_spaces_count
        elif not stop_counting or seq_count >= self.seq_to_win:
            return seq_count
        else:
            return 1

    def check_draw(self):
        return self.filled == len(self.squares)

    def size(self):
        return self.x_size * self.y_size

    def get_square_by_index(self, index):
        return self.squares[index]

    def clear(self):
        self.squares = [SquareState() for _ in range(self.x_size * self.y_size)]
        self.filled = 0

    def sum_squares_in_winnable_distance(self, index: int, square_state: SquareState, return_highest=False) -> int:
        x, y = self.get_index_coord(index)
        if return_highest:
            count = [0, 0, 0, 0]
            count[0] = self.check_x(x, y, square_state, False, False) - 1
            count[1] = self.check_y(x, y, square_state, False, False) - 1
            count[2] = self.check_left_diag(x, y, square_state, False, False) - 1
            count[3] = self.check_right_diag(x, y, square_state, False, False) - 1
            highest = count[0]
            for i in range(1, len(count)):
                if count[i] > highest:
                    highest = count[i]
            return int(highest)
        else:
            return int((self.check_x(x, y, square_state, False, False) +
                        self.check_y(x, y, square_state, False, False) +
                        self.check_left_diag(x, y, square_state, False, False) +
                        self.check_right_diag(x, y, square_state, False, False)) - 4)

    def check_n_of_available_axis(self, index: int, square_state: SquareState) -> int:
        coord = self.get_index_coord(index)
        axis = 0
        if self.check_x(coord[0], coord[1], square_state, False, True) >= self.seq_to_win:
            axis += 1
        if self.check_y(coord[0], coord[1], square_state, False, True) >= self.seq_to_win:
            axis += 1
        if self.check_left_diag(coord[0], coord[1], square_state, False, True) >= self.seq_to_win:
            axis += 1
        if self.check_right_diag(coord[0], coord[1], square_state, False, True) >= self.seq_to_win:
            axis += 1
        return axis

    def spaces_of_around(self, index: int, square_state: SquareState) -> int:
        count = 0
        x, y = self.get_index_coord(index)
        if x - 1 >= 0:
            if square_state == self.get_square(x-1, x):
                count += 1
        if x + 1 < self.x_size:
            if square_state == self.get_square(x+1, y):
                count += 1
        if x != 0:
            check_x = x - 1
            spaces_to_check = 3
        else:
            check_x = 0
            spaces_to_check = 2
        for i in range(spaces_to_check):
            if check_x + i < self.x_size:
                if y - 1 >= 0:
                    if square_state == self.get_square(check_x+i, y - 1):
                        count += 1
                if y + 1 < self.y_size:
                    if square_state == self.get_square(check_x+i, y + 1):
                        count += 1
        return count
