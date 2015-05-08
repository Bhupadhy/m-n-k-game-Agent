# -*- coding: utf-8 -*-
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

import heapq

from assignment2 import Player


class EvaluationPlayer(Player):
    def move(self, state):
        """Calculates the best move after 1-ply look-ahead with a simple evaluation function.

        Args:
            state (State): The current state of the board.

        Returns:
            the next move (Action)
        """

        # *You do not need to modify this method.*
        best_move = None
        max_value = -1.0
        my_color = state.to_play.color

        for action in state.actions():
            if self.is_time_up():
                break

            result_state = state.result(action)
            value = self.evaluate(result_state, my_color)
            if value > max_value:
                max_value = value
                best_move = action

        # Return the move with the highest evaluation value
        return best_move

    # def evaluate(self, state, color):
    #     longestStreak = 0
    #     currentStreak = 0
    #     m = state.M
    #     n = state.N
    #     board = state.board
    #     for i in range(m):
    #         for j in range(n):
    #             if board[i][j] == self.color and currentStreak == 0:
    #                 currentStreak = 1
    #             elif board[i][j] == self.color and currentStreak >= 1:
    #                 currentStreak += 1
    #                 longestStreak = max(longestStreak, currentStreak)
    #             elif

    #     return 0.0
    def evaluate(self, state, color):
        """Evaluates the state for the player with the given stone color.

        This function calculates the length of the longest ``streak'' on the board
        (of the given stone color) divided by K.  Since the longest streak you can
        achieve is K, the value returned will be in range [1 / state.K, 1.0].
        Args:
            state (State): The state instance for the current board.
            color (int): The color of the stone for which to calculate the streaks.

        Returns:
            the evaluation value (float), from 1.0 / state.K (worst) to 1.0 (win).
        """

        longestStreak = 0
        currentStreak = 0
        m = state.M
        n = state.N
        board = state.board
        i = 0
        j = 0

        # Check Vertical
        for i in range(n):
            currentStreak = 0
            for j in range(m):
                if board[j][i] == color:
                    currentStreak += 1
                    longestStreak = max(longestStreak, currentStreak)
                else:
                    currentStreak = 0

        # Check Horizontal
        for j in range(m):
            currentStreak = 0
            for i in range(n):
                if board[j][i] == color:
                    currentStreak += 1
                    longestStreak = max(longestStreak, currentStreak)
                else:
                    currentStreak = 0

        # Check Forward Diagonal (Left Half)
        for j in range(m):
            #print "{} {}".format("Diagonal", j)
            d = j
            currentStreak = 0
            for i in range(j + 1):
                if i > n - 1:
                    break
                #print "i{} j{} board{}".format(i, d, board[d][i])
                if board[d][i] == color:
                    currentStreak += 1
                    longestStreak = max(longestStreak, currentStreak)
                else:
                    currentStreak = 0
                if d != 0:
                    d += -1

        # Check Forward Diagonal (Right Half)
        for i in range(n):
            d=i
            currentStreak = 0
            for j in reversed(range(m)):
                if board[j][d] == color:
                    currentStreak += 1
                    longestStreak = max(longestStreak, currentStreak)
                else:
                    currentStreak = 0
                if d < n - 1:
                    d += 1
                else:
                    break


        # Check Backward Diagonal (Left Half)
        for i in reversed(range(n)):
            d=i
            currentStreak = 0
            for j in range(m):

                if board[j][d] == color:
                    currentStreak += 1
                    longestStreak = max(longestStreak, currentStreak)
                else:
                    currentStreak = 0
                if d < n - 1:
                    d += 1
                else:
                    break

        # Check Backward Diagonal (Right Half)
        for i in range(n):
            d=i
            currentStreak = 0
            for j in range(m):
                if board[d][j] == color:
                    currentStreak += 1
                    longestStreak = max(longestStreak, currentStreak)
                else:
                    currentStreak = 0
                if d < n - 1:
                    d += 1
                else:
                    break
 


        return longestStreak/ float(state.K)

