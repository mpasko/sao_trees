from trees import *
from genetic import *
import matplotlib.pyplot as plt
import copy

if __name__ == '__main__':
    # Create graph
    g = Graph("benchmark/n010d100C010c001Q010q001s-3i1.txt")
    population_size=10
    generations=40
    crossover_prob=0.4
    mutation_prob=0.1
    
    def energy(tree):
        # genetic is maximizing
        # we would like to minimize spanning tree
        return 1/getCost(tree, g.q, g.v2e)
        
    def energy_pression(tree):
        cost = getCost(tree, g.q, g.v2e)
        return 1/(cost**2);

    def move(tree):
        mutant=tree.copy()
#        print "before mutation:", tree.nodes()
        mutation(mutant, g.c)
        return mutant
        
    def pleasure(active_one, passive_one):
#        print "before crossover:", active_one.nodes(), passive_one.nodes()
        child=crossover(active_one, passive_one, g.c)
#        print "after crossover:", child.nodes()
        return child
        
    def create_population():
        population=[]
        for x in range(0, population_size):
            tree = generateRandomSpanningTree(g.c)
            ind = Individual(tree,energy(tree))
            population.append(ind)
        return population
        
    population=create_population()
    gen=Genetic("simple_genetic",population,energy,pleasure,move,crossover_prob,mutation_prob)
    gen.generations(generations)  
    for ind in gen.population:
        ind.fitness = energy(ind.chromosome)
        print(ind.fitness)
    population=create_population()
    gen=Genetic("pression_genetic",population,energy_pression,pleasure,move,crossover_prob,mutation_prob)
    gen.generations(generations) 
    for ind in gen.population:
        ind.fitness = energy(ind.chromosome)
        print(ind.fitness)
