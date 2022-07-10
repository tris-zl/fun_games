import random
from collections import Counter
import time
import math


board = [[' A1', ' A2', ' A3'],
         [' B1', ' B2', ' B3'],
         [' C1', ' C2', ' C3']]

symbols = []
players = ["AiPlayer", "HumanPlayer"]


class Player:

    def __init__(self, symbol, mode):
        self.symbol = symbol
        self.mode = mode

    def move(self):
        pass


class HumanPlayer(Player):

    def __init__(self, symbol, mode):
        super().__init__(symbol, mode)

    def move(self):
        try:
            open_spots = Game.open_spots()
            if open_spots == 9:
                show = Game.show_board()
                print(show)

            result = Game().check_winner()
            if not result:

                move = input("Enter where you want to place your letter: ")
                move = f' {move}'

                # find index of selected move and place it
                no_spot = 0
                for i in range(3):
                    if move in board[i]:
                        index = board[i].index(move)
                        board[i][index] = self.symbol
                    else:
                        no_spot = no_spot + 1
                if no_spot == 3:
                    print("Invalid enter. ")
                    self.move()

            else:
                result = Game().check_winner()
                print(result)

            show = Game.show_board()
            print(show)

        except ValueError as err:
            print(err)
            self.move()


class AiPlayer(Player):

    def __init__(self, symbol, mode):
        super().__init__(symbol, mode)

    def move(self):
        result = Game().check_winner()
        if not result:
            open_spots = Game.list_of_open_spots()

            # time delay for computer vs computer
            if self.mode == 3:
                time.sleep(2)

            # random choice
            if self.mode == 2 or self.mode == 3:
                move = random.choice(open_spots)
                for i in range(3):
                    if move in board[i]:
                        index = board[i].index(move)
                        board[i][index] = self.symbol

            # start of minimax
            else:
                best_score = -math.inf
                best_move = []  # declaration so best_move cannot be undefined
                for i in range(3):
                    for j in range(3):
                        if board[i][j] in open_spots:  # if spot is still empty
                            saved = board[i][j]  # save board to restore it later
                            board[i][j] = self.symbol   # place symbol
                            # call minimax
                            if self.symbol == " O ":
                                score = UnbeatableAi(" O ", self.mode).minimax(" X ", False)
                            else:
                                score = UnbeatableAi(" X ", self.mode).minimax(" O ", False)
                            board[i][j] = saved  # restore board as it was before
                            #  compares all possibilities and sets the best move
                            if score > best_score:
                                best_score = score
                                best_move = [i, j]
                board[best_move[0]][best_move[1]] = self.symbol  # best move

        else:
            print(result)

        show = Game.show_board()
        print(show)


class SecondHumanPlayer(HumanPlayer):

    def __init__(self, symbol, mode):
        super().__init__(symbol, mode)


class SecondAiPlayer(AiPlayer):

    def __init__(self, symbol, mode):
        super().__init__(symbol, mode)


class UnbeatableAi(AiPlayer):

    def __init__(self, symbol, mode):
        super().__init__(symbol, mode)

    def minimax(self, symbol, is_maximizing):
        result = Game().check_winner()

        # if there is a tie or somebody won
        if result:
            score = Game().scores(self.symbol, result)
            return score

        else:
            if is_maximizing:
                open_spots = Game().list_of_open_spots()
                best_score = -math.inf
                for i in range(3):
                    for j in range(3):
                        if board[i][j] in open_spots:
                            saved = board[i][j]
                            board[i][j] = symbol
                            if symbol == " O ":
                                score = self.minimax(" X ", False)
                            else:
                                score = self.minimax(" O ", False)
                            board[i][j] = saved
                            if score > best_score:
                                best_score = score
                return best_score

            else:
                open_spots = Game().list_of_open_spots()
                best_score = math.inf
                for i in range(3):
                    for j in range(3):
                        if board[i][j] in open_spots:
                            saved = board[i][j]
                            board[i][j] = symbol
                            if symbol == " O ":
                                score = self.minimax(" X ", True)
                            else:
                                score = self.minimax(" O ", True)
                            board[i][j] = saved
                            if score < best_score:
                                best_score = score
                return best_score


class Game:

    def __init__(self):
        pass

    def set_up(self):
        try:
            game_option = int(input("Choose from: 1vs1(1), MeVsComputer(2), ComputerVsComputer(3), MeVsAI(4): "))

            letter = input("Choose between O and X: ")
            letter_two = ""
            if letter == "O" or letter == "X":
                letter = f' {letter} '
                letter_two = " O " if letter == " X " else " X "
            else:
                print("Invalid enter.")
                self.set_up()

            result = None

            # human vs human
            if game_option == 1:
                players.insert(1, "SecondHumanPlayer")
                choice = random.choice(players)
                if choice == "SecondHumanPlayer":
                    while not result:
                        SecondHumanPlayer(letter_two, 1).move()
                        result = self.check_winner()
                        if not result:
                            HumanPlayer(letter, 1).move()
                        result = self.check_winner()
                else:
                    while not result:
                        HumanPlayer(letter, 1).move()
                        result = self.check_winner()
                        if not result:
                            SecondHumanPlayer(letter_two, 1).move()
                        else:
                            result = self.check_winner()
                            print(result)
                        result = self.check_winner()

            # human vs computer
            elif game_option == 2:
                choice = random.choice(players)
                if choice == "AiPlayer":
                    while not result:
                        AiPlayer(letter_two, 2).move()
                        result = self.check_winner()
                        if not result:
                            HumanPlayer(letter, 2).move()
                        else:
                            result = self.check_winner()
                            print(result)
                        result = self.check_winner()
                else:
                    while not result:
                        HumanPlayer(letter, 2).move()
                        result = self.check_winner()
                        if not result:
                            AiPlayer(letter_two, 2).move()
                        else:
                            result = self.check_winner()
                            print(result)
                        result = self.check_winner()

            # computer vs computer
            elif game_option == 3:
                while not result:
                    SecondAiPlayer(letter_two, 3).move()
                    result = self.check_winner()
                    if not result:
                        AiPlayer(letter, 3).move()
                    else:
                        result = self.check_winner()
                        print(result)
                    result = self.check_winner()

            # human vs unbeatable AI
            elif game_option == 4:
                players.insert(1, "UnbeatableAi")
                choice = random.choice(players)
                if choice == "UnbeatableAi":
                    while not result:
                        UnbeatableAi(letter_two, 4).move()
                        result = self.check_winner()
                        if not result:
                            HumanPlayer(letter, 4).move()
                        else:
                            result = self.check_winner()
                            print(result)
                        result = self.check_winner()
                else:
                    while not result:
                        HumanPlayer(letter, 4).move()
                        result = self.check_winner()
                        if not result:
                            UnbeatableAi(letter_two, 4).move()
                        else:
                            result = self.check_winner()
                            print(result)
                        result = self.check_winner()

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
        for i in range(3):
            if " O " or " X " in board[i]:
                dic = Counter(board[i])
                count = dic[" O "] + dic[" X "]
                open_spots = open_spots - count
        return open_spots

    # function for random pick of spot by AI
    @staticmethod
    def list_of_open_spots():
        open_spots = []
        for i in range(3):
            open_spots_one = [x for x in board[i] if x != " O " and x != " X "]
            open_spots.extend(open_spots_one)
        return open_spots

    def check_winner(self):
        open_spots = self.open_spots()

        # check all possible winning combinations
        for i in range(3):
            result = 0

            if board[i][0] == board[i][1] == board[i][2]:
                result = f'{board[i][0]}won the game'
            elif board[0][i] == board[1][i] == board[2][i]:
                result = f'{board[0][i]}won the game'
            elif board[1][1] == board[2][2] == board[0][0]:
                result = f'{board[1][1]}won the game'
            elif board[0][2] == board[1][1] == board[2][0]:
                result = f'{board[0][2]}won the game'

            # if somebody won
            if result != 0:
                return result

        # when no spots are available and no one wins --> tie
        if open_spots == 0:
            result = f'Tie.'
            return result

        return None

    @staticmethod
    def scores(symbol, result):
        if symbol == " X ":
            scores = {
                " X won the game": 1,
                " O won the game": -1,
                "Tie.": 0
            }
        else:
            scores = {
                " X won the game": -1,
                " O won the game": 1,
                "Tie.": 0
            }
        score = scores[result]
        return score


Game().set_up()
