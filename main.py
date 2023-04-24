from genetic.genetic import simulation as genetic_simulation
from greedy.greedy import simulation as greedy_simulation
from stochastic.stochastic import simulation as stochastic_simulation
from utils.utils import generate_graph, draw_graph

graph = generate_graph(18)
draw_graph(graph, 'main')

print('----Genetic----')
genetic_simulation(graph)
print('----Greedy----')
greedy_simulation(graph)
print('----Stochastic----')
stochastic_simulation(graph)