from game.ai.aiplayer import Ai
from game.player import Player
from game.tictactoecore import TicTacToe, SquareState, TurnState
from game.turnlogger import TurnLogger

TITLE = """
  _______     _______      _______
 |__   __|   |__   __|    |__   __|
    | |   _  ___| | __ _  ___| | ___   ___
    | |  | |/ __| |/ _` |/ __| |/ _ \\ / _ \\
    | |  | | (__| | (_| | (__| | (_) |  __/
    |_|  |_|\\___|_|\\__,_|\\___|_|\\___/ \\___|

"""
AUTHOR = "Gabrielle, Kovalski and KnightLeo"
REPO_LINK = "https://github.com/TrabalhosPUCPR/PythonTicTacToe"
AI_MOVE_DELAY = 1000  # in ms


class AiDifficulties:
    Easy = 0,
    Medium = 1,
    Hard = 2


class GameState:
    Begin = 0
    PlayerTurn = 1
    Finished = 2

    def __init__(self, state, next_player: Player = None, next_player_n=None):
        self.state = state
        self.next_player = (next_player, next_player_n)


class TicTacToeGame:
    def __init__(self, player1=Player("Player1", 'X'), player2=Player("Player2", 'O'), show_turn_info=False):
        self.player1 = player1
        self.player2 = player2
        self.board = TicTacToe()
        self.show_turn_info = show_turn_info
        self.game_state = GameState(GameState.Begin, next_player=player1, next_player_n=1)

    def __str__(self):
        if self.game_state.state == GameState.Begin or self.game_state.state == GameState.PlayerTurn:
            return f"\n{self.game_state.next_player[0].name}'s turn!\n\n" + self.board.__str__()
        if self.game_state.state == GameState.Finished:
            return "\nGame is finished!" + self.board.__str__()

    @staticmethod
    def setup_new_game_with_prompts():
        while True:
            print(f"{TITLE}\t\tMade by {AUTHOR}\nRepo link: {REPO_LINK}\n\n")
            try:
                choice = int(input("\nPlease choose an option:\n1-Load 1 player game\n2-Load 2 player game\n3-Load Ai "
                                   "game\n(default: 1)"))
            except ValueError:
                choice = 1

            if choice == 2:
                game = TicTacToeGame.load_default_2player_game()
            elif choice == 3:
                game = TicTacToeGame.load_default_ai_game(AiDifficulties.Hard, AiDifficulties.Hard)
            else:
                try:
                    dif = int(input("\nChoose a difficulty for the AI\n1-Easy\n2-Medium\n3-Hard\n(default: 3):"))
                except ValueError:
                    dif = 3
                game = TicTacToeGame.load_default_1player_game(dif - 1)
            print(f"\nBoard size: {game.board.size()}\nSequence to win: {game.board.seq_to_win}")
            try:
                choice = int(input("\n1-Start Game\n2-Configure Game\n(default: 1)"))
            except ValueError:
                choice = 1

            if choice == 2:
                while True:
                    try:
                        choice = int(input("\n1-Change board size\n2-Debug Mode\n3-Start Game\n(default: 3)"))
                    except ValueError:
                        choice = 3

                    if choice == 1:
                        size = int(input("\nType the new board size: "))
                        seq = int(input("\nType sequence length to win: "))
                        if not game.change_size(size, seq):
                            print("\nInvalid size or sequence length!")
                    elif choice == 2:
                        if game.show_turn_info:
                            print("\nDebug Mode Deactivated!")
                            game.show_turn_info = False
                        else:
                            print("\nDebug Mode Activated!")
                            game.show_turn_info = True
                    else:
                        break
            else:
                break
        return game

    @staticmethod
    def load_default_1player_game(ai_difficulty):
        game = TicTacToeGame()
        game.player2 = TicTacToeGame.create_ai(game.player2, game.player1.square_symbol, ai_difficulty)
        return game

    @staticmethod
    def load_default_2player_game():
        return TicTacToeGame()

    @staticmethod
    def load_default_ai_game(ai1_difficulty, ai2_difficulty):
        game = TicTacToeGame()
        game.player1 = TicTacToeGame.create_ai(game.player1, game.player2.square_symbol, ai1_difficulty)
        game.player2 = TicTacToeGame.create_ai(game.player2, game.player1.square_symbol, ai2_difficulty)
        return game

    def start_game(self):
        turn_logger = TurnLogger()
        print(self)
        while self.game_state.state == GameState.Begin or self.game_state.state == GameState.PlayerTurn:
            turn_logger.restart_timer()
            x, y = self.game_state.next_player[0].act(self.board)
            turn_logger.end_timer()
            board_state = self.board.set_square(x, y)
            turn_logger.total_turns += 1
            turn_logger.latest_placed_coord = (x, y)
            turn_logger.player_n_turn = self.game_state.next_player[1]
            turn_logger.game_state = board_state
            if board_state == TurnState.Draw:
                print(f"\nAll spaces hae been filled! It's a draw!")
                self.game_state.state = GameState.Finished
            elif board_state == TurnState.Victory:
                print(f"\n{self.board.seq_to_win} in a row! {self.game_state.next_player[0].name} wins!")
                self.game_state.state = GameState.Finished
            elif board_state == TurnState.Error:
                print("\nPlease type a valid postition!")
                continue
            else:
                self.game_state.state = GameState.PlayerTurn
                if self.game_state.next_player[1] == 1:
                    self.game_state.next_player = (self.player2, 2)
                else:
                    self.game_state.next_player = (self.player1, 1)
            print(self)
        print("\nGame is finished!")

    @staticmethod
    def create_ai(player, op_symbol, difficulty):
        if difficulty == AiDifficulties.Easy:
            max_childs = 7
            max_layers = 1
        elif difficulty == AiDifficulties.Medium:
            max_childs = 6
            max_layers = 2
        else:
            max_childs = 10
            max_layers = 5
        return Ai(player, max_childs, max_layers, op_symbol)

    def change_size(self, size, seq_to_win) -> bool:
        if size < seq_to_win:
            return False
        self.board.x_size = size
        self.board.y_size = size
        self.board.seq_to_win = seq_to_win
        self.board.squares = [SquareState() for _ in range(size)]
        return True
