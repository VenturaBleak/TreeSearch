# game_main.py
from tkinter import Tk
from game_ui import GameUI
from game_logic import Game

def main():
    root = Tk()
    game = Game()
    game_app = GameUI(root, game)  # Pass the game instance directly
    game_app.run()

if __name__ == "__main__":
    main()
