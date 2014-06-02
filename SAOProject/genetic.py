
from random import *
from logging import *
#from guppy import hpy
import os, os.path
import gc

#profiler = hpy()
prof_log=getLogger("Memory")
prof_log.addHandler(FileHandler('memory.log'))
prof_log.setLevel(INFO)

def dump_memory():
    global prof_log
    global profiler
#    prof_log.info(profiler.heap())

def prepare_logger(problem_name):
    dir_name='log_archive'
    number=0
    try:
        os.mkdir(dir_name)
    except OSError:
        number=1+len([fil for fil in os.listdir(dir_name+"/") if os.path.isfile(dir_name+"/"+fil)])
    filename=dir_name+'/'+problem_name+str(number)+'.log'
    print "writing to: ",filename
    log = getLogger("Genetics")
    log.addHandler(FileHandler(filename))
    log.setLevel(INFO)
    return log

seed(None)

class Individual:
    def __init__(self,chromosome, target_fun):
        self.fitness = target_fun(chromosome)
        self.chromosome = chromosome
    def __str__(self):
        return "fitness:"+ str(self.fitness)+ " chromosome:" + str(self.chromosome)


class Genetic:
    def __init__(self, name, population, target_function, crossover_function, mutation_function, crossover_prob = 0.05, mutation_prob = 0.01):
        self.target_fun = target_function
        self.cross_fun = crossover_function
        self.mutat_fun = mutation_function
        self.population = population
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.log = prepare_logger(name)
        self.crossovers_performed=0
        self.mutations_performed=0

        for ind in self.population:
            ind.fitness=target_function(ind.chromosome)
    
    def statistics(self):
        max_fit=-1.0
        min_fit=100000.0
        sum_fit=0.0
        for ind in self.population:
            fit=ind.fitness
            self.log.info("Individual_fitness:"+str(fit))
            if fit > max_fit:
                max_fit=fit
            if fit < min_fit:
                min_fit=fit
            sum_fit+=fit
        self.log.info("Min_fitness:"+str(min_fit))
        self.log.info("Average_fitness:"+str(sum_fit/len(self.population)))
        self.log.info("Max_fitness:"+str(max_fit))
        self.log.info("Crossovers_performed:"+str(self.crossovers_performed))
        self.log.info("Mutations_performed:"+str(self.mutations_performed))
    
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
    
#    @profile
    def generation(self):
        new_generation = []
        total = len(self.population)

        for x in range(0,total):
            parent1 = self.population[self.select()]
            parent2 = self.population[self.select()]
            new_individual = None
            if (self.should_do_crossover()):
                self.crossovers_performed+=1
                new_individual = self.perform_crossover(parent1,parent2)
                gc.collect(2)
            else:
                new_individual = Individual(parent1.chromosome, self.target_fun)

            new_generation.append(new_individual)

        self.population = []
        for i in new_generation:
            if self.should_do_mutation():
                self.mutations_performed+=1
                self.population.append(Individual(self.mutat_fun(i.chromosome), self.target_fun))
            else:
                self.population.append(Individual(i.chromosome, self.target_fun))
        new_generation=[] #for memory optimization purpose
        
    def generations(self, iterations):
        for x in range(0, iterations):
            self.log.info("Producing generation number:"+str(x))
            self.generation()
            gc.collect(2)
            self.statistics()
            dump_memory()
