# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import time

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    startPosition = problem.getStartState()
    searchStack = util.Stack()
    ancestors = set()
    searchStack.push( (startPosition, []) )

    while searchStack.isEmpty() == False:
        current, actions = searchStack.pop()
        if problem.isGoalState(current):
            # print "Actions: ", actions
            return actions
        ancestors.add(current)
        for nextPosition, action, cost in problem.getSuccessors(current):
            if nextPosition not in ancestors:
                updated_actions = actions + [action]
                searchStack.push( (nextPosition, updated_actions) )
                
    return []

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    startPosition = problem.getStartState()
    # print "startPosition: ", startPosition
    searchQueue = util.Queue()
    ancestors = set()
    searchQueue.push( (startPosition, []) )
    expanded = set()
    expanded.add(startPosition)

    while searchQueue.isEmpty() == False:
        current, actions = searchQueue.pop()
        
        if problem.isGoalState(current): 
            return actions
        ancestors.add(current)
        expanded.remove(current)
        for nextPosition, action, cost in problem.getSuccessors(current):
            if nextPosition not in ancestors and nextPosition not in expanded:
                updated_actions = actions + [action]
                searchQueue.push( (nextPosition, updated_actions) )
                expanded.add(nextPosition)
    
    return []
    # util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    startPosition = problem.getStartState()
    # print "startPosition: ", startPosition
    searchPriorityQueue = util.PriorityQueue()
    ancestors = set()
    searchPriorityQueue.push( (startPosition, [], 0), 0 )

    while searchPriorityQueue.isEmpty() == False:
        current, actions, costs = searchPriorityQueue.pop()
        # print "current", current
        if problem.isGoalState(current):
            return actions
        ancestors.add(current)
        for nextPosition, action, cost in problem.getSuccessors(current):
            if nextPosition not in ancestors:
                updated_actions = actions + [action]
                updated_costs = costs + cost
                searchPriorityQueue.push( (nextPosition, updated_actions, updated_costs), updated_costs )
    
    return []
    # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    startPosition = problem.getStartState()
    searchPriorityQueue = util.PriorityQueue()
    ancestors = set()
    searchPriorityQueue.push( (startPosition, [], 0, heuristic(startPosition, problem)), 0 + heuristic(startPosition, problem))
    # print "hcost", heuristic(startPosition, problem)

    while searchPriorityQueue.isEmpty() == False:
        current, actions, gcost, hcost = searchPriorityQueue.pop()
        # print " pop:", (current, actions, gcost, hcost)
        if problem.isGoalState(current):
            return actions
        ancestors.add(current)
        for nextPosition, action, cost in problem.getSuccessors(current):
            if nextPosition not in ancestors:
                updated_actions = actions + [action]
                updated_gcost = gcost + cost
                updated_hcost = heuristic(current, problem)
                updated_costs = updated_gcost + updated_hcost
                searchPriorityQueue.push( (nextPosition, updated_actions, updated_gcost, updated_hcost),  updated_costs )
    
    return []
    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
