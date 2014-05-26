
from random import *

seed(None)

class Individual:
    def __init__(self,chromosome, target_fun):
        self.fitness = target_fun(chromosome)
        self.chromosome = chromosome
    def __str__(self):
        return "fitness:"+ str(self.fitness)+ " chromosome:" + str(self.chromosome)

        

class Genetic:
    def __init__(self, population, target_function, crossover_function, mutation_function, crossover_prob = 0.05, mutation_prob = 0.01):
        self.target_fun = target_function
        self.cross_fun = crossover_function
        self.mutat_fun = mutation_function
        self.population = population
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob

        for ind in self.population:
            ind.fitness=target_function(ind.chromosome)
    
    def select(self):
        rand = uniform(0, sum([ ind.fitness for ind in self.population ]))

        current = 0.0
        i=0
        while ((current + self.population[i].fitness) <= rand) and i<len(self.population):
            current+=self.population[i].fitness
            i+=1

        return i
        
    def should_do_sth(self, prob):
        return (uniform(0.0,1.0) <= prob)
    
    def should_do_mutation(self):
        return self.should_do_sth(self.mutation_prob)
        
    def should_do_crossover(self):
        return self.should_do_sth(self.crossover_prob)
        
    def perform_crossover(self, x, y):
        new_chr = self.cross_fun(x.chromosome,y.chromosome)
        return Individual(new_chr, self.target_fun)
        
    def generation(self):
        new_generation = []
        total = len(self.population)

        for x in range(0,total):
            parent1 = self.population[self.select()]
            parent2 = self.population[self.select()]
            new_individual = None
            if (self.should_do_crossover()):
                new_individual = self.perform_crossover(parent1,parent2)
            else:
                new_invidual = Individual(parent1.chromosome, self.target_fun)

            new_generation.append(new_individual)

        self.population = []
        for i in new_generation:
            if self.should_do_mutation():
                self.population.append(Individual(self.mutat_fun(i.chromosome), self.target_fun))
            else:
                self.population.append(Individual(i.chromosome, self.target_fun))

        
    def generations(self, iterations):
        for x in range(0, iterations):
            self.generation()

            