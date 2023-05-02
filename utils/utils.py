import random
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime


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
    nx.draw_spring(g, with_labels=True)

    return g


def draw_graph(g: any, name: str) -> None:
    pos: any = nx.spring_layout(g)
    labels: any = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels, font_size=5)
    time: str = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    plt.savefig('logs/' + time + '_' + name + '.png', dpi=500)
