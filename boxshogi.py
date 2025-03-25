import sys
from game_modes.filegame import FileGame
from game_modes.interactivegame import InteractiveGame
def main():
    """
    Main function to read terminal input
    """
    if sys.argv[1] == '-f':
        file_mode = FileGame()
        file_mode.run_game_file_mode(sys.argv[2])

    if sys.argv[1] == '-i':
        interactive_mode = InteractiveGame()
        interactive_mode.start_interactive_game()

if __name__ == "__main__":
    main()