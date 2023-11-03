# game_environment.py
import gymnasium as gym
from gymnasium import spaces
from tkinter import Tk

# import custom modules
from game_logic import Game
from game_ui import GameUI

class TwoThousandFortyEightEnv(gym.Env):
    metadata = {'render.modes': ['human', 'none']}

    def __init__(self, size=4, win_tile=2048, human_renderer=False):
        super(TwoThousandFortyEightEnv, self).__init__()

        self.size = size
        self.win_tile = win_tile
        self.game = Game(size=self.size, win_tile=self.win_tile)
        self.human_renderer = human_renderer
        self.game_app = None  # Placeholder for the GUI

        self.action_space = spaces.Discrete(4)  # up, down, left, right
        self.observation_space = spaces.Box(low=0, high=self.win_tile,
                                            shape=(self.size, self.size),
                                            dtype=int)

        self.action_set = ['up', 'down', 'left', 'right']

    def step(self, action):
        direction = self.action_set[action]
        truncated, terminated = self.game.play(direction)

        # Define your reward here. This example gives a point for each merge.
        reward = self.game.score

        # Add any additional information you want to return
        info = {'score': self.game.score}

        return self.game.grid, reward, terminated, truncated, info

    def reset(self):
        self.game = Game(size=self.size, win_tile=self.win_tile)
        return self.game.grid

    def render(self, mode='none'):
        if self.human_renderer and mode == 'human':
            # Initialize GUI if it hasn't been already
            if self.game_app is None:
                root = Tk()
                self.game_app = GameUI(root, self.game, visual=True)
                root.after(0, self.game_app.run)  # Schedule the GUI to start
                root.mainloop()  # Start the GUI event loop
            else:
                self.game_app.update_grid_cells()
        elif mode == 'none':
            pass  # Do nothing for 'none' mode

    def close(self):
        if self.game_app is not None:
            self.game_app.master.destroy()
            self.game_app = None


# Register the environment
gym.register(
    id='TwoThousandFortyEight-v0',
    entry_point='your_module:TwoThousandFortyEightEnv',
    kwargs={'human_renderer': True}  # Set to True to enable human rendering
)

# To play with the GUI
env = gym.make('TwoThousandFortyEight-v0', human_renderer=True)
obs = env.reset()
for _ in range(1000):
    action = env.action_space.sample()
    obs, reward, done, truncated, info = env.step(action)
    if done:
        print("Game Over")
        break
    env.render(mode='human')  # Render the GUI