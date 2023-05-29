import copy

from game.ai.node import Node
from game.player import Player
from game.tictactoecore import SquareState, TicTacToe, TurnState


class Ai(Player):

    def __init__(self, player: Player, max_node_childs, max_layers, op_symbol):
        super().__init__(player.name, player.square_symbol)
        self.max_node_childs = max_node_childs
        self.max_layers = max_layers
        self.op_symbol = op_symbol

    def act(self, current_board) -> (int, int):
        root = Node((current_board, 0, TurnState.Continue))
        _, index = self.compute_moves(root, float('-inf'), float('inf'), self.max_layers, True)
        return current_board.get_index_coord(index)

    def compute_moves(self, current_node, alpha, beta, layer, maximizing):
        if layer == 0 or current_node.data[2] != TurnState.Continue:
            return current_node.data_score, current_node.data[1]
        if maximizing:
            best_move = (float('-inf'), 0)
            for move in self.get_possible_moves(current_node.data[0], maximizing):
                childs_best, _ = self.compute_moves(move, alpha, beta, layer-1, False)
                if best_move[0] < childs_best:
                    best_move = (childs_best, move.data[1])
                alpha = max(alpha, childs_best)
                if beta <= alpha:
                    break
            return best_move
        else:
            best_move = (float('inf'), 0)
            for move in self.get_possible_moves(current_node.data[0], maximizing):
                childs_best, _ = self.compute_moves(move, alpha, beta, layer-1, True)
                if best_move[0] > childs_best:
                    best_move = (childs_best, move.data[1])
                beta = min(beta, childs_best)
                if beta <= alpha:
                    break
            return best_move

    def get_possible_moves(self, current_board: TicTacToe, maximizing):
        moves = []
        for index, square in enumerate(current_board.squares):
            if square.is_none():
                if maximizing:
                    square_state = SquareState(self.square_symbol)
                else:
                    square_state = SquareState(self.op_symbol)
                board_copy = copy.deepcopy(current_board)
                possible_move_node = Node((board_copy, index, board_copy.set_square_from_index(index, square_state)))
                if possible_move_node.data[2] == TurnState.Victory:
                    if maximizing:
                        possible_move_node.data_score = 1.0
                    else:
                        possible_move_node.data_score = -1.0
                elif possible_move_node.data[2] == TurnState.Continue:
                    possible_move_node.data_score = self.get_move_heuristic(possible_move_node.data[0], square_state,
                                                                            index, maximizing)
                moves.append(possible_move_node)
        moves.sort(key=lambda x: x.data_score, reverse=maximizing)
        if len(moves) > 0 and len(moves) > self.max_node_childs:
            moves = moves[0:self.max_node_childs]
        return moves

    def get_move_heuristic(self, board: TicTacToe, square_state, index, maximizing) -> float:
        attack_score = board.sum_squares_in_winnable_distance(index, square_state)
        available_axis = board.check_n_of_available_axis(index, square_state)
        if maximizing:
            op_state = SquareState(self.op_symbol)
        else:
            op_state = SquareState(self.square_symbol)
        total_defense_score = board.sum_squares_in_winnable_distance(index, op_state)
        empty_space_around_score = board.spaces_of_around(index, SquareState())
        if board.seq_to_win**2 < board.size():
            highest_defense_score = board.sum_squares_in_winnable_distance(index, op_state, return_highest=True)
            if (board.seq_to_win % 2 != 0 and highest_defense_score >= (board.seq_to_win / 2.0).__ceil__()) or \
                    (board.seq_to_win % 2 == 0 and highest_defense_score >= (board.seq_to_win - 2)):
                total_defense_score *= 100
        coord = board.get_index_coord(index)
        if coord[1] == 0 or coord[1] == board.y_size-1:
            if 0 < coord[0] < board.x_size-1:
                empty_space_around_score = 0
        elif coord[0] == 0 or coord[0] == board.x_size-1:
            empty_space_around_score = 0
        total_defense_score /= 10.0
        heuristic = ((attack_score + total_defense_score + (available_axis/10.0)) +
                     (empty_space_around_score / 100.0)) / 100.0
        if maximizing:
            return heuristic
        else:
            return -heuristic
