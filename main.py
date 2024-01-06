import random
import time
import numpy as np
import sys
import math
import pprint

HORIZONTAL = 0
VERTICAL = 1
AI = 1
PLAYER = 0


class Ai:
    def __init__(self, shape, minimax_depth):
        self.shape = shape
        self.X = shape[0]
        self.Y = shape[1]
        self.state = [[[0, 0] for _ in range(self.Y)] for _ in range(self.X)]
        self.score = 0
        self.line_drawn = 0
        self.minimax_depth = minimax_depth
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
        # print(self.state)
        for j in range(self.Y):
            for i in range(self.X):
                print(". ", end="")
                if self.state[i][j][HORIZONTAL] == 1:
                    print("_", end="")
                else:
                    print(" ", end="")
            print()

            for i in range(self.X):
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
        return self.line_drawn == self.X * (self.Y - 1) + (self.X - 1) * self.Y

    def minimax(self, depth, maximizingPlayer, alpha , beta):
        if depth == 0 or self.has_won():
            return None, self.calculate_heuristic()

        valid_actions = self.valid_actions()
        if maximizingPlayer:
            max_eval = float('-inf')
            max_action = None
            for action in valid_actions:
                x, y, direction = action
                self.draw_line(x, y, direction)
                if self.check_completed_boxes(x, y, direction) > 0:

                    self.score += self.check_completed_boxes(x, y, direction)
                    _, eval_score = self.minimax(depth - 1, True,alpha,beta)
                else:
                    _, eval_score = self.minimax(depth - 1, False,alpha,beta)

                if self.check_completed_boxes(x, y, direction) > 0:
                    self.score -= self.check_completed_boxes(x, y, direction)

                self.undo_move(x, y, direction)


                if eval_score > max_eval:
                    max_eval = eval_score
                    max_action = action
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break  # Prune the remaining branches
            return max_action, max_eval

        else:
            min_eval = float('inf')
            min_action = None
            for action in valid_actions:
                x, y, direction = action
                self.draw_line(x, y, direction)
                if self.check_completed_boxes(x, y, direction):
                    self.score -= self.check_completed_boxes(x, y, direction)
                    _, eval_score = self.minimax(depth - 1, False,alpha,beta)

                else:
                    _, eval_score = self.minimax(depth - 1, True,alpha,beta)
                if self.check_completed_boxes(x, y, direction):
                    self.score += self.check_completed_boxes(x, y, direction)
                self.undo_move(x, y, direction)

                if eval_score < min_eval:
                    min_eval = eval_score
                    min_action = action
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_action, min_eval

    def check_completed_boxes(self, x, y, direction):
        completed_boxes = 0

        if direction == VERTICAL:
            if x > 0 and self.state[x - 1][y][HORIZONTAL] == 1 and self.state[x - 1][y][VERTICAL] == 1 and \
                    self.state[x - 1][y + 1][HORIZONTAL] == 1:
                completed_boxes += 1
            if x < self.X - 1 and self.state[x][y][HORIZONTAL] == 1 and self.state[x+1][y][VERTICAL] == 1 and \
                    self.state[x][y + 1][HORIZONTAL] == 1:
                completed_boxes += 1
        elif direction == HORIZONTAL:
            if y > 0 and self.state[x][y - 1][HORIZONTAL] == 1 and self.state[x][y-1][VERTICAL] == 1 and \
                    self.state[x + 1][y - 1][VERTICAL] == 1:
                completed_boxes += 1
            if y < self.Y - 1 and self.state[x][y + 1][HORIZONTAL] == 1 and self.state[x + 1][y][VERTICAL] == 1 and \
                    self.state[x][y][VERTICAL] == 1:
                completed_boxes += 1

        return completed_boxes

    def calculate_heuristic(self):
        heuristic_value = self.score * 100
        heuristic_value += len(self.valid_actions())
        return heuristic_value

    def play_and_show(self):
        turn = 0
        over = False
        self.print_board()
        print("_________________________________")

        while not over:
            print(turn)

            if turn == PLAYER:
                # played_x, played_y, played_dir = [int(i) for i in input().split()]
                valid_list = self.valid_actions()
                randind = random.randint(0,len(valid_list) -1)
                played_x, played_y, played_dir = valid_list[randind]
                # print(valid_list)
                # print(valid_list[randind])
                self.draw_line(played_x, played_y, played_dir)
                self.print_board()
                self.score -= self.check_completed_boxes(played_x, played_y, played_dir)
                if self.check_completed_boxes(played_x, played_y, played_dir) > 0:
                    turn = PLAYER
                    print("got one")
                else:
                    turn = AI
                if self.line_drawn == self.X * (self.Y - 1) + (self.X - 1) * self.Y:
                    # print(self.score)
                    over = True
            else:
                start_time = time.time()

                played_action, played_score = self.minimax(self.minimax_depth, True,float('-inf'),float('inf'))
                elapsed_time = time.time() - start_time

                played_x, played_y, played_dir = played_action
                self.draw_line(played_x, played_y, played_dir)
                self.print_board()
                self.score += self.check_completed_boxes(played_x, played_y, played_dir)
                if self.check_completed_boxes(played_x, played_y, played_dir) > 0:
                    turn = AI
                    # print("BOOOO")
                else:
                    turn = PLAYER
                if self.line_drawn == self.X * (self.Y - 1) + (self.X - 1) * self.Y:
                    # print(self.score)
                    over = True
            print("Move: ",played_x, played_y, played_dir)
            print("Completed boxes: ",self.check_completed_boxes(played_x, played_y, played_dir))
            print("Score Diff: ",self.score)
            print("Total Line Drawn: ",self.line_drawn)
            print("_________________________________")

x = Ai((5,5),5)
x.play_and_show()