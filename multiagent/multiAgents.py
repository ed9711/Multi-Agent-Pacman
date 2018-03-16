# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        result = 0
        if successorGameState.isWin():
            # take this move
            return 999999

        if successorGameState.getScore() > currentGameState.getScore():
            # this move is good
            result += 100
        ghostPosition = successorGameState.getGhostPosition(1)

        food = newFood.asList()

        closest = 99999
        for f in food:
            distance = (manhattanDistance(f, newPos))
            if distance < closest:
                closest = distance
        # the closer the food the better the move
        result -= closest
        if newPos == ghostPosition and newScaredTimes[0] == 0:
            # do not take this move ever
            result = -999999
        if action == 'Stop':
            # do not take this move
            result = -111111
        return result


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        result = []
        action = []
        for s in gameState.getLegalActions(0):
            result.append(self.minimax(gameState.generateSuccessor(0, s), 0, 1))
            action.append(s)
        return action[result.index(max(result))]

    def minimax(self, state, depth, agent):

        num = state.getNumAgents()

        if agent == num:
            # Is player go back to 0, change depth
            return self.minimax(state, depth + 1, 0)
        legalMoves = state.getLegalActions(agent)

        if state.isLose() or state.isWin() or depth == self.depth or len(legalMoves) == 0:
            return self.evaluationFunction(state)
        # loop through agents
        values = [self.minimax(state.generateSuccessor(agent, a), depth, agent + 1) for a in legalMoves]

        if agent == 0:
            # Is player
            return max(values)
        else:
            return min(values)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        # result = []
        # action = []
        # alpha = -999999
        # beta = 999999
        # for s in gameState.getLegalActions(0):
        #     result.append(self.maxValue(gameState.generateSuccessor(0, s), 0, 0, alpha, beta))
        #     action.append(s)
        # return action[result.index(max(result))]
        alpha = -999999
        beta = 999999
        return self.maxValue(gameState, 0, 0, alpha, beta)[1]

    # def alphaBeta(self, state, depth, agent, alpha, beta):
    # "might work, but don't have time to fix this one, seems to look better"
    #     num = state.getNumAgents()
    #
    #     if agent == num:
    #         # Is player go back to 0
    #         return self.alphaBeta(state, 0, depth + 1, alpha, beta)
    #
    #     if state.isLose() or state.isWin() or depth == self.depth or len(state.getLegalActions(agent)) == 0:
    #         return self.evaluationFunction(state)
    #
    #     for a in state.getLegalActions(agent):
    #         v = self.alphaBeta(state.generateSuccessor(agent, a), depth, agent + 1, alpha, beta)
    #
        #     if agent == 0:
        #         # Is player
        #         if v >= beta:
        #             return v, a
        #         alpha = max(alpha, v)
        #         return v, a
        #     else:
        #         if v <= alpha:
        #             return v, a
        #         beta = min(beta, v)
        #         return v, a

    def maxValue(self, state, agent, depth, alpha, beta):
        legalMoves = state.getLegalActions(agent)
        if state.isLose() or state.isWin() or depth == self.depth or len(legalMoves) == 0:
            return [self.evaluationFunction(state), None]

        v = -999999
        action = None
        for a in legalMoves:
            value = self.minValue(state.generateSuccessor(agent, a), agent + 1, depth, alpha, beta)
            if value[0] > v:
                v = value[0]
                action = a
            if v >= beta:
                # prune
                return [v, action]
            alpha = max(alpha, v)
        return [v, action]

    def minValue(self, state, agent, depth, alpha, beta):
        legalMoves = state.getLegalActions(agent)
        num = state.getNumAgents()
        if state.isLose() or state.isWin() or depth == self.depth or len(legalMoves) == 0:
            return [self.evaluationFunction(state), None]
        v = 999999
        action = None
        for a in legalMoves:
            if agent == num - 1:
                # Is player go back to 0
                value = self.maxValue(state.generateSuccessor(agent, a), 0, depth + 1, alpha, beta)
            else:
                value = self.minValue(state.generateSuccessor(agent, a), agent + 1, depth, alpha, beta)
            if value[0] < v:
                v = value[0]
                action = a
            if v <= alpha:
                # prune
                return [v, action]
            beta = min(beta, v)
        return [v, action]


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
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
