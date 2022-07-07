import random
from collections import Counter
import time

board = [[' A1', ' A2', ' A3'],
         [' B1', ' B2', ' B3'],
         [' C1', ' C2', ' C3']]

symbols = [" O ", " X "]
players = ["AiPlayer", "HumanPlayer"]


class HumanPlayer:

    def __init__(self, symbol, mode):
        self.symbol = symbol
        self.mode = mode

    def move(self):
        try:
            result = Game().check_winner()
            if result == f'keep going':

                move = input("Enter where you want to place your letter: ")
                move = f' {move}'

                # find index of selected move and place it
                i = 0
                no_spot = 0
                while i < 3:
                    if move in board[i]:
                        index = board[i].index(move)
                        board[i][index] = self.symbol
                    else:
                        no_spot = no_spot + 1
                    i = i + 1
                if no_spot == 3:
                    print("Invalid enter. ")
                    self.move()
                show = Game.show_board()
                print(show)

                num_of_open_spots = Game.open_spots()
                if self.symbol == " X " and num_of_open_spots > 0:  # if no tie and symbol = X
                    # if human vs computer --> computer's turn
                    if self.mode == 2:
                        AiPlayer(" O ", self.mode).move()
                    # if human vs human --> human's turn (player2)
                    else:
                        SecondHumanPlayer(" O ", self.mode).move()
                elif self.symbol == " O " and num_of_open_spots > 0:  # if no tie and symbol = O
                    # if human vs computer --> computer's turn
                    if self.mode == 2:
                        AiPlayer(" X ", self.mode).move()
                    # if human vs human --> human's turn (player2)
                    else:
                        SecondHumanPlayer(" X ", self.mode).move()

                # if number of available spots decreased to 0 after move
                else:
                    result = Game().check_winner()
                    print(result)
            else:
                result = Game().check_winner()
                print(result)

        except ValueError as err:
            print(err)
            self.move()


class AiPlayer:

    def __init__(self, symbol, mode):
        self.symbol = symbol
        self.mode = mode

    def move(self):
        result = Game().check_winner()
        if result == f'keep going':
            open_spots = Game.list_of_open_spots()

            if self.mode == 3:
                time.sleep(2)

            move = random.choice(open_spots)
            i = 0
            while i < 3:
                if move in board[i]:
                    index = board[i].index(move)
                    board[i][index] = self.symbol
                i = i + 1
            show = Game.show_board()
            print(show)

            num_of_open_spots = Game.open_spots()
            if self.symbol == " X " and num_of_open_spots > 0:  # if no tie and symbol = X
                # if human vs computer --> human's turn
                if self.mode == 2:
                    HumanPlayer(" O ", self.mode).move()
                # if computer vs computer --> computer's turn (player2)
                else:
                    SecondAiPlayer(" O ", self.mode).move()
            elif self.symbol == " O " and num_of_open_spots > 0:    # if no tie and symbol = 0
                # if human vs computer --> human's turn
                if self.mode == 2:
                    HumanPlayer(" X ", self.mode).move()
                # if computer vs computer --> computer's turn (player2)
                else:
                    SecondAiPlayer(" X ", self.mode).move()
            else:
                result = Game().check_winner()
                print(result)
        else:
            result = Game().check_winner()
            print(result)


class SecondHumanPlayer(HumanPlayer):

    def __init__(self, symbol, mode):
        super().__init__(symbol, mode)


class SecondAiPlayer(AiPlayer):

    def __init__(self, symbol, mode):
        super().__init__(symbol, mode)


class UnbeatableAi(AiPlayer):

    def __init__(self, symbol, mode):
        super().__init__(symbol, mode)


class Game:

    def __init__(self):
        pass

    def set_up(self):
        try:
            game_option = int(input("Choose from: 1vs1(1), MeVsComputer(2), ComputerVsComputer(3), MeVsAI(4): "))

            # human vs human
            if game_option == 1:
                players.insert(1, "SecondHumanPlayer")
                letter = input("Choose between O and X: ")
                choice = random.choice(players)
                show = self.show_board()
                print(show)
                if letter == "O" or letter == "o":
                    if choice == "SecondHumanPlayer":
                        SecondHumanPlayer(" X ", 1).move()
                    else:
                        HumanPlayer(" O ", 1).move()
                elif letter == "X" or letter == "x":
                    if choice == "SecondHumanPlayer":
                        SecondHumanPlayer(" O ", 1).move()
                    else:
                        HumanPlayer(" X ", 1).move()
                else:
                    print("Invalid enter.")
                    self.set_up()

            # human vs computer
            elif game_option == 2:
                letter = input("Choose between O and X: ")
                choice = random.choice(players)
                if letter == "O" or letter == "o":
                    if choice == "AiPlayer":
                        AiPlayer(" X ", 2).move()
                    else:
                        show = self.show_board()
                        print(show)
                        HumanPlayer(" O ", 2).move()
                elif letter == "X" or letter == "x":
                    if choice == "AiPlayer":
                        AiPlayer(" O ", 2).move()
                    else:
                        show = self.show_board()
                        print(show)
                        HumanPlayer(" X ", 2).move()
                else:
                    print("Invalid enter.")
                    self.set_up()

            # computer vs computer
            elif game_option == 3:
                players.insert(2, "SecondAiPlayer")
                choice = random.choice(players)
                if choice == "SecondAiPlayer":
                    SecondAiPlayer(" X ", 3).move()
                else:
                    AiPlayer(" O ", 3).move()

            # human vs unbeatable AI
            elif game_option == 4:
                pass

            else:
                print("Invalid enter. ")
                self.set_up()

        except ValueError as err:
            print(err)
            self.set_up()

    # function for showing the board
    @staticmethod
    def show_board():
        shown_board = (f'|{board[0][0]}|{board[0][1]}|{board[0][2]}|\n'
                       f'|{board[1][0]}|{board[1][1]}|{board[1][2]}|\n'
                       f'|{board[2][0]}|{board[2][1]}|{board[2][2]}|\n')
        return shown_board

    # function for number of open spots
    @staticmethod
    def open_spots():
        open_spots = 9
        i = 0
        while i < 3:
            if " O " or " X " in board[i]:
                dic = Counter(board[i])
                count = dic[" O "] + dic[" X "]
                open_spots = open_spots - count
            i = i + 1
        return open_spots

    # function for random pick of spot by AI
    @staticmethod
    def list_of_open_spots():
        open_spots = []
        i = 0
        while i < 3:
            open_spots_one = [x for x in board[i] if x != " O " and x != " X "]
            open_spots.extend(open_spots_one)
            i = i + 1
        return open_spots

    def check_winner(self):
        open_spots = self.open_spots()

        # check all possible winning combinations
        i = 0
        while i < 3:
            result = 0

            if board[i][0] == board[i][1] == board[i][2]:
                result = f'{board[i][0]} won the game'
            elif board[0][i] == board[1][i] == board[2][i]:
                result = f'{board[0][i]} won the game'
            elif board[1][1] == board[2][2] == board[0][0]:
                result = f'{board[1][1]} won the game'
            elif board[0][2] == board[1][1] == board[2][0]:
                result = f'{board[0][2]} won the game'

            # if somebody won
            if result != 0:
                return result
            i = i + 1

        # when no spots are available and no one wins --> tie
        if open_spots == 0:
            result = f'Tie.'
            return result

        return f'keep going'


Game().set_up()