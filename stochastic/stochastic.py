import copy
import time
import random
import numpy as np
import networkx as nx
from utils.utils import draw_graph


class Network:
    def __init__(self, num_of_node, side_length):
        self.num_of_node = num_of_node
        self.side_length = side_length
        self.initialize_graph()

    def initialize_graph(self):
        # Generate random node position
        nodes = np.random.randint(self.side_length, size=self.num_of_node * 2)
        nodes = nodes.reshape(self.num_of_node, 2)
        self.positions = {key: tuple(node) for key, node in enumerate(nodes)}

        # Set up the graph
        self.graph = nx.Graph()
        self.graph.add_nodes_from([i for i in range(self.num_of_node)])

        # Set up edge and edge weight
        for i in range(self.num_of_node - 1):
            d = nodes[i] - nodes[i + 1:, :]
            weight = (d[:, 0] ** 2 + d[:, 1] ** 2) ** 0.5
            weighted_edges = [(i, i + j, weight[j - 1]) for j in range(1, self.num_of_node - i)]
            self.graph.add_weighted_edges_from(weighted_edges)

        draw_graph(self.graph, 'stochastic')


class Node:
    def __init__(self, parent, node, path, unvisited_nodes, cost):
        self.parent = parent
        self.node = node
        self.path = path
        self.unvisited_nodes = unvisited_nodes
        self.cost = cost
        self.num_of_visit = 1
        self.estimate = None
        self.score = None
        self.policy = None
        self.expandables = copy.deepcopy(unvisited_nodes)
        random.shuffle(self.expandables)
        self.expanded = {}

    def calculate_score(self, C=1):
        self.score = self.estimate + C * (np.log(self.parent.num_of_visit) / self.num_of_visit) ** 0.5


class MCTS:
    def __init__(self, network):
        self.num_of_node = network.num_of_node
        self.graph = network.graph
        self.root = Node(None, 'root', [], list(self.graph.nodes), 0)

    def select(self, node):
        if node.policy is None:
            return node
        else:
            return self.select(node.policy)

    def expand(self, node):
        new_node = node.expandables.pop()
        new_path = copy.deepcopy(node.path)
        new_path.append(new_node)
        new_unvisited_nodes = copy.deepcopy(node.unvisited_nodes)
        new_unvisited_nodes.remove(new_node)
        new_cost = copy.deepcopy(node.cost)
        if node.node != 'root':
            new_cost += self.graph.edges[node.node, new_node]['weight']
        new_node_object = Node(node, new_node, new_path, new_unvisited_nodes, new_cost)
        node.expanded[new_node] = new_node_object
        return new_node_object

    def backpropagate(self, node):
        # Decide policy for this node
        scores = []
        for key, n in node.expanded.items():
            if node.node != 'root':
                scores.append([key, n.score + self.graph.edges[node.node, n.node]['weight']])
            else:
                scores.append([key, n.score])
        scores = np.array(scores)
        node.score = sum(scores[:, 1]) / len(scores)
        node.policy = node.expanded[scores[np.argmin(scores[:, 1])][0]]

        if node.node != 'root':
            # Evaluate how good this node is as a child
            estimates = []
            for key, n in node.expanded.items():
                estimates.append([key, n.estimate + self.graph.edges[node.node, n.node]['weight']])
            estimates = np.array(estimates)
            node.estimate = sum(estimates[:, 1]) / len(estimates)
            node.calculate_score()

            # Keep going until root node
            self.backpropagate(node.parent)

    def calculate_path_edges(self, path):
        path_edges = []
        cost = 0
        current_node = path.pop()
        while len(path) > 0:
            next_node = path.pop()
            path_edges.append(tuple([current_node, next_node,
                                     self.graph.edges[current_node, next_node]]))
            cost += path_edges[-1][2]['weight']
            current_node = next_node
        path_edges.append(tuple([path_edges[-1][1], path_edges[0][0],
                                 self.graph.edges[path_edges[-1][1], path_edges[0][1]]]))
        cost += path_edges[-1][2]['weight']
        return path_edges, cost

    def run(self, num_of_expand, num_of_simulate, C):
        while True:
            current_node = self.select(self.root)

            # Reach the end, break condition
            if len(current_node.path) == self.num_of_node:
                break

            # Expand and simulate
            for i in range(min(num_of_expand, len(current_node.expandables))):
                new_node = self.expand(current_node)
                costs = []
                for j in range(num_of_simulate):
                    costs.append(self.simulate(new_node))
                new_node.estimate = sum(costs) / num_of_simulate
                new_node.calculate_score()

            # Back up the estimate, calculate score, and update policy
            self.backpropagate(current_node)

        return self.calculate_path_edges(current_node.path)


class RandomMCTS(MCTS):
    def __init__(self, network):
        MCTS.__init__(self, network)

    def simulate(self, node):
        # Setup
        unvisited_nodes = copy.deepcopy(node.unvisited_nodes)
        random.shuffle(unvisited_nodes)
        current_node = node.node
        cost = 0

        # Path finding
        while len(unvisited_nodes) > 0:
            next_node = unvisited_nodes.pop()
            cost += self.graph.edges[current_node, next_node]['weight']
            current_node = next_node

        cost += self.graph.edges[current_node, node.path[0]]['weight']

        return cost


def run_trail(network):
    start = time.time()
    random_mcts = RandomMCTS(network)
    edges, cost = random_mcts.run(50, 20, 100)
    run_time = time.time() - start

    return edges, cost, run_time


def simulation(num_of_node, side_length=100):
    network = Network(num_of_node, side_length)
    edges, cost, run_time = run_trail(network)

    print("Random mcts has average cost of {:.2f}".format(cost))
    print('Path: ', edges)


simulation(30)