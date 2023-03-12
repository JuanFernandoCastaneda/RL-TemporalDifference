from enum import Enum
from random import randint

class Board:
    # Parameter Dimensions: tuple containing the dimensions (x, y).

    def __init__(self, skeleton: list) -> None:
        self._board = skeleton
        self._dimensions = (len(skeleton), len(skeleton[0]))
        self._initial_state = self.reset_random()
        self._current_state = self._initial_state

    def _reward_map(self, cell_value: str) -> float:
        # Wall.
        if cell_value == "*":
            return None
        # Terminal state.
        elif "T" in cell_value:
            return float(cell_value[1:])
        # Everything else.
        else:
            return float(cell_value)
        
    def current_state(self) -> tuple:
        return self._current_state
    
    def dimensions(self) -> tuple:
        return self._dimensions
        
    class Actions(Enum):
        UP = (-1, 0)
        DOWN = (1, 0)
        RIGHT = (0, 1)
        LEFT = (0, -1)

    def _is_terminal(self) -> bool:
        x, y = self._current_state
        return "T" in self._board[x][y]
        
    def possible_actions(self) -> list:
        x, y = self._current_state
        if self._is_terminal(): 
            return []
        def legal_action(action):
            action_value = action.value
            xf, yf = x + action_value[0], y + action_value[1]
            return xf < self._dimensions[0] and xf >= 0 and yf < self._dimensions[1] and yf >= 0 \
                and self._board[xf][yf] != "*"
        return list(filter(legal_action, [action for action in self.Actions]))
    
    # Returns tuple reward - new state
    def do_action(self, action: Actions):
        if action not in self.possible_actions() or self._is_terminal():
            raise Exception("Illegal action")
        x0, y0 = self._current_state
        xf, yf = x0 + action.value[0], y0 + action.value[1]
        self._current_state = (xf, yf)
        return (self._reward_map(self._board[xf][yf]), self._current_state)
    
    def reset(self) -> None:
        self._current_state = self._initial_state

    def reset_random(self) -> tuple:
        apt = False
        while not apt:
            xf, yf = randint(0, self._dimensions[0]-1), randint(0, self._dimensions[1]-1)
            if self._board[xf][yf] != "*" and "T" not in self._board[xf][yf]:
                self._initial_state = (xf, yf)
                self._current_state = (xf, yf)
                apt = True
        return self._current_state

