"""Main entry point for 4x4 Tic Tac Toe game."""

import sys
import argparse
from tictactoe.user_interface import UserInterface


def main():
    """Main function to start the game."""
    parser = argparse.ArgumentParser(
        description='Play 4x4 Tic Tac Toe against an AI opponent'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='4x4 Tic Tac Toe v1.0'
    )
    
    args = parser.parse_args()
    
    try:
        ui = UserInterface()
        ui.start_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
