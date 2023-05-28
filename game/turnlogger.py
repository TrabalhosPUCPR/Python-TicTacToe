from datetime import datetime, timedelta
from game.tictactoecore import TurnState


class TurnLogger:
    def __init__(self):
        self.start_time = datetime.now()
        self.end_time = datetime.now()
        self.player_n_turn = 0
        self.latest_placed_coord = (0, 0)
        self.game_state = TurnState.Continue
        self.total_turns = 0

    def restart_timer(self):
        self.start_time = datetime.now()

    def end_timer(self):
        self.end_time = datetime.now()

    def elapsed_time(self) -> timedelta:
        return self.end_time - self.start_time

    def __str__(self):
        return f"Turn: {self.total_turns}\nPlaced coordinates: x={self.latest_placed_coord[0]}; y={self.latest_placed_coord[1]}\nGame State: {self.game_state}\nElapsed Time: {self.elapsed_time().total_seconds()}"
