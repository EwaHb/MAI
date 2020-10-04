
from collections import defaultdict, namedtuple
import math
import numpy as np
from random import choice


from pacman import readCommand
from pacman import runGames
from MCTS_utils import Node, play_game
from searchAgents import PositionSearchProblem
"""
A minimal implementation of Monte Carlo tree search (MCTS) in Python 3
Adapted by Toke Faurby in January 2020, based on previous work by
Luke Harold Miles, July 2019.
    https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
See also 
    https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
Public Domain Dedication
"""

PACMAN = True
TICTACTOE_VS_HUMAN = False
TICTACTOE_DETERMINIST = False

class MCTSagent:
    "Monte Carlo tree searcher. First rollout the tree then choose a move."
    def __init__(self, exploration_weight=1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight
        self.simulate_steps = 5
        self.num_rollout = 50

    def reset(self, state):
        """ ONLY NEEDED FOR PACMAN - PREVENT MEMORY LECKAGE"""
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        state.getAndResetExplored()

    def getAction(self, state):
        """ ONLY NEEDED FOR PACMAN """
        self.reset(state)
        node = Node(state)

        for i in range(self.num_rollout):
            self.do_rollout(node)
        best_successor = self.choose(node)
        action = best_successor.state.getPacmanState().getDirection()
        if action not in state.getLegalPacmanActions():
            # print('Action', action, 'not legal - "Stop" action instead.')
            action = 'Stop'
        return action

    def choose(self, node):
        """ Choose the best successor of node. (Choose a move in the game)
        """
        if node.is_terminal():
            raise RuntimeError("choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n): # here we have a function that is being used in the 71st line
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / float(self.N[n])  # average reward

        return max(self.children[node], key=score)

    def do_rollout(self, node):
        """ Make the tree one layer better. (Train for one iteration.)
        """
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

    def _select(self, node):
        """ Find an unexplored descendent of `node`
            1) check if node is unexplored or terminal
                if so, return path
            2) check if the node has any unexplored children
                if so append it to path and return path
            3) select a new node using uct and go back to 1)
            TIP: I had an issue with infinite paths, so
                if len(path)>100 then return path
            returns a list of nodes, the last one being a leaf node.


        path = []
        def ewas_recursion(node):
            if node not in node.get_explored_MCTS_utils or node.is_terminal():
                return path

            for nino in node.find_children:
                if nino not in node.get_explored_MCTS_utils:
                    path.append(nino)
            return path

            if len(path) > 100:
                return path
            new_node = self._uct_select(node)
            my_recursion(new_node)

        ewas_recursion(node)
        return path
        """

        path = []
        while True:
            path.append(node)

            if len(path) > 100:
                return path
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper



    def _expand(self, node): # adds the node to the mcts tree! to jest haszmapa gdzie key to node a value to path of nodes ktore sa jego dziecmi!
        """ Update the self.children dict with the children of `node`
            If node is already in self.children then do nothing.
            Otherwise add the children of node (node.find_children())
            to self.children, using node as the hash
            returns nothing


        pass
        """
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children()


    def _simulate(self, node):
        """ Returns the reward for a random simulation (to completion) of `node`"
            1) for a fixed number of steps, or until termination do
            1a) check if node is terminal, if so return the reward
            1b) select a random action
            returns a number
        """
        if PACMAN:
            while True:
                if node.is_terminal():
                    reward = node.reward()
                    return reward
                #action = self.getAction(node.state)
                #node = node.make_action(action)
                node = node.find_random_child()

            """
            while True:
                if node.is_terminal():
                    reward = node.reward()
                    return reward
                node = node.find_random_child()
            """


        else:  # Tic Tac Toe
            invert_reward = True
            while True:
                if node.is_terminal():
                    reward = node.reward()
                    return 1 - reward if invert_reward else reward
                node = node.find_random_child()
                invert_reward = not invert_reward #its like not not gives true

    def _backpropagate(self, path, reward):
        """ Send the reward back up to the ancestors of the leaf
            for each node in the path increase the coresponding ellements
            of self.N and self.Q with 1 and the reward respectively.
            returns nothing
            [a,b,a,d,a]
        """

        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward



            ## IGNORE THIS - Tic Tac Toe specific ##
            if not PACMAN:
                # Tic Tac Toe is strange, don't worry about it
                reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa
                # this changes the value

    def _uct_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)


if __name__ == '__main__':
    if PACMAN:  # PacMan
        str_args = ['-l', 'mediumClassic', '-g', 'DirectionalGhost', '--frameTime', '0', '-n', '100']
        str_args = ['-l', 'TinyMaze', '-g', 'DirectionalGhost', '--frameTime', '0', '-n', '100']
        str_args = ['-l', 'TestMaze', '-g', 'DirectionalGhost', '--frameTime', '0', '-n', '100']
        args = readCommand(str_args)
        # args['display'] = textDisplay.NullGraphics()  # Disable rendering

        args['pacman'] = MCTSagent()
        out = runGames( **args)

        scores = [o.state.getScore() for o in out]
        print(scores)

    else:  # TicTacToe
        winner = []
        n = 200
        for i in range(n):
            winner.append(play_game(MCTSagent(), human=TICTACTOE_VS_HUMAN, deterministic=TICTACTOE_DETERMINIST))
            print("Game", i)
        print('MCTS win:  ', np.sum([i == -1 for i in winner])/float(n))
        print('Draw:      ', np.sum([i == 0 for i in winner])/float(n))
        print('MCTS loose:', np.sum([i == 1 for i in winner])/float(n))
        print('')