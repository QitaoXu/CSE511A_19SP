# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    # print "new pacman position: ", newPos
    # print "newFood: ", newFood
    # print "newGhostStates.configuration.position: ", newGhostStates[0].configuration.getPosition()
    # print "newScaredTimes: ", newScaredTimes
    # currentDistances = []
    # currentGhostStates = currentGameState.getGhostStates()
    # for currentGhostState in currentGhostStates:
    #   currentGhostPosition = currentGhostState.configuration.getPosition()
    #   currentPacmanPosition = currentGameState.getPacmanPosition()
    #   currentDistances.append(util.manhattanDistance(currentGhostPosition, currentPacmanPosiztion))

    score = successorGameState.getScore()
    newDistances = []
    # newGhostPositions = []
    for newGhostState in newGhostStates:
      newGhostPosition = newGhostState.configuration.getPosition()
      newDistances.append(util.manhattanDistance(newGhostPosition, newPos))
    if min(newDistances) < 2 and newScaredTimes[0] < 2:
      score -= 50
    
    if currentGameState.getScore() >= successorGameState.getScore():
      score -= 150

    if min(newDistances) < 1 and newScaredTimes[0] > 1:
      score += 50

    if currentGameState.getPacmanPosition() == successorGameState.getPacmanPosition():
      score -= 75
    
    
    
    return score
    # return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    # print "depth: ", self.depth
    def maxValue( gameState, depth ):
      v = -9999999 # initialize v to minus infinity
      lastGhostIndex = gameState.getNumAgents() - 1
      if depth == 0: # fringe
        return self.evaluationFunction(gameState)

      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

      successorGameStates = []
      for action in gameState.getLegalActions(0):
        successorGameStates.append(gameState.generateSuccessor(0, action))

      for successorGameState in successorGameStates:
        v = max( v, minValue(successorGameState, depth, lastGhostIndex) )
      
      return v

    def minValue( gameState, depth, ghostIndex ):
      v = 9999999 # initialize v to infinity

      if depth == 0: # terminal state or fringe
        return self.evaluationFunction(gameState)
      
      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

      successorGameStates = []
      for action in gameState.getLegalActions(ghostIndex):
        successorGameStates.append(gameState.generateSuccessor(ghostIndex, action))
      
      for successorGameState in successorGameStates:
        if (ghostIndex - 1) > 0: # at least one ghost has not moved in current depth level
          v = min( v, minValue(successorGameState, depth, ghostIndex - 1) )
        if (ghostIndex - 1) == 0: # all ghosts have moved in current depth level
          v = min( v, maxValue(successorGameState, depth -1) )
      
      return v
          
    max_action = Directions.STOP
    max_value = -9999999
    if gameState.isLose() or gameState.isWin():
      return max_action
    
    lastGhostIndex = gameState.getNumAgents() - 1

    # to find max_action among all actions pacman can choose 
    # such that it can get max value in worst case
    # after first action
    # 
    for action in gameState.getLegalActions(0):

      if action == Directions.STOP:
        continue

      successorGameState = gameState.generateSuccessor(0, action)
      v = minValue( successorGameState, self.depth, lastGhostIndex)
      if max_value < v:
        max_value = v
        max_action = action

    return max_action

    # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    def maxValue(gameState, alpha, beta, depth):
      if depth == 0:
        return self.evaluationFunction(gameState)

      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

      v = -9999999
      
      successorGameStates = []
      for action in gameState.getLegalActions(0):
        successorGameStates.append(gameState.generateSuccessor(0, action))

      for successorGameState in successorGameStates:
        v = max(v, miniValue(successorGameState, alpha, beta, depth, gameState.getNumAgents() -1))
        alpha = max(alpha, v)
        if alpha >= beta: # pruning
          return v
      return v

    def miniValue(gameState, alpha, beta, depth, ghostIndex):
      if depth == 0:
        return self.evaluationFunction(gameState)
      
      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

      v = 9999999
      
      successorGameStates = []
      for action in gameState.getLegalActions(ghostIndex):
        successorGameStates.append(gameState.generateSuccessor(ghostIndex, action))
      
      for successorGameState in successorGameStates:
        if (ghostIndex - 1) > 0:
          v = min(v, miniValue(successorGameState, alpha, beta, depth, ghostIndex - 1))
        if (ghostIndex - 1) == 0:
          v = min(v, maxValue(successorGameState, alpha, beta, depth - 1))
        beta = min(beta, v)
        if alpha >= beta: # pruning
          return v
      return v

    # max_value = -9999999
    max_action = Directions.STOP
    alpha = -9999999
    beta = 9999999

    if gameState.isWin() or gameState.isLose():
      return max_action
     
    lastGhostIndex = gameState.getNumAgents() - 1

    for action in gameState.getLegalActions(0):
      if action  == Directions.STOP:
        continue 
      
      successorGameState = gameState.generateSuccessor(0, action)
      v = miniValue(successorGameState, alpha, beta, self.depth, lastGhostIndex)
      if alpha < v:
        alpha = v
        max_action = action
    
    return max_action


    # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    def maxValue(gameState, depth):
      if depth == 0:
        return self.evaluationFunction(gameState)
      
      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

      v = -9999999
      lastGhostIndex = gameState.getNumAgents() - 1
      
      successorGameStates = []
      for action in gameState.getLegalActions(0):
        successorGameStates.append(gameState.generateSuccessor(0, action))

      for successorGameState in successorGameStates:
        v = max(v, expValue(successorGameState, depth, lastGhostIndex))
      return v

    
    def expValue(gameState, depth, ghostIndex):
      if depth == 0:
        return self.evaluationFunction(gameState)

      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      
      v = 0
      successorGameStates = []
      for action in gameState.getLegalActions(ghostIndex):
        successorGameStates.append(gameState.generateSuccessor(ghostIndex, action))

      p = 1.0 / len(successorGameStates)
      for successorGameState in successorGameStates:
        if (ghostIndex - 1) > 0:
          v = v + p * expValue(successorGameState, depth, ghostIndex - 1)
        if (ghostIndex - 1) == 0:
          v = v + p * maxValue(successorGameState, depth - 1)
      return v

    max_value = -9999999
    max_action = Directions.STOP
    v = -9999999
    lastGhostIndex = gameState.getNumAgents() - 1

    if gameState.isLose() or gameState.isWin():
      return max_action
    
    for action in gameState.getLegalActions(0):

      if action == Directions.STOP:
        continue

      successorGameState = gameState.generateSuccessor(0, action)
      v = max(v, expValue(successorGameState, self.depth, lastGhostIndex))
      if (max_value < v):
        max_value = v
        max_action = action

    return max_action
    # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    The constant values are found by testing it with various values and 
    seeing the results to find the best values for the best avg score.
    Ghost distance is calculated and pacman made to move away 
    when it is 2 spaces away. It will eat the Big pellet when ghost is 2 spaces near it.
  """
  "*** YOUR CODE HERE ***"
  pacPosition = currentGameState.getPacmanPosition()
  food = currentGameState.getFood()
  foodList = food.asList()
  foodDistance = 0

  # Food utility calculation
  for dot in foodList:
    foodDistance += manhattanDistance(pacPosition, dot)

  # Ghost distance utility calculation
  ghostDistance = 0
  for ghost in currentGameState.getGhostPositions():
    dist = max( 4.315 - manhattanDistance(pacPosition, ghost), 0)
    ghostDistance += dist**2
  # return utility score of state

  return currentGameState.getScore() - foodDistance - ghostDistance
  # util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

