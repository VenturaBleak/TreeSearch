# visualize.py
import time
import random
import gymnasium as gym

# if name == 'main':
if __name__ == '__main__':
    # Register the environment
    gym.register(
        id='TwoThousandFortyEight-v0',
        entry_point='game_environment:TwoThousandFortyEightEnv',
        kwargs={'human_renderer': True}  # Set to True to enable human rendering
    )

    # To play with the GUI
    env = gym.make('TwoThousandFortyEight-v0')
    obs, reward, terminated, truncated, info = env.reset()
    print(f"obs: {obs}, reward: {reward}, terminated: {terminated}, truncated: {truncated}, info: {info}")
    while not terminated and not truncated:
        # Get legal moves which will now be numeric
        legal_moves = env.game.get_legal_moves()
        print(f"legal moves: {legal_moves}")
        action = random.choice(legal_moves)
        print(f"action: {action}")
        obs, reward, terminated, truncated, info = env.step(action)
        print(f"obs: {obs}, reward: {reward}, terminated: {terminated}, truncated: {truncated}, info: {info}")
        env.render()  # Render the GUI based on the instantiation parameter
        time.sleep(0.05)
    # When the game is terminated or truncated, wait for a specified delay and then close the GUI
    time.sleep(5)
    env.close()