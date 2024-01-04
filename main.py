import random
import time
import numpy as np
import random
import sys
import math
import pprint

HORIZONTAL = 0
VERTICAL = 1
AI = 1
PLAYER = 0


class Ai:
    def __init__(self, shape):
        self.shape = shape
        self.X = shape[0]
        self.Y = shape[1]
        self.state = [[[0, 0] for _ in range(self.Y)] for _ in range(self.X)]
        self.score = 0
        self.line_drawn = 0

    def decide(self, state):
        # decide based on the state
        return (0, 0), (1, 0)

    def draw_line(self, x, y, direction):
        if self.state[x][y][direction] != 0:
            return False
        self.state[x][y][direction] = 1
        self.line_drawn += 1
        return True

    def undo_move(self, x, y, direction):
        self.line_drawn -= 1

        self.state[x][y][direction] = 0

    def print_board(self):
        for i in range(self.X):
            for j in range(self.Y):
                print(". ", end="")
                if self.state[i][j][HORIZONTAL] == 1:
                    print("_", end="")
                else:
                    print(" ", end="")
            print()

            for j in range(self.Y):
                if self.state[i][j][1] == VERTICAL:
                    print("|  ", end="")
                else:
                    print("   ", end="")
            print()
        print()

    def valid_actions(self):
        valids_list = []
        for i in range(self.X):
            for j in range(self.Y):
                if self.state[i][j][HORIZONTAL] == 0 and i < self.X - 1:
                    valids_list.append((i, j, HORIZONTAL))
                if self.state[i][j][VERTICAL] == 0 and j < self.Y - 1:
                    valids_list.append((i, j, VERTICAL))
        return valids_list

    def has_won(self):
        return self.line_drawn == (self.X - 1) * (self.Y - 1)

    def minimax(self, depth, maximizingPlayer):
        if depth == 0 or self.has_won():
            return None, self.calculate_heuristic()

        valid_actions = self.valid_actions()
        if maximizingPlayer:
            max_eval = float('-inf')
            max_action = None
            for action in valid_actions:
                x, y, direction = action
                self.draw_line(x, y, direction)
                if self.check_completed_boxes(x, y, direction):
                    self.score += self.check_completed_boxes(x, y, direction)
                    _, eval_score = self.minimax(depth - 1, True)
                else:
                    _, eval_score = self.minimax(depth - 1, False)
                if self.check_completed_boxes(x, y, direction):
                    self.score -= self.check_completed_boxes(x, y, direction)
                self.undo_move(x, y, direction)
                if eval_score > max_eval:
                    max_eval = eval_score
                    max_action = action
            return max_action, max_eval

        else:
            min_eval = float('inf')
            min_action = None
            for action in valid_actions:
                x, y, direction = action
                self.draw_line(x, y, direction)
                if self.check_completed_boxes(x, y, direction):
                    self.score -= self.check_completed_boxes(x, y, direction)
                    _, eval_score = self.minimax(depth - 1, False)

                else:
                    _, eval_score = self.minimax(depth - 1, True)
                if self.check_completed_boxes(x, y, direction):
                    self.score += self.check_completed_boxes(x, y, direction)
                self.undo_move(x, y, direction)
                if eval_score < min_eval:
                    min_eval = eval_score
                    min_action = action
            return min_action, min_eval

    def check_completed_boxes(self, x, y, direction):
        completed_boxes = 0

        if direction == HORIZONTAL:
            if x > 0 and self.state[x - 1][y][HORIZONTAL] == 1 and self.state[x - 1][y][VERTICAL] == 1 and \
                    self.state[x - 1][y + 1][VERTICAL] == 1:
                completed_boxes += 1
            if x < self.X - 1 and self.state[x][y][HORIZONTAL] == 1 and self.state[x][y][VERTICAL] == 1 and \
                    self.state[x][y + 1][VERTICAL] == 1:
                completed_boxes += 1
        elif direction == VERTICAL:
            if y > 0 and self.state[x][y - 1][HORIZONTAL] == 1 and self.state[x + 1][y - 1][HORIZONTAL] == 1 and \
                    self.state[x][y - 1][VERTICAL] == 1:
                completed_boxes += 1
            if y < self.Y - 1 and self.state[x][y][HORIZONTAL] == 1 and self.state[x + 1][y][HORIZONTAL] == 1 and \
                    self.state[x][y][VERTICAL] == 1:
                completed_boxes += 1

        return completed_boxes

    def calculate_heuristic(self):
        heuristic_value = self.score * 10
        heuristic_value += len(self.valid_actions())
        return heuristic_value

    def play_and_show(self):
        turn = 0
        over = False
        self.print_board()
        print("_________________________________")

        while not over:

            if turn == PLAYER:
                played_x, played_y, played_dir = [int(i) for i in input().split()]
                self.draw_line(played_x, played_y, played_dir)
                self.print_board()
                self.line_drawn += 1
                self.score -= self.check_completed_boxes(played_x, played_y, played_dir)
                if self.check_completed_boxes(played_x, played_y, played_dir) > 0:
                    turn = PLAYER
                else:
                    turn = AI
                if self.line_drawn == (self.Y - 1) * (self.Y - 1):
                    print(self.score)
                    over = True
            else:
                played_action, played_score = self.minimax(2, True)
                played_x, played_y, played_dir = played_action
                self.draw_line(played_x, played_y, played_dir)
                self.print_board()
                self.line_drawn += 1
                self.score += self.check_completed_boxes(played_x, played_y, played_dir)
                if self.check_completed_boxes(played_x, played_y, played_dir) > 0:
                    turn = AI
                else:
                    turn = PLAYER
                if self.line_drawn == (self.Y - 1) * (self.Y - 1):
                    print(self.score)
                    over = True
            print(played_x, played_y, played_dir)
            print(self.score)
            print(self.line_drawn)
            print(turn)
            print("_________________________________")


ai_instance = Ai((3, 3))

ai_instance.play_and_show()
