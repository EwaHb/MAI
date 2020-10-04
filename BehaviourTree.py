import numpy as np
from enum import Enum
import searchAgents as sa
import search
import copy

class NodeState(Enum):
    RUNNING = 1
    SUCCESS = 2
    FAILED = 3

class Sequence:
    """ Continues until one failure is found."""
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.state = NodeState.RUNNING

    def add_child(self, child):
        self.children.append(child)
        return child

    def __call__(self, state):
        self.state = NodeState.RUNNING
        ## Your code HERE
        ## do a for loop through the children and check if
        ## the one child node fails, then this failed, until all succeded, then an action is given back.
        
        for node in self.children:
            action = node(state)
            if node.state == NodeState.FAILED:
                self.state = NodeState.FAILED
                return action
        self.state = NodeState.SUCCESS
        return action

        


class Selector:
    """ Continues until one success is found."""
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.state = NodeState.RUNNING

    def add_child(self, child):
        self.children.append(child)
        return child

    def __call__(self, state):
        self.state = NodeState.RUNNING
        ## Your code HERE
        ## do a for loop through the children and check if
        ## the child nodes succeded, then this succeded and the action is given back.
       
        for node in self.children:
            action = node(state)
            if node.state == NodeState.SUCCESS:
                self.state = NodeState.SUCCESS
                return action

        self.state = NodeState.FAILED


## Your code HERE
## implement the valid, Go and Danger classes that are nodes.
## and Add them to the parse_node function. note

class Valid:
    def __init__(self, direc):
        self.state = NodeState.RUNNING
        self.direction = direc
    
    def __call__(self,state):
        if self.direction not in state.getLegalPacmanActions():
            self.state = NodeState.FAILED
        else:
            self.state = NodeState.SUCCESS

class Danger:
    def __init__(self, direc):
        self.state = NodeState.RUNNING
        self.direction = direc

    def __call__(self, state):
        nextState = state.generateSuccessor(0, self.direction)
        if nextState.getPacmanPosition in nextState.getGhostPositions():
            self.state = NodeState.FAILED
            return
        while self.direction in nextState.getLegalPacmanActions():
            nextState = nextState.generateSuccessor(0, self.direction)
            if nextState.getPacmanPosition in nextState.getGhostPositions():
                self.state = NodeState.FAILED
                return
        self.state = NodeState.SUCCESS

class Go:
    def __init__(self, direc):
        self.state = NodeState.RUNNING
        self.direction = direc

    def __call__(self, state):
        self.state = NodeState.SUCCESS
        if self.direction == 'Random':
            return np.random.choice(state.getLegalPacmanActions())
        else:
                return self.direction

                
class CheckCapsules:

    def __init__(self):
        self.state = NodeState.RUNNING
        self.firstEaten = False

    def __call__(self, state):
        capsules = state.getCapsules()
        ## Set deppending on the level!

        if capsules <= 1:
            vals =[]
            # This tries to find the shortest path to the capsule. Note that now it is not doing it.
            for capsule in capsules:
                problem = sa.PositionSearchProblem(state, goal=capsule)
                vals.append(search.tinyMazeSearch(problem))
            path = sorted(vals, key=len)[0]
            self.state = NodeState.SUCCESS
            return path[0]
        else:
            self.state = NodeState.FAILED
            return None


class badsearch:
    """ Return <direction> as an action. If <direction> is 'Random' return a random legal action
    """
    def __init__(self):
        self.state = NodeState.RUNNING

    def __call__(self, state):
        self.state = NodeState.SUCCESS
        problem = sa.PositionSearchProblem(state)
        vals = search.tinyMazeSearch(problem)
        return vals[0]




def parse_node(encode, parent=None):
    if isinstance(encode[0], list):
        parse_node(encode[0], parent)
        parse_node(encode[1:], parent)

    elif encode[0] is "SEQ":
        if parent is not None:
            node = parent.add_child(Sequence(parent))
        else:
            node = Sequence(parent)
            parent = node
        parse_node(encode[1:], node)

    elif encode[0] is "SEL":
        if parent is not None:
            node = parent.add_child(Selector(parent))
        else:
            node = Selector(parent)
            parent = node
        parse_node(encode[1:], node)

    elif encode[0].startswith("Valid"):
        arg = encode[0].split('.')[-1]
        parent.add_child(Valid(arg))
        if len(encode) > 1:
            parse_node(encode[1:], parent)

    elif encode[0].startswith("Danger"):
        arg = encode[0].split('.')[-1]
        parent.add_child(Danger(arg))
        if len(encode) > 1:
            parse_node(encode[1:], parent)

    elif encode[0].startswith("Go"):
        arg = encode[0].split('.')[-1]
        parent.add_child(Go(arg))
        if len(encode) > 1:
            parse_node(encode[1:], parent)


    elif encode[0].startswith("CheckCapsules"):
        arg = encode[0].split('.')[-1]
        ## TODO: note how you can add args to the function
        ## parent.add_child(CheckCapsules(arg))
        parent.add_child(CheckCapsules())
        if len(encode) > 1:
            parse_node(encode[1:], parent)
    elif encode[0].startswith("bad"):
        parent.add_child(badsearch())
        if len(encode) > 1:
            parse_node(encode[1:], parent)
    else:
        print("Unrecognized in ")
        raise Exception

    return parent




