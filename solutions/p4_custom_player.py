# -*- coding: utf-8 -*-
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

from assignment2 import Player, State, Action
import time

a = 0
timings = {
    'evalCalls': 0,
    'move': [0, 0, 0],
    'feel_like_thinking': [0, 0, 0],
    'do_the_magic': [0, 0, 0],
    'miniMax': [0, 0, 0],
    'minValue': [0, 0, 0],
    'maxValue': [0, 0, 0],
    'evaluate': [0, 0, 0],
    'evaluate1': [0, 0, 0],
    'evaluate2': [0, 0, 0],
    'evaluate3': [0, 0, 0],
    'evaluate4': [0, 0, 0]
}

class YourCustomPlayer(Player):
    @property
    def name(self):
        """Returns the name of this agent. Try to make it unique!"""
        return 'HAL9000'

    def move(self, state):
        """Calculates the absolute best move from the given board position using magic.
        
        Args:
            state (State): The current state of the board.

        Returns:
            your next Action instance
        """

        timeTemp = time.time()
        my_move = state.actions()[0]

        while not self.is_time_up():
            # Do some thinking here
            return self.do_the_magic(state)


        
        # Time's up, return your move
        # You should only do a small amount of work here, less than one second.
        # Otherwise a random move will be played!
        timings['move'][0] += time.time() - timeTemp
        timings['move'][1] += 1
        timings['move'][2] = 1
        return my_move

    def feel_like_thinking(self):
        
        return False
    # min( dLimit, amount of moves left)
    def do_the_magic(self, state):
        global a
        timeTemp = time.time()
        bestAction = 0
        v = 0
        for depth in range(1,6):
            action = self.miniMax(state, depth)
            result = self.evaluate(state.result(action), state.to_play.next)
            if v < result:
                v = result
                bestAction = action

        #print a
        #print bestAction

        print a
        print bestAction
        timings['do_the_magic'][0] += time.time() - timeTemp
        timings['do_the_magic'][1] += 1
        timings['do_the_magic'][2] = 10
        return bestAction

    def miniMax(self, state, dLimit):
        timeTemp = time.time()
        v = int(-999999)
        bestAction = 0
        table = {}
        i = 0
        for action in state.actions():
            #printAction(action,state.result(action))
            newState = state.result(action)
            v2 = self.minValue(newState, -999999, 999999, table , dLimit)
            if v < v2:
                if v2 is 1.0:
                    return v2
                v = v2
                bestAction = action
        #print bestAction
        timings['miniMax'][0] += time.time() - timeTemp
        timings['miniMax'][1] += 1
        timings['miniMax'][2] = len(state.actions())
        return bestAction

    # Name: minValue
    # Input: state
    # Output: integer - minValue returns a value from the utility function
    # Description:  Same as previous min value function but includes alpha/beta pruning
    #               and a transposition table.
    def minValue(self, state, alpha, beta, table, dLimit):
        timeTemp = time.time()
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
                timings['minValue'][0] += time.time() - timeTemp
                timings['minValue'][1] += 1
                timings['minValue'][2] = len(state.actions())
                return v
            beta = min(beta, v)
        timings['minValue'][0] += time.time() - timeTemp
        timings['minValue'][1] += 1
        timings['minValue'][2] = len(state.actions())
        return v

    # Name: maxValue
    # Input: state
    # Output: integer - maxValue returns a value from the utility function
    # Description:  Same as previous max value function but includes alpha/beta pruning
    #               and a transposition table.
    def maxValue(self, state, alpha, beta, table, dLimit):
        timeTemp = time.time()
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
                timings['maxValue'][0] += time.time() - timeTemp
                timings['maxValue'][1] += 1
                timings['maxValue'][2] = len(state.actions())
                return v
            alpha = max(alpha, v)
        timings['maxValue'][0] += time.time() - timeTemp
        timings['maxValue'][1] += 1
        timings['maxValue'][2] = len(state.actions())
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
            timings['evalCalls'] += 1
            f = open("timingResults.txt", 'a')
            timeTemp = time.time()
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
     
            if timings['evalCalls'] % 20 == 0:
                timings['evaluate'][0] += time.time() - timeTemp
                timings['evaluate'][1] += 1
                timings['evaluate'][2] = (4 * n*m) + m
                f.write("***"*5)
                f.write("Evaluate")
                f.write("###"*5)
                for k in timings.keys():
                    if k is not "evalCalls":
                        f.write(k + ": " + str(timings[k][0]) + " | " + str(timings[k][1]) + " | " + str(timings[k][2]))
                f.write("***"*5)

            f.close()
            return longestStreak/ float(state.K)