import sys
import time
from greedy.greedy import greedy
from stochastic.stochastic import stochastic
from utils.utils import create_directory, split_array, generate_graph, draw_graph


def print_info(__start_time: float, __path: list, __cost: float, __graph: any, __name: str) -> None:
    print('Execution time: %s seconds' % (time.time() - __start_time))
    print('Path:', __path)
    print('Cost:', __cost)

    for i, sub in enumerate(split_array(__path)):
        draw_graph(
            g=__graph.copy(),
            name=__name + '_' + str(i + 1),
            to_color=sub,
        )


create_directory('logs')
graph = generate_graph(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
draw_graph(graph.copy(), 'graph')

print('\n----Greedy----')
start_time = time.time()
path, cost = greedy(graph)
print_info(start_time, path, cost, graph.copy(), 'greedy')

print('\n----Stochastic----')
start_time = time.time()
path, cost = stochastic(graph)
print_info(start_time, path, cost, graph.copy(), 'stochastic')
