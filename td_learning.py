from board import Board
from noise import Noise
from random import choice
import numpy as np
import matplotlib.pyplot as plt

class TemporalDifference:

    @classmethod
    def run(self, policy: list, alpha: int, board: Board, iterations: int, noise: Noise):
        gamma = 1
        value_function = [[0 for _ in range(board.dimensions()[1])] for _ in range(board.dimensions()[0])]
        change = True
        counter = 0
        while change:
            counter += 1
            print(counter)
            change = False
            board.reset_random()
            while True:
                x0, y0 = board.current_state()
                possible_actions = board.possible_actions()
                action_no_noise = policy[x0][y0]
                # Case in which the policy was not initialized correctly.
                if action_no_noise not in possible_actions:
                    policy[x0][y0] = choice(possible_actions)
                    action_no_noise = policy[x0][y0]
                # Adding the noise of the envirnoment to the action.
                action_with_noise = noise.do_action(action_no_noise, possible_actions)
                reward, new_state = board.do_action(action_with_noise)
                xf, yf = new_state
                v_s = value_function[x0][y0]
                v_s_prime = value_function[xf][yf]
                # Store old value function to check if something changed in the iteration.
                old_value_function = value_function[x0][y0]
                # Update the value function.
                value_function[x0][y0] = round(v_s + alpha*(reward + gamma*v_s_prime - v_s), 2)

                # -------------- VALUE ITERATION ------------------
                # change = self._value_iteration(old_value_function, value_function[x0][y0])

                # Check if it is terminal.
                new_possible_actions = board.possible_actions()
                if new_possible_actions == []:
                    break
                # If it is not terminal, update policy.
                old_policy = policy[xf][yf]
                policy[xf][yf] = self._max_value(value_function, (xf, yf), new_possible_actions)

                # --------------- POLICY ITERATION -------------------
                change = self._policy_iteration(old_policy, policy[xf][yf])
        return (value_function, policy)
    
    def _max_value(value_function: list, state: tuple, possible_actions: list) -> Board.Actions:
        x, y = state
        best = None
        best_value = float("-inf")
        for action in possible_actions:
            dx, dy = action.value
            if value_function[x + dx][y + dy] > best_value:
                best_value = value_function[x + dx][y + dy]
                best = action
        return best
    
    def _value_iteration(old_value, new_value):
        return old_value != new_value

    def _policy_iteration(old_policy, new_policy):
        return old_policy != new_policy


gridworld = [
    ["-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1"],
    ["-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1"],
    ["-0.1", "*", "*", "*", "*", "-0.1", "*", "*", "*", "-0.1"],
    ["-0.1", "-0.1", "-0.1", "-0.1", "*", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1"],
    ["-0.1", "-0.1", "-0.1", "-0.1", "*", "-1", "-0.1", "-0.1", "-0.1", "-0.1"],
    ["-0.1", "-0.1", "-0.1", "-0.1", "*", "T1", "-0.1", "-0.1", "-0.1", "-0.1"],
    ["-0.1", "-0.1", "-0.1", "-0.1", "*", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1"],
    ["-0.1", "-0.1", "-0.1", "-0.1", "*", "-1", "-1", "-0.1", "-0.1", "-0.1"],
    ["-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1"],
    ["-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1", "-0.1"],
]
hehe = [
    ["-0.1", "-0.1"],
    ["-0.1", "T1"]
]
board = Board(gridworld)
policy = [[Board.Actions.UP for _ in range(board.dimensions()[1])] for _ in range(board.dimensions()[0])]
noise = Noise({Board.Actions.UP: 0.3, 
                   Board.Actions.DOWN: 0.2, 
                   Board.Actions.LEFT: 0.2, 
                   Board.Actions.RIGHT: 0.3})
value_function, policy = TemporalDifference.run(policy, 0.9, board, 10000, noise)
array = np.array(list(map(lambda row: list(map(lambda action: abs(action.value[0])*2+abs(action.value[1]), row)), policy)))
plt.imshow(array, cmap='hot', interpolation='nearest')
plt.show()
