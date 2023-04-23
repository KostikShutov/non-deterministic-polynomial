import networkx as nx
from utils.utils import generate_graph, draw_graph


def greedy(graph: any, weight="weight", source=None) -> any:
    N = len(graph) - 1

    if any(len(nbrdict) - (n in nbrdict) != N for n, nbrdict in graph.adj.items()):
        raise nx.NetworkXError("Graph must be a complete graph.")

    if source is None:
        source = nx.utils.arbitrary_element(graph)

    if graph.number_of_nodes() == 2:
        neighbor = next(graph.neighbors(source))
        return [source, neighbor, source]

    nodeset = set(graph)
    nodeset.remove(source)
    cycle = [source]
    next_node = source

    while nodeset:
        nbrdict = graph[next_node]
        next_node = min(nodeset, key=lambda n: nbrdict[n].get(weight, 1))
        cycle.append(next_node)
        nodeset.remove(next_node)

    cycle.append(cycle[0])

    return cycle


graph = generate_graph(18)
draw_graph(graph, 'greedy')
path = greedy(graph)
print('Path: ', path)
