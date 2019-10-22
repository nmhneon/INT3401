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
        eat=[manhattanDistance(newPos,food) for food in newFood.asList()]
        eaten=0
        for i in eat:
          if i<=4:
            eaten+=1
          elif i<=10:
            eaten+=0.45
          elif i<=16:
            eaten+=0.35
          else:
            eaten+=0.3
        scared=[[ghostState.scaredTimer,manhattanDistance(newPos,ghostState.getPosition())] for ghostState in newGhostStates]
        near=0
        for i in scared:
          if i[1]==0:
            if i[0]>0:
              near+=5
            else:
              near-=2
          elif i[1]<=4:
            if i[0]-i[1]>1:
              near+=2
            else:
              near-=1
        
        return successorGameState.getScore()+eaten+near

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

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        
        def max_value(gameState,depth):
          actions=gameState.getLegalActions(0)
          if len(actions)==0 or depth==self.depth or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState),0)
          maxValue=-(float("inf"))
          action=0

          for act in actions:
            successorValue=min_value(gameState.generateSuccessor(0,act),1,depth)
            if successorValue[0]>maxValue:
              maxValue,action=successorValue[0],act
          return (maxValue,action)
        
        def min_value(gameState,agentIndex,depth):
          actions=gameState.getLegalActions(agentIndex)
          if len(actions)==0:
            return (self.evaluationFunction(gameState),0)
          minValue=(float("inf"))
          action=0

          for act in actions:
            if(agentIndex==gameState.getNumAgents()-1):
              successorValue=max_value(gameState.generateSuccessor(agentIndex,act),depth+1)
            else:
              successorValue=min_value(gameState.generateSuccessor(agentIndex,act),agentIndex+1,depth)
            if successorValue[0]<minValue:
              minValue,action=successorValue[0],act
          return (minValue,action)
        max_value=max_value(gameState,0)[1]
        return max_value
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState,depth,a,b):
          actions=gameState.getLegalActions(0)
          if len(actions)==0 or depth==self.depth or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState),0)
          maxValue=-(float("inf"))
          action=0

          for act in actions:
            successorValue=min_value(gameState.generateSuccessor(0,act),1,depth,a,b)
            if successorValue[0]>maxValue:
              maxValue,action=successorValue[0],act
            if maxValue>b:
              return (maxValue,action)
            a=max(a,maxValue)
          return (maxValue,action)
        
        def min_value(gameState,agentIndex,depth,a,b):
          actions=gameState.getLegalActions(agentIndex)
          if len(actions)==0:
            return (self.evaluationFunction(gameState),0)
          minValue=(float("inf"))
          action=0

          for act in actions:
            if(agentIndex==gameState.getNumAgents()-1):
              successorValue=max_value(gameState.generateSuccessor(agentIndex,act),depth+1,a,b)
            else:
              successorValue=min_value(gameState.generateSuccessor(agentIndex,act),agentIndex+1,depth,a,b)
            if successorValue[0]<minValue:
              minValue,action=successorValue[0],act
            if minValue<a:
              return (minValue,action)
            b=min(b,minValue)
          return (minValue,action)
        
        a=-(float("inf"))
        b=(float("inf"))
        max_value=max_value(gameState,0,a,b)[1]
        return max_value
        util.raiseNotDefined()

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
        def max_value(gameState,depth):
          actions=gameState.getLegalActions(0)
          if len(actions)==0 or depth==self.depth or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState),0)
          maxValue=-(float("inf"))
          action=0

          for act in actions:
            successorValue=exp_value(gameState.generateSuccessor(0,act),1,depth)
            if successorValue[0]>maxValue:
              maxValue,action=successorValue[0],act
          return (maxValue,action)
        
        def exp_value(gameState,agentIndex,depth):
          actions=gameState.getLegalActions(agentIndex)
          if len(actions)==0:
            return (self.evaluationFunction(gameState),0)
          expValue=0
          action=0

          for act in actions:
            if(agentIndex==gameState.getNumAgents()-1):
              successorValue=max_value(gameState.generateSuccessor(agentIndex,act),depth+1)
            else:
              successorValue=exp_value(gameState.generateSuccessor(agentIndex,act),agentIndex+1,depth)
            expValue+=successorValue[0]/len(actions)
          return (expValue,action)
        max_value=max_value(gameState,0)[1]
        return max_value
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    food=currentGameState.getFood().asList()
    totalFood=len(food)
    
    capsules=currentGameState.getCapsules()
    totalCapsules=len(capsules)

    pacmanPosition=currentGameState.getPacmanPosition()

    ghosts=currentGameState.getGhostStates()
    scaredGhosts=[]
    activeGhosts=[]
    for ghost in ghosts:
      if ghost.scaredTimer:
        scaredGhosts.append(ghost)
      else:
        activeGhosts.append(ghost)

    score=1.5*currentGameState.getScore()
    score+= -10*totalFood
    score+=-20*totalCapsules

    foodDistances=[manhattanDistance(pacmanPosition,item) for item in food]
    for i in foodDistances:
      if i<3:
        score+= -1*i
      elif i<10:
        score+= -0.45*i
      elif i<16:
        score+= -0.3*i
      else:
        score+= -0.15*i
      
    capsuleDistances=[manhattanDistance(pacmanPosition,item) for item in capsules]
    for i in capsuleDistances:
      if i<3:
        score+= -2*i
      else:
        score+= -0.5*i

    scaredGhostDistances=[manhattanDistance(pacmanPosition,item.getPosition()) for item in scaredGhosts]
    for i in scaredGhostDistances:
      if i<3:
        score+= -3*i
      else:
        score+= -1.2*i

    activeGhostDistances=[manhattanDistance(pacmanPosition,item.getPosition()) for item in activeGhosts]
    for i in activeGhostDistances:
      if i<3:
        score+= 3*i
      elif i<10:
        score+= 1.5*i
      elif i<16:
        score+= 1*i
      else:
        score+= 0.5*i

    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

