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

    def get_square(self, x: int, y: int) -> SquareState:
        return self.squares[self.get_coord_index(x, y)]

    def get_coord_index(self, x, y) -> int:
        return int(x + self.x_size * y)

    def get_index_coord(self, index) -> (int, int):
        return index % self.x_size, int(index / self.x_size)

    def set_square(self, x: int, y: int, state: SquareState) -> TurnState:
        i = self.get_coord_index(x, y)
        if not self.squares[i].is_none():
            return TurnState.Error
        self.squares[i] = state
        self.filled += 1
        return self.check_game_over(x, y, state)

    def set_square_from_index(self, index: int, square_state: SquareState) -> TurnState:
        if not self.squares[index].is_none():
            return TurnState.Error
        self.squares[index] = square_state
        self.filled += 1
        coord = self.get_index_coord(index)
        return self.check_game_over(coord[0], coord[1], square_state)


    def check_game_over(self, x: int, y: int, state: SquareState) -> TurnState:
        if self.filled >= self.seq_to_win + 2 and \
                ((self.check_x(x, y, state, True, False) >= self.seq_to_win) or \
                (self.check_y(x, y, state, True, False) == self.seq_to_win) or \
                (self.check_left_diag(x, y, state, True, False) == self.seq_to_win) or \
                (self.check_right_diag(x, y, state, True, False) == self.seq_to_win)):
            return TurnState.Victory
            
        if self.check_draw():
            return TurnState.Draw
        return TurnState.Continue

    def all_lines_checker(self, x: int, y: int, state: SquareState, stop_counting: bool, check_x_axis: bool, check_y_axis: bool, inverted = False) -> tuple[int, int]:
        available_spaces_count = 1
        seq_count = 1
        if check_x_axis == check_y_axis:
            def loop_condition(dist: int, check: tuple[int, int]):
                offset_x, offset_y = (dist, -dist) if inverted else (dist, dist)
                check_x, check_y = check
                result = \
                    x + offset_x >= 0 and \
                    y + offset_y >= 0 and \
                    dist < self.seq_to_win

                if result:
                    check_y = y + offset_y
                    check_x = x + offset_x
                return result, (check_x, check_y)
        else:
            def loop_condition(dist: int, check: tuple[int, int]):
                check_x, check_y = check
                if check_x_axis:
                    result = x + dist >= 0 and dist < self.seq_to_win
                    if result:
                        check_x = x + dist
                    return result, (check_x, y)
                else:
                    result = y + dist >= 0 and dist < self.seq_to_win
                    if result:
                        check_y = x + dist
                    return result, (x, check_y)
                
        for i in [1, -1]:
            dist = i
            checking_x = x
            checking_y = y
            while True:
                result, (checking_x, checking_y) = loop_condition(dist, (checking_x, checking_y))
                if not result:
                    break
                square_state = self.get_square(int(checking_x), int(checking_y))
                if square_state is not None:
                    if square_state == state:
                        seq_count += 1
                    elif stop_counting or not square_state.is_none():
                        break
                else:
                    break
                dist += i
                available_spaces_count += 1
        return seq_count, available_spaces_count

    def check_for_victory(self, x: int, y: int, state: SquareState, x_axis: bool, y_axis: bool, stop_counting = False, return_available_spaces=False, inverted_axis = False) -> int:
        result = self.all_lines_checker(x, y, state, stop_counting, x_axis, y_axis, inverted_axis)
        if return_available_spaces:
            return result[1]
        elif not stop_counting or result[0] >= self.seq_to_win:
            return result[0]
        else:
            return 1


    def check_x(self, x: int, y: int, state: SquareState, stop_counting: bool, return_available_spaces: bool) -> int:
        return self.check_for_victory(x, y, state, stop_counting, return_available_spaces, True, False, False)

    def check_y(self, x: int, y: int, state: SquareState, stop_counting: bool, return_available_spaces: bool) -> int:
        return self.check_for_victory(x, y, state, stop_counting, return_available_spaces, False, True, False)

    def check_left_diag(self, x: int, y: int, state: SquareState, stop_counting: bool, return_available_spaces: bool) -> int:
        return self.check_for_victory(x, y, state, stop_counting, return_available_spaces, True, True, False)

    def check_right_diag(self, x: int, y: int, state: SquareState, stop_counting: bool, return_available_spaces: bool) -> int:
        return self.check_for_victory(x, y, state, stop_counting, return_available_spaces, True, True, True)


    def check_draw(self):
        return self.filled == len(self.squares)

    def size(self):
        return self.x_size * self.y_size

    def get_square_by_index(self, index):
        return self.squares[index]

    def clear(self):
        self.squares = [SquareState() for _ in range(self.x_size * self.y_size)]
        self.filled = 0

    def sum_squares_in_winnable_distance(self, index: int, square_state: SquareState, return_highest = False) -> int:
        x, y = self.get_index_coord(index)
        if return_highest:
            count = [0,0,0,0]
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
        coord = self.get_index_coord(index)
        count = 0
        if coord[0] > 0:
            n = coord[0] - 1
            square = self.get_square(n, coord[1])
            if square is not None and square_state == square:
                count += 1
        square = self.get_square(coord[0] + 1, coord[1])
        if square is not None and square_state == square:
            count += 1
        x = 0
        n = 2
        if coord[0] != 0:
            x = coord[0] - 1
            n = 3
        top_y = coord[1] - 1
        for i in range(n):
            if top_y is not None:
                square = self.get_square(x + i, top_y)
                if square is not None and square_state == square:
                    count += 1
            square = self.get_square(x + i, coord[1] + 1)
            if square is not None and square_state == square:
                count += 1
        return count

