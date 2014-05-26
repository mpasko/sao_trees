
from random import *

seed(None)

class Individual:
    def __init__(self,chromosome):
        self.fitness = 0.0
        self.chromosome = chromosome
    def __str__(self):
        return "fitness:"+ str(self.fitness)+" chromosome:"+ str(self.chromosome)
        

class Genetic:
    def __init__(self, population, target_function, crossover_function, mutation_function):
        self.target_fun = target_function
        self.cross_fun = crossover_function
        self.mutat_fun = mutation_function
        self.population = population
        self.crossover_prob = 0.5
#        self.mutation_prob = 0.01
        self.__cross_last_done=False
        for ind in self.population:
            ind.fitness=target_function(ind.chromosome)
    
    def select(self):
        sum=0.0
        for ind in self.population:
            sum+=ind.fitness
        rand = uniform(0, sum)
        current=0.0
        index=0
        while (current<= rand) and index<len(self.population)-1:
            current+=self.population[index].fitness
            index+=1
        return index
        
    def should_do_sth(self, prob):
        randnum=uniform(0.0,1.0)
        return (randnum <= prob)
    
    def should_do_mutation(self):
        return not self.__cross_last_done
        
    def should_do_crossover(self):
        self.__cross_last_done = self.should_do_sth(self.crossover_prob)
        return self.__cross_last_done
        
    def perform_crossover(self, x, y):
        x_chr = x.chromosome
        y_chr = y.chromosome
        new_ind=None
        if self.should_do_crossover():
            new_chr = self.cross_fun(x_chr,y_chr)
            new_ind = Individual(new_chr)
            new_ind.fitness = self.target_fun(new_chr)
        else:
            #we gotta bloody week -no crossover! ;(
            new_ind = Individual(x_chr)
            #to save one calculation we copy fitness ;)
            new_ind.fitness = x.fitness
        return new_ind
        
    def generation(self):
        new_generation = []
        total = len(self.population)
        for x in range(0,total):
            parent1 = self.population[self.select()]
            parent2 = self.population[self.select()]
            new_individual = self.perform_crossover(parent1,parent2)
            if self.should_do_mutation():
                new_chr = self.mutat_fun(new_individual.chromosome)
                new_fit = self.target_fun(new_chr)
                new_individual.chromosome=new_chr
                new_individual.fitness=new_fit
            new_generation.append(new_individual)
        self.population = new_generation
        
    def generations(self, iterations):
        for x in range(0, iterations):
            self.generation()

            