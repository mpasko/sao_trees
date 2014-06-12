from trees import *
from genetic import *
import matplotlib.pyplot as plt
<<<<<<< HEAD
import copy
=======
>>>>>>> a101bed2cad65208cb7ccb4fe384e451464539c4

if __name__ == '__main__':
    # Create graph
    g = Graph("benchmark/n010d100C010c001Q010q001s-3i1.txt")
    population_size=100
    generations=200
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
        
    def simple_genetic():
        population=create_population()
        gen=BasicGenetic("simple_genetic",population,energy,pleasure,move,crossover_prob,mutation_prob)
        gen.generations(generations)  
        for ind in gen.population:
            ind.fitness = getCost(ind.chromosome,g.q, g.v2e)
            print(ind.fitness)

    def pression_genetic():
        population=create_population()
        gen=BasicGenetic("pression_genetic",population,energy_pression,pleasure,move,crossover_prob,mutation_prob)
        gen.generations(generations) 
        for ind in gen.population:
            ind.fitness = getCost(ind.chromosome,g.q, g.v2e)
            print(ind.fitness)
        
    def tournament_genetic():
        population=create_population()
        gen=BasicGenetic("tournament_genetic",population,energy,pleasure,move,crossover_prob,mutation_prob)
<<<<<<< HEAD
        gen.tournament_percentage = 0.25
        gen.first_win_prob = 0.33
=======
>>>>>>> a101bed2cad65208cb7ccb4fe384e451464539c4
        gen.selection='tournament'
        gen.generations(generations)  
        for ind in gen.population:
            ind.fitness = getCost(ind.chromosome,g.q, g.v2e)
            print(ind.fitness)
            
#    simple_genetic()
#   pression_genetic()
    tournament_genetic()
