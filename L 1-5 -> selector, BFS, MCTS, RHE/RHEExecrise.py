import numpy as np
import copy

import util
from game import Agent, Directions, Actions, random


class RHEAgent(Agent):
    "An agent that does RHE."

    def __init__(self):
        np.random.seed(100) #change seed value to true in pacman
        self.length = 15
        self.actions = [Directions.WEST, Directions.EAST, Directions.SOUTH, Directions.NORTH]
        self.generations = 180
        self.plan = self.RandomPlan()
        self.mutationRate = 0.9
        self.discount = 1
        self.callCount = 0



    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        self.callCount += 1
        fitness = self.getFitness(self.plan, state)
        legalMoves = state.getLegalPacmanActions()
        for i in range(self.generations):
            "*** YOUR CODE HERE ***"

            offspring = self.Mutate(self.plan, state)
            fitnessInn = self.getFitness(offspring, state)
            if fitnessInn > fitness:
               self.plan = offspring
               fitness = fitnessInn

            # mutate the offspring from the current plan.
            # then check its fitness, if this fitness is greater than the current fitness,
            # then the new plan is the current offspring

        while True:
            action = self.plan.pop(0)
            self.plan.append(self.RandomAction())
            if action in legalMoves:#for the first random round
                return action

        # bo jak juz mamy ten przemielony przez algorytm plan to bierzemy pierwsza akcje z planu
         # a zeby utrzymac plan o odpowiedniej dlugosci to musimy dodac element do niego
        # append a random action after the pop so that the plan is always the length it should be.
        # You should check that the action you are using is in a legal move.
        # If it is not you can pop the plan until you have one action that is legal.



        # Filter impossible moves



    def getFitness(self,plan,state):
        nextState = state # dla tego ze bedziemy przypisywac do niego nowe wartosci z generatesuccesor method
        fitness = state.getScore() # jezeli z naszego loopa jeden z possible statow bedzie mial wiekszy wynik to przypiszemy nowa wartosc i zmienimy nextState
        prevScore = fitness
        for actionIndex in range(len(plan)):
            action = plan[actionIndex]
            "*** YOUR CODE HERE ***"
            next1 = nextState.generateSuccessor(0, action)
            if next1.isWin():
                    nextState = next
                    fitness+=nextState.getScore()
                    ghostStates = nextState.getGhostStates()
                    ghostPositions = nextState.getGhostPositions()
                    for ghostState in ghostStates:
                            possibleGhost = self.simulateGhost(ghostState.getPosition(), next1, 0, ghostState)
                            if possibleGhost==next1:
                                    fitness = -np.inf
                                    return fitness
            elif next1.isLose():
                fitness = -np.inf

            # simulate the environment by using the generateSuccessor function. check if the action makes you lose or win.
            # (state.isWin() let you check this. you can here simulate the ghosts and see if pacman dies.
            # (using the simulateGhost function defined in this class)


        return fitness
        # wydaje mi sie ze fitness function bedzie po prostu najwyzszy score

    def getdiscountedChange(self, state, prevScore, index):
        "*** YOUR CODE HERE ***"
        # Generate a discounted value from state.getScore()

        newScore = state.getScore()
        return  newScore

    def simulateGhost(self,position, pacmanPosition, index, state):
        # This was created based on how the directional ghosts move in the code.
        # więc na początku musimy wywolac metode getLegalActions by wobaczyc jakie ruchy duch moze wykonac
        legalActions = state.getLegalActions(index) # index musi byc tutaj jeden bo symulujemy ducha a akcje dla ducha są pod indexem 1
        # teraz inicjujemy dwie zmienne, max przypisujemy bestdistance a nic bestAction
        bestDistance = np.inf
        bestAction = None

        for action in legalActions: #dla każdego możliwego ruchu jaki może wykonać dkuch czyli albo north west east its
            actionVector = Actions.directionToVector(action, 1) # tutaj po prostu zbieramy vektory bo trzeba do nich dodac speed w tym przypadku wynosi on 1 (action, speed)
            newPosition = (position[0] + actionVector[0], position[1] + actionVector[1])
            # no i tutaj porównujemy funkcje, bierzemy tą sciezke, ktora jest najblizej packmana
            distance = util.manhattanDistance(newPosition, pacmanPosition)
            if distance < bestDistance:
                bestDistance = distance
                bestAction = action

        return state.generateSuccessor(index, bestAction)


    def Mutate(self, plan, state):
        offspring = copy.copy(plan)
        nextState = state
        for i in range(len(plan)):
            if(nextState.isWin() or nextState.isLose()):
                return offspring
            action = offspring[i]
            legalMoves = nextState.getLegalPacmanActions()
            legalMoves.remove('Stop')
            "*** YOUR CODE HERE ***"
            if action in legalMoves:
                #if state.generateSuccessor(action).getScore()
                n = random.randint(0, 1)
                if n > self.mutationRate():
                    offspring[i] = self.RandomLegalAction(legalMoves)
            else:
                offspring[i] = self.RandomLegalAction(legalMoves)

            # Check if the action is in the legal moves, if it is not, change the action to a legal move,
            # if it is in the legal moves, then check if it mutates. You can use np.random.random_sample()
            # to simulate a random number 0-1. generate then the next state (you have to use generateSuccessor
        return offspring

    def RandomPlan(self):
        return list(np.random.choice(self.actions,self.length,True))
    def RandomAction(self):
        return np.random.choice(self.actions)
    def RandomLegalAction(self, legalActions):
        return np.random.choice(legalActions)

