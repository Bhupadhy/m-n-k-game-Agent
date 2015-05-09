# -*- coding: utf-8 -*-
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

from assignment2 import Player, State, Action

a = 0 
class PlayerB(Player):
    @property
    def name(self):
        """Returns the name of this agent. Try to make it unique!"""
        return 'PlayerB'

    def move(self, state):
        """Calculates the absolute best move from the given board position using magic.
        
        Args:
            state (State): The current state of the board.

        Returns:
            your next Action instance
        """
        my_move = state.actions()[0]

        while not self.is_time_up():
            # Do some thinking here
            my_move = self.do_the_magic(state)
            return my_move


        
        # Time's up, return your move
        # You should only do a small amount of work here, less than one second.
        # Otherwise a random move will be played!
        return my_move

    def feel_like_thinking(self):
        
        return False
    # min( dLimit, amount of moves left)
    def do_the_magic(self, state):
        global a
        
        v = 0
        for depth in range(1,6):
            action = self.miniMax(state, depth)
            if self.is_time_up():
                return action

       #print a
        #print bestAction
        return action

    def miniMax(self, state, dLimit):
        v = int(-999999)
        bestAction = 0
        table = {}
        i = 0
        for action in state.actions():
            #printAction(action,state.result(action))
            newState = state.result(action)
            v2 = self.minValue(newState, -999999, 999999, table , dLimit)
            print "Action: {} \n Value: {} Value2: {}".format(action, v2, v)
            if v <= v2:
                v = v2
                bestAction = action
        print "DONE HERE best move {}".format(bestAction)
        return bestAction

    # Name: minValue
    # Input: state
    # Output: integer - minValue returns a value from the utility function
    # Description:  Same as previous min value function but includes alpha/beta pruning
    #               and a transposition table.
    def minValue(self, state, alpha, beta, table, dLimit):
        dLimit += -1
        if dLimit == 0 or self.is_time_up() or state.is_terminal():

            return self.evaluate(state, self.color)
        v = int(999999)
        for action in state.actions():
            newState = state.result(action)
            if table.has_key(hash(newState)):
                v2 = table[hash(newState)]
            else:
                v2 = self.maxValue(newState, alpha, beta, table, dLimit)
                if v2 is 1.0:
                    return v2
                table[hash(newState)] = v2
            #printCompare(v,v2,"min")
            v = min(v, v2 )
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Name: maxValue
    # Input: state
    # Output: integer - maxValue returns a value from the utility function
    # Description:  Same as previous max value function but includes alpha/beta pruning
    #               and a transposition table.
    def maxValue(self, state, alpha, beta, table, dLimit):
        dLimit += -1
        if dLimit == 0 or self.is_time_up() or state.is_terminal():

            return self.evaluate(state, self.color)
        v = int(-999999)
        for action in state.actions():
            newState = state.result(action)
            if table.has_key(hash(newState)):
                v2 = table[hash(newState)]
            else:
                v2 = self.minValue(newState, alpha, beta, table, dLimit)
                if v2 is 1.0:
                    return v2
                table[hash(newState)] = v2
            #printCompare(v,v2,"max")
            v = max(v, v2)
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    
    # Possible optimizations: If currentStreak = 0 and the position in the board
    # is at a place where it wont be able to break the longest streak just break out
    # of loop and go on to next
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
            global a
            a += 1
            longestStreak = 0
            currentStreak = 0
            m = state.M
            n = state.N
            board = state.board
            i = 0
            j = 0
            k = state.K
            # Check Vertical
            for i in range(n):
                currentStreak = 0
                for j in range(m):
                    if board[j][i] == self.color:
                        currentStreak += 1
                        longestStreak = max(longestStreak, currentStreak)
                    else:
                        currentStreak = 0

            # Check Horizontal
            for j in range(m):
                currentStreak = 0
                for i in range(n):
                    if board[j][i] == self.color:
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
                    if board[d][i] == self.color:
                        currentStreak += 1
                        longestStreak = max(longestStreak, currentStreak)
                    else:
                        currentStreak = 0
                    if d != 0:
                        d += -1
                    else:
                        break

            if longestStreak == k:
                return longestStreak/ float(state.K)
            # Check Forward Diagonal (Right Half)
            for i in range(n):
                d=i
                currentStreak = 0
                for j in reversed(range(m)):
                    if board[j][d] == self.color:
                        currentStreak += 1
                        longestStreak = max(longestStreak, currentStreak)
                    else:
                        currentStreak = 0
                    if d < n - 1:
                        d += 1
                    else:
                        break

            if longestStreak == k:
                return longestStreak/ float(state.K)
            # Check Backward Diagonal (Left Half)
            for i in reversed(range(n)):
                d=i
                currentStreak = 0
                for j in range(m):

                    if board[j][d] == self.color:
                        currentStreak += 1
                        longestStreak = max(longestStreak, currentStreak)
                    else:
                        currentStreak = 0
                    if d < n - 1:
                        d += 1
                    else:
                        break

            if longestStreak == k:
                return longestStreak/ float(state.K)

            # Check Backward Diagonal (Right Half)
            for i in reversed(range(n)):
                d=i
                currentStreak = 0
                for j in range(m):
                    if board[j][d] == self.color:
                        currentStreak += 1
                        longestStreak = max(longestStreak, currentStreak)
                    else:
                        currentStreak = 0
                    if d != 0:
                        d += -1
                    else:
                        break
            return longestStreak/ float(state.K)