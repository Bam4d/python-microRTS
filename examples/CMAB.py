import pyrts
from pyrts import Server
import json
from collections import defaultdict
import random
import logging



class CMABSampleStrategy:

    def __init__(self, name):
        self._name = name

    def sample(self, node):
        raise NotImplementedError()

class Naieve(CMABSampleStrategy):

    def __init__(self, global_MAB, local_MAB, epsilon_global, epsilon_local, epsilon):
        super(Naieve).__init__('Naieve Sampling Strategy')

        self._epsilon = epsilon
        self._epsilon_global = epsilon_global
        self._epsilon_local = epsilon_local

        self._global_MAB = global_MAB
        self._local_MAB = local_MAB

    def sample(self, node):

        valid_actions = node.get_valid_actions()
        # Calculate explore vs explit using epsilon greedy
        # high epsilon mean more likely to explore
        if random.random() < self._epsilon:
            # Explore

        else:
            # Exploit

class TreePolicy:

    def __init__(self, name):
        self._name = name

    def sample(self, node):
        raise NotImplementedError()

class CMAB(TreePolicy):

    def __init__(self, sample_strategy):
        super(CMAB).__init__('CMAB Tree Policy')

        # Contains tuples of {set([(action, unit)]): (times_visited, average_reward)}
        self._global_MAB = []

        # Contains tupes of ((action, unit): (times_visited, average_reward))
        self._local_MAB = []
        self._sample_strategy = sample_strategy(self._global_MAB)

    def sample(self, node):
        self._sample_strategy.sample(node)

class MCTSNode:

    def __init__(self, state, tree_policy):
        self._state = state
        self.reward = 0
        self.children = []

        self.parent = None

        self._tree_policy = tree_policy

    def sample_action(self):
        self._tree_policy.sample(self)

class MCTSTree:

    def __init__(self, initial_state):
        self._root_node = MCTSNode(initial_state)

    def get_root_node(self):
        return self._root_node

    def backup(self, node, reward):

        iter_node = node
        while(iter_node):
            iter_node.reward = reward
            iter_node = iter_node.parent

class CMABAI(Server):

    def __init__(self):
        super(CMABAI, self).__init__()


    def get_action(self, state, gameover):

        return []


