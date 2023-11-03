# game_environment.py
import gymnasium as gym
from gymnasium import spaces
from tkinter import Tk
import pickle

# import custom modules
from game_logic import Game
from game_ui import GameUI

class TwoThousandFortyEightEnv(gym.Env):
    metadata = {'render.modes': ['human', 'none']}

    def __init__(self, size=4, win_tile=2048, human_renderer=False, truncate_at=100000):
        super(TwoThousandFortyEightEnv, self).__init__()

        self.size = size
        self.win_tile = win_tile
        self.truncate_at = truncate_at
        self.move_count = 0

        self.game = Game(size=self.size, win_tile=self.win_tile)
        self.human_renderer = human_renderer
        self.game_app = None

        self.action_space = spaces.Discrete(4)  # up, down, left, right
        self.observation_space = spaces.Box(low=0, high=self.win_tile, shape=(self.size, self.size), dtype=int)

        self.terminated = False
        self.truncated = False

        # action space is discrete
        self.action_set = [0, 1, 2, 3]  # up, down, left, right as numeric values
        self._reset_info()

    def step(self, action):
        # Update move count
        self.move_count += 1

        # Get direction from action
        direction = self.action_set[action]

        if direction not in self.game.get_legal_moves():
            # Illegal move, penalize
            reward = -100
        else:
            # Legal move, update game state and reward
            self.game.grid, self.game.score, game_over = self.game.play(self.action_set[action])
            reward = self.game.score

        # Check if game is truncated
        self.truncated = self.move_count >= self.truncate_at

        # Check if game is terminated, i.e. game over or solved
        max_tile = self.game.get_max_tile()
        solved = max_tile >= self.win_tile
        self.terminated = game_over or solved

        # Update info
        self._update_info(max_tile, game_over, solved)

        return self.game.grid, reward, self.terminated, self.truncated, self.info

    def reset(self):
        self.move_count = 0
        self.game = Game(size=self.size, win_tile=self.win_tile)
        self.terminated = False
        self.truncated = False
        self._reset_info()
        return self.game.grid, 0, self.terminated, self.truncated, self.info

    def render(self, mode='human'):
        if self.human_renderer and mode == 'human':
            if self.game_app is None:
                print("Initializing UI...")  # Log statement for debugging
                self.game_app = GameUI(Tk(), self.game, visual=True)
                self.game_app.master.protocol("WM_DELETE_WINDOW", self.close)
                self.game_app.init_ui()
            else:
                self.game_app.update_grid_cells()
            self.game_app.master.update_idletasks()
            self.game_app.master.update()

    def close(self):
        if self.game_app is not None:
            self.game_app.master.destroy()
            self.game_app = None

    def _update_info(self, max_tile, game_over, solved):
        self.info = {
            'score_sum': self.game.score,
            'score_max_tile': max_tile,
            'game_over': game_over,
            'solved': solved
        }

    def _reset_info(self):
        self.info = {
            'score_sum': self.game.score,
            'score_max_tile': self.game.get_max_tile(),
            'game_over': False,
            'solved': False
        }