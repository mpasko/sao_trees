from random import Random, uniform
from time import time
import inspyred
import trees

def generate_tree(random, args):
    c = args.get('c', None)
    return trees.generateRandomSpanningTree(c)


def evaluate_tree(candidates, args):
    fitness = []
    q = args.get('q', None)
    v2e = args.get('v2e', None)
    for c in candidates:
        fitness.append(trees.getCost(c, q, v2e))
    return fitness

def mutate_tree(random, candidates, args):
    c = args.get('c', None)
    mutation_rate = args.get('mutation_rate', None)
    for cs in candidates:
        if uniform(0.0,1.0) <=mutation_rate:
            trees.mutation(cs, c)

    return candidates

def crossover_tree(random, mom, dad, args):
    # Implementation of paired crossing
    c = args.get('c', None)
    return [ trees.crossover(dad, mom, c)]



def observer_tree(population, num_generations, num_evaluations, args):
    print('{0} evaluations'.format(num_evaluations))
    best = args.get('best', None)
    if population[0].fitness < best:
        best = population[0].fitness
        args['best'] = best
    print(best)
    print(population[0].candidate.edges())


def main(): 


    g = trees.Graph("benchmark/n010d100C100c001Q100q001s-3i1.txt")

    rand = Random()
    rand.seed(int(time()))
    my_ec = inspyred.ec.EvolutionaryComputation(rand)
    my_ec.selector = inspyred.ec.selectors.tournament_selection
    my_ec.variator = [inspyred.ec.variators.crossover(crossover_tree), mutate_tree]
    my_ec.replacer = inspyred.ec.replacers.steady_state_replacement
    my_ec.terminator = [inspyred.ec.terminators.evaluation_termination, inspyred.ec.terminators.average_fitness_termination]
    my_ec.observer = observer_tree


    final_pop = my_ec.evolve(
        generator=generate_tree,
        evaluator=evaluate_tree,
        pop_size=100,
        maximize=False,
        max_evaluations=5000,
        num_selected=50,
        mutation_rate=0.25,
        c = g.c,
        q = g.q,
        v2e = g.v2e,
        best = 100000000000000
    )


    print final_pop
                          
      
            
if __name__ == '__main__':
    main()