import os
import random
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime


def create_directory(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)


def split_array(array: list) -> list[list]:
    return [array[:i + 1] for i in range(len(array))]


def generate_graph(number_of_nodes: int) -> any:
    n = number_of_nodes
    g = nx.Graph()
    g.add_nodes_from(list(range(1, n + 1)))

    for u in g.nodes:
        for v in g.nodes:
            if u != v:
                tmp = random.randint(1, 10)
                g.add_edge(u, v, weight=tmp)

    print('Graph with', g.number_of_nodes(), 'nodes and', g.number_of_edges(), 'edges successfully created.')

    return g


def draw_graph(g: any, name: str, to_color: list = None) -> any:
    pos: any = nx.spring_layout(g, seed=42)
    labels: any = nx.get_edge_attributes(g, 'weight')
    node_colors = ['blue'] * g.number_of_nodes()

    if to_color is not None:
        for node in to_color:
            node_colors[node - 1] = 'red'

    nx.draw(g, pos, with_labels=True, node_color=node_colors)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels, label_pos=0.5, font_size=5, rotate=False)
    time: str = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    plt.savefig('logs/' + time + '_' + name + '.png', dpi=500)
    plt.clf()

    return g
