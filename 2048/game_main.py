# game_main.py
from tkinter import Tk
from game_ui import GameUI
from game_state import GameState

def main():
    root = Tk()
    game_state = GameState()
    game_ui = GameUI(root, game_state, visual=True)
    game_ui.run()

if __name__ == "__main__":
    main()