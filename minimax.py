__author__ = "Graham Traines CSCI7130 23 Sept 2014 Tic-Tac-Toe Minimax"
#Traines_900824397_CSCI_7130_F2014_HM3_RubyToPython

# This is my adaptation of the Ruby program that was originally provided
# I used the text

import copy
import numpy as np
import random
from abc import ABCMeta, abstractmethod

HUMAN_PLAYER_SYMBOL = ""
COMPUTER_PLAYER_SYMBOL = ""
BOARD_DIMENSION = 0
GAME_OVER = False
MIN_WINNING_MOVES = 0


class Board(object):
    def __init__(self):
        self.open = []
        self.closed = []
        self.can_check_win = False
        self.over = False
        self.dimension = BOARD_DIMENSION
        self.win = ''
        self.active_player = ""
        return

    def create_new_board(self, dimension):
        self.dimension = dimension
        self.grid = np.empty(shape=[dimension, dimension], dtype=str)
        for y in range(self.dimension):
            for x in range(self.dimension):
                self.grid[x][y] = " "
                self.open.append(Move(x, y))
        return

    def move(self, move):
        self.grid[move.x][move.y] = self.active_player
        self.open = [openmove for openmove in self.open if (openmove.x != move.x or openmove.y != move.y)]
        self.closed.append(move)
        if self.active_player == "X":
            self.active_player = "O"
        else:
            self.active_player = "X"

        if self.can_check_win == False and (len(self.closed) >= MIN_WINNING_MOVES):
            self.can_check_win = True
        if self.can_check_win:
            self.check_board_over()
            return
        return

    def check_board_over(self):
        self.win = GameStateEvaluator.win(self)
        if len(self.open) == 0 or (self.win != '' and self.win != None):
            self.over = True
        return

    def get_available_moves(self):
        return self.open

    def is_move_available(self, move):
        if any((openmove.x == move.x and openmove.y == move.y) for openmove in self.open):
            return True
        else:
            return False

    def print_board(self):
        print
        print(" ================================ ")
        print "  X: ",
        for x in range(self.dimension):
            print " %d  " % x,
        print
        print "Y:"
        for y in range(self.dimension):
            print " %d" % y,
            for x in range(self.dimension):
                print("[ %s ]" % self.grid[x][y]),
            print
        print(" ================================ ")
        print
        return


class Move(object):
    def __init__(self, xcoord, ycoord):
        self.x = xcoord
        self.y = ycoord
        return


class Player(object):
    def __init__(self, symbol):
        self.symbol = symbol
        return

    @abstractmethod
    def take_turn(self, board):
        pass


class HumanPlayer(Player):
    def take_turn(self, board):
        move = self.get_player_move(board)
        board.move(move)
        return

    def get_player_move(self, board):
        xcoord = int(raw_input("Enter the x-coordinate for your move (0 - %d): " % (BOARD_DIMENSION - 1)))
        ycoord = int(raw_input("Enter the y-coordinate for your move (0 - %d): " % (BOARD_DIMENSION - 1)))

        move = Move(xcoord, ycoord)
        if (board.is_move_available(move)) == True:
            return move
        else:
            print("Invalid move, try again.")
            self.get_player_move(board)


class ComputerPlayer(Player):
    def __init__(self, playersymbol):
        self.symbol = playersymbol

    def take_turn(self, board):
        if len(board.closed) == 0:
            firstmoveindex = random.randint(0, BOARD_DIMENSION ** 2 - 1)
            firstmove = board.get_available_moves()[firstmoveindex]
            board.move(firstmove)
            print("I take %d, %d" % (firstmove.x, firstmove.y))
            return

        fantasy_board = copy.deepcopy(board)

        ComputerBrain.minimax(fantasy_board, 0)

        board.move(fantasy_board.choice)
        print("I take %d, %d" % (fantasy_board.choice.x, fantasy_board.choice.y))
        return


class GameStateEvaluator(object):
    @staticmethod
    def win(board):
        non_candidate_rows = []
        non_candidate_columns = []
        diagonal_candidate = True
        reverse_diagonal_candidate = True

        if len(board.open) > 0:
            for entry in board.open:
                non_candidate_rows.append(entry.y)
                non_candidate_columns.append(entry.x)
                if (entry.x == 0 and entry.y == 0) or (
                        entry.x == BOARD_DIMENSION - 1 and entry.y == BOARD_DIMENSION - 1):
                    diagonal_candidate = False
                if (entry.x == BOARD_DIMENSION - 1 and entry.y == 0) or (
                        entry.x == 0 and entry.y == BOARD_DIMENSION - 1):
                    reverse_diagonal_candidate = False

        for y in range(BOARD_DIMENSION):
            if y not in non_candidate_rows:
                winner = GameStateEvaluator.winning_row(board, y)
                if winner != '' and winner != None:
                    return winner

        for x in range(BOARD_DIMENSION):
            if x not in non_candidate_columns:
                winner = GameStateEvaluator.winning_column(board, x)
                if winner != '' and winner != None:
                    return winner

        if diagonal_candidate:
            winner = GameStateEvaluator.winning_diagonal(board)
            if winner != '' and winner != None:
                return winner

        if reverse_diagonal_candidate:
            winner = GameStateEvaluator.winning_reverse_diagonal(board)
            if winner != '' and winner != None:
                return winner

        return

    @staticmethod
    def winning_row(board, row):
        candidate_player = board.grid[0][row]
        rowline = []
        for x in range(1, BOARD_DIMENSION):
            rowline.append(board.grid[x][row])
        return GameStateEvaluator.check_line(candidate_player, rowline)

    @staticmethod
    def winning_column(board, column):
        candidate_player = board.grid[column][0]
        columnline = []
        for y in range(1, BOARD_DIMENSION):
            columnline.append(board.grid[column][y])
        return GameStateEvaluator.check_line(candidate_player, columnline)

    @staticmethod
    def winning_diagonal(board):
        candidate_player = board.grid[0][0]
        diagonalline = []
        for x in range(1, BOARD_DIMENSION):
            diagonalline.append(board.grid[x][x])
        return GameStateEvaluator.check_line(candidate_player, diagonalline)

    @staticmethod
    def winning_reverse_diagonal(board):
        candidate_player = board.grid[0][BOARD_DIMENSION - 1]
        reversediagonalline = []
        for x in range(1, BOARD_DIMENSION):
            reversediagonalline.append(board.grid[x][BOARD_DIMENSION - 1 - x])
        return GameStateEvaluator.check_line(candidate_player, reversediagonalline)

    @staticmethod
    def check_line(candidate_player, line):
        for i in line:
            if i != candidate_player:
                return None
        else:
            return candidate_player


class ComputerBrain(object):
    @staticmethod
    def minimax(board, depth):
        if board.can_check_win and board.over == True:
            return ComputerBrain.score(board, depth)
        depth += 1
        scores = []  # an array of scores
        moves = []  # an array of moves

        # Populate the scores array, recursing as needed
        availablemoves = board.get_available_moves()
        for move in availablemoves:
            possible_game = ComputerBrain.get_new_state(board, move)
            score = ComputerBrain.minimax(possible_game, depth)
            scores.append(score)
            moves.append(move)

        # Do the min or the max calculation
        if board.active_player == COMPUTER_PLAYER_SYMBOL:
            # This is the max calculation
            max_score_index = scores.index(max(scores))
            board.choice = moves[max_score_index]
            return scores[max_score_index]
        else:
            # This is the min calculation
            min_score_index = scores.index(min(scores))
            board.choice = moves[min_score_index]
            return scores[min_score_index]

    @staticmethod
    def get_new_state(board, move):
        # new_state = copy.copy(board)
        newboard = copy.deepcopy(board)
        newboard.move(move)
        return newboard

    @staticmethod
    def score(board, depth):
        if board.win == COMPUTER_PLAYER_SYMBOL:
            return 10 - depth
        elif board.win == HUMAN_PLAYER_SYMBOL:
            return depth - 10
        else:
            return 0


class GameEngine(object):
    def __init__(self):
        return

    def start(self):
        print " WELCOME TO TIC-TAC-TOE "
        print " ========================= "
        global BOARD_DIMENSION
        BOARD_DIMENSION = int(raw_input("How large would you like your board to be? Ex: 3 creates a 3x3 board. "))
        print("Thank you, playing a %s by %s game." % (BOARD_DIMENSION, BOARD_DIMENSION))

        global MIN_WINNING_MOVES

        # the Ruby program doesn't check for a win unless there are at least 5 moves
        # I generalize this to 2*dimension - 1
        MIN_WINNING_MOVES = 2 * BOARD_DIMENSION - 1
        symbols = ["X", "O"]
        global HUMAN_PLAYER_SYMBOL
        humanplayerin = str(raw_input("Which symbol would you like to play as? Available: X or O: "))
        HUMAN_PLAYER_SYMBOL = humanplayerin.upper()
        symbols.remove(HUMAN_PLAYER_SYMBOL)

        global COMPUTER_PLAYER_SYMBOL
        COMPUTER_PLAYER_SYMBOL = symbols.pop()
        print("Human playing as %s, computer playing as %s" % (HUMAN_PLAYER_SYMBOL, COMPUTER_PLAYER_SYMBOL))

        humanplayer = HumanPlayer(HUMAN_PLAYER_SYMBOL)
        computerplayer = ComputerPlayer(COMPUTER_PLAYER_SYMBOL)

        humanfirst = raw_input("Would you like to go first? [Y or N]")
        if humanfirst.upper() == "Y":
            self.first_player = humanplayer
            self.second_player = computerplayer
        else:
            self.first_player = computerplayer
            self.second_player = humanplayer

        board = Board()
        board.create_new_board(BOARD_DIMENSION)
        board.active_player = self.first_player.symbol

        print("Game starting!")

        board.print_board()

        self.game_loop(board)
        return

    def game_loop(self, board):
        while board.over == False:
            self.first_player.take_turn(board)
            board.print_board()

            if board.over:
                self.end_sequence(board)
                return

            self.second_player.take_turn(board)
            board.print_board()

        self.end_sequence(board)

        return

    def end_sequence(self, board):
        board.print_board()
        if board.win != "" and board.win != None:
            print("The winner is: %s" % board.win)
        else:
            print("You fought the computer to a draw!")
        return


game = GameEngine()
game.start()


