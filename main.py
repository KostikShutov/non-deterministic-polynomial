import os
import time
from genetic.genetic import simulation as genetic_simulation
from greedy.greedy import simulation as greedy_simulation
from stochastic.stochastic import simulation as stochastic_simulation
from utils.utils import generate_graph, draw_graph


def create_directory(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)


def print_time(start_time: float) -> None:
    print('Execution time: %s seconds' % (time.time() - start_time))


create_directory('logs')
graph = generate_graph(18)
draw_graph(graph, 'main')

print('\n----Genetic----')
start_time = time.time()
genetic_simulation(graph)
print_time(start_time)

print('\n----Greedy----')
start_time = time.time()
greedy_simulation(graph)
print_time(start_time)

print('\n----Stochastic----')
start_time = time.time()
stochastic_simulation(graph)
print_time(start_time)
