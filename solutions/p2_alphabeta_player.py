# -*- coding: utf-8 -*-
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

from assignment2 import Player, State, Action

class AlphaBetaPlayer(Player):
    def move(self, state):
        """Calculates the best move from the given board using the minimax algorithm with alpha-beta pruning.

        Args:
            state (State): The current state of the board.

        Returns:
            the next move (Action)
        """

        # TODO implement this
        return miniMax(state)

# Debugging : Prints action i.e. "Player 1 played at (1,0)"
def printAction(action,state):
    print "*****" * 5
    print action
    print "*****" * 5
    print state.to_play

# Debugging : prints -
#                       Utility value of leaf node
#                       Whos turn it is
#                       State of the board
def printUtility(state):
    print "*" * 5
    print "Utility"
    print int(state.utility(state.to_play.next))
    print state.to_play
    print state
    print "*" * 5

# Debugging : prints the two values that are being compared in min and max
def printCompare(v,v2, comparator):
    print "{} {} {}".format(v,comparator,v2)


# Name: miniMax
# Input: state
# Output: Action object - returns the best action to take on the board according
#                         to miniMax algorithm.
# Description: Same as previous miniMax function but uses a transposition table
#				to keep track of states that have already been seen and replaces
#				call to the function with the value that would have returned.
#				Also includes alpha beta pruning which keeps a tab on the highest
#				max utility found and the lowest min utility and if the search
#				finds a v such that it is less than the alpha value in the min
#				function then returns that v. Vice versa for beta value
def miniMax(state):
    v = int(-999999)
    bestAction = 0
    table = {}
    for action in state.actions():
        #printAction(action,state.result(action))
        newState = state.result(action)
        v2 = minValue(newState, -999999, 999999, table)
        if v < v2:
            v = v2
            bestAction = action
    #print bestAction
    return bestAction

# Name: minValue
# Input: state
# Output: integer - minValue returns a value from the utility function
# Description:  Same as previous min value function but includes alpha/beta pruning
#				and a transposition table.
def minValue(state, alpha, beta, table):
    if state.is_terminal():
        #printUtility(state)
        return int(state.utility(state.to_play.next))
    v = int(999999)
    for action in state.actions():
    	newState = state.result(action)
    	if table.has_key(hash(newState)):
    		v2 = table[hash(newState)]
    	else:
        	v2 = maxValue(newState, alpha, beta, table)
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
#				and a transposition table.
def maxValue(state, alpha, beta, table):
    if state.is_terminal():
        #printUtility(state)
        return int(state.utility(state.to_play))
    v = int(-999999)
    for action in state.actions():
    	newState = state.result(action)
    	if table.has_key(hash(newState)):
    		v2 = table[hash(newState)]
    	else:
        	v2 = minValue(newState, alpha, beta, table)
        	table[hash(newState)] = v2
        #printCompare(v,v2,"max")
        v = max(v, v2)
        if v >= beta:
        	return v
        alpha = max(alpha, v)
    return v

