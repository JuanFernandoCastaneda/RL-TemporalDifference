from board import Board
from random import random, choice

class Noise:
    def __init__(self, action_noise: dict) -> None:
        self.action_noise = action_noise

    def do_action(self, action: Board.Actions, possible_actions: list) -> Board.Actions:
        probability = random()
        if probability >= self.action_noise[action]:
            return action
        else:
            return choice(possible_actions)
