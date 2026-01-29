# goal: print out our board that doesnt have a snake yet. a board is a width by height string of .'s. We want this reprinting every tick

import keyboard
import sys
import os

class Game:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

        self.game_over = False

        # List[List[Str]]
        self.board = self.make_board()
        
        keyboard.add_hotkey('r', self.restart)
        pass

    # will return the list of lists that is the game board
    def make_board(self):
        board = []

        for j in range(self.height):
            board.append([])

        for inner_list_j in range(len(board)):
            inner_list = board[inner_list_j]

            for i in range(self.width):
                inner_list.append('. ')

        return board

    def create_board_string(self):
        # OUTPUT what the user sees (Front end, GUI)
        board_string = ''
        for i in range(len(self.board)):
            inner_list = self.board[i]
            for j in range(len(inner_list)):
                board_string += inner_list[j]
            board_string += '\n'
        return board_string

    
    def run_game(self):
        while not self.game_over:
            board_string = self.create_board_string()
            os.system("clear")   # macOS/Linux
            print(board_string)

    def restart(self):
        self.game_over = True

game = Game(10, 10)

game.run_game()

