# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""






import util
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]
def generalSearch(problem,fringe,heuristic=nullHeuristic):
    visited=[]
    path=[]

    if problem.isGoalState(problem.getStartState()):
        return []

    #initial
    if isinstance(fringe,util.PriorityQueueWithFunction):
        element=(problem.getStartState(),[])
        fringe.push(element)
    elif isinstance(fringe,util.PriorityQueue):
        fringe.push((problem.getStartState(),[]),0)
    else:
        fringe.push((problem.getStartState(),[]))

    while not fringe.isEmpty():
        point,path=fringe.pop()
        
        if isinstance(fringe,util.PriorityQueueWithFunction) and point in visited:
            continue
        visited.append(point)

        if problem.isGoalState(point):
            return path
        
        scs=problem.getSuccessors(point)

        if scs:
            for p in scs:
                if p[0] not in visited:
                    if isinstance(fringe,util.Stack):
                        newPath=path+[p[1]]
                        fringe.push((p[0],newPath))
                    elif isinstance(fringe,util.Queue) and p[0] not in (state[0] for state in fringe.list):
                        newPath=path+[p[1]]
                        fringe.push((p[0],newPath))
                    elif isinstance(fringe,util.PriorityQueueWithFunction):
                        newPath=path+[p[1]]
                        element=(p[0],newPath)
                        fringe.push(element)
                    elif isinstance(fringe,util.PriorityQueue):
                        if (p[0] not in (state[2][0] for state in fringe.heap)):
                            newPath = path + [p[1]]
                            pri = problem.getCostOfActions(newPath)
                            fringe.push((p[0],newPath),pri)
                        elif (p[0] in (state[2][0] for state in fringe.heap)):
                            for state in fringe.heap:
                                if state[2][0] == p[0]:
                                    old=problem.getCostOfActions(state[2][1])
                            new=problem.getCostOfActions(path+[p[1]])
                            if old>new:
                                newPath = path + [p[1]]
                                fringe.update((p[0],newPath),new)
                    

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    fringe=util.Stack()
    return generalSearch(problem,fringe)
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
    return generalSearch(problem,fringe)
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe=util.PriorityQueue()
    return generalSearch(problem,fringe)
    util.raiseNotDefined()




def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    fringe=util.PriorityQueueWithFunction(lambda state:problem.getCostOfActions(state[1]) + heuristic(state[0],problem))
    return generalSearch(problem,fringe,heuristic)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
