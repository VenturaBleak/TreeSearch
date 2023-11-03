# visualize_solution.py
import time
import gymnasium as gym
from solvers.dfs_solver import DFSSolver

if __name__ == '__main__':
    # Register the environment
    gym.register(
        id='TwoThousandFortyEight-v0',
        entry_point='game_environment:TwoThousandFortyEightEnv',
        kwargs={'human_renderer': True}  # Set to True to enable human rendering
    )

    # To play with the GUI
    env = gym.make('TwoThousandFortyEight-v0')
    solver = DFSSolver(env)

    obs, _, terminated, truncated, info = env.reset()

    while not terminated and not truncated:
        action = solver.solve(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        if info.get('solved', False):
            print("Goal state reached!")
            break
        env.render()
        time.sleep(0.05)

    print("Solution has been executed.")

    time.sleep(5)
    env.close()