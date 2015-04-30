# -*- coding: utf-8 -*-
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

from assignment2 import Player, State, Action

class MinimaxPlayer(Player):

    def move(self, state):
        """Calculates the best move from the given board using the minimax algorithm.

        Args:
            state (State): The current state of the board.

        Returns:
            the next move (Action)
        """
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
# Description: Takes the current state of the board and for each legal action that
#               can be taken on the state, calls minValue on the result of that
#               action. After minValue returns from all recursions miniMax takes
#               the highest value action from the set of actions that can be taken
#               on the board. By doing this a game tree will be created until either
#               min or max functions reach a leaf node. Then the utility of that leaf
#               will be determined for the player and traverse the tree back to the root
#               doing min/max comparisons for whichever function it is in.
def miniMax(state):
    v = int(-999999)
    bestAction = 0
    for action in state.actions():
        #printAction(action,state.result(action))
        v2 = minValue(state.result(action))
        if v < v2:
            v = v2
            bestAction = action
    #print bestAction
    return bestAction

# Name: minValue
# Input: state
# Output: integer - minValue returns a value from the utility function
# Description:  Takes the current state of the board. If it is a terminal state...
#               i.e. it is winnable by either or player or it is a draw for both
#               players, returns the value from a utility function which determines
#               the value of the state of the board for the player that is passed in.
#               In cases where the state is not terminal, minValue, for each action
#               that can be taken on the current state of the board, calls function
#               maxValue then takes the min utility of all the actions that are returned
#               from maxValue and returns that value.
def minValue(state):
    if state.is_terminal():
        #printUtility(state)
        return int(state.utility(state.to_play.next))
    v = int(999999)
    for action in state.actions():
        v2 = maxValue(state.result(action))
        #printCompare(v,v2,"min")
        v = min(v, v2 )
    return v

# Name: maxValue
# Input: state
# Output: integer - maxValue returns a value from the utility function
# Description:  Takes the current state of the board. If it is a terminal state...
#               i.e. it is winnable by either or player or it is a draw for both
#               players, returns the value from a utility function which determines
#               the value of the state of the board for the player that is passed in.
#               In cases where the state is not terminal, maxValue, for each action
#               that can be taken on the current state of the board, calls function
#               minValue then takes the max utility of all the actions that are returned
#               from minValue and returns that value.
def maxValue(state):
    if state.is_terminal():
        #printUtility(state)
        return int(state.utility(state.to_play))
    v = int(-999999)
    for action in state.actions():
        v2 = minValue(state.result(action))
        #printCompare(v,v2,"max")
        v = max(v, v2)
    return v