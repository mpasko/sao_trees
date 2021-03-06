
from random import *
from logging import *
import os, os.path



def prepare_logger(problem_name):
    dir_name='log_archive'
    number=0
    try:
        os.mkdir(dir_name)
    except OSError:
        number=1+len([fil for fil in os.listdir(dir_name+"/") if os.path.isfile(dir_name+"/"+fil)])
    filename=dir_name+'/'+problem_name+str(number)+'.log'
    print ("writing to: ",filename)
    log = getLogger("Genetics")
    log.addHandler(FileHandler(filename))
    log.setLevel(INFO)
    return log

seed(None)

class Individual:
    def __init__(self,chromosome, fitness):
        self.fitness = fitness
        self.chromosome = chromosome
    def __str__(self):
        return "fitness:" + str(self.fitness)+ " chromosome:" + str(self.chromosome)


class BasicGenetic:
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
        """ Probability that we take the best in tournament selection """
        self.first_win_prob=0.4
        """ It is tournament size as percentage of whole population """
        self.tournament_percentage=0.3
        self.selection = 'roulette'
    
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
        self.log.info("Min_fitness:"+str(1/min_fit))
        self.log.info("Average_fitness:"+str(sum_fit/len(self.population)))
        self.log.info("Max_fitness:"+str(1/max_fit))
        self.log.info("Crossovers_performed:"+str(self.crossovers_performed))
        self.log.info("Mutations_performed:"+str(self.mutations_performed))
    

    # select random individual from population
    # proportionally to its fitness, aka roulette wheel selection
    def roulette_selection(self):
        rand = uniform(0, sum([ ind.fitness for ind in self.population]))
        current = 0.0
        i=0
        while ((current + self.population[i].fitness) <= rand) and i<len(self.population):
            current+=self.population[i].fitness
            i+=1
        return self.population[i]
        
    def tournament_selection(self):
        size = int(len(self.population) * self.tournament_percentage)
        total = len(self.population)
        # Random some subset of population
        tournament = [self.population[randint(0,total-1)] for x in range(size)]
        # Sort it descending
        sortedT = sorted(tournament, key=lambda ind: ind.fitness, reverse=True)
        # Probability that we keep first element
        cond = (uniform(0.0,1.0) <= self.first_win_prob)
        index = 0;
        while (not cond) and index<size-1:
            # If not we get next and next and et caetera...
            cond = (uniform(0.0,1.0) <= self.first_win_prob)
            index=index+1
        return sortedT[index]
           
    def should_mutation(self):
        return uniform(0.0,1.0) <= self.mutation_prob
        
    def should_crossover(self):
        return uniform(0.0,1.0) <= self.crossover_prob
        
  #  @profile
    def generation(self):
        new_generation = []
        total = len(self.population)

        # crossover phase
        for x in range(0,total):
            p1, p2 = [], []
            if self.selection == 'roulette':
                p1, p2 = self.roulette_selection(), self.roulette_selection()
            else:
                p1, p2 = self.tournament_selection(), self.tournament_selection()
                

            if (self.should_crossover()):
                self.crossovers_performed+=1
                new_chr = self.cross_fun(p1.chromosome,p2.chromosome)
                fitness = self.target_fun(new_chr)
                new_generation.append(Individual(new_chr, fitness))
            else:
                new_generation.append(Individual(p1.chromosome, p1.fitness))

        # mutation phase
        self.population = []
        for i in new_generation:
            if self.should_mutation():
                self.mutations_performed+=1
                new_chr = self.mutat_fun(i.chromosome)
                fitness = self.target_fun(new_chr)
                self.population.append(Individual(new_chr, fitness))
            else:
                self.population.append(Individual(i.chromosome, i.fitness))

        
    def generations(self, iterations):
        for x in range(0, iterations):
            self.log.info("Producing generation number:"+str(x))
            self.generation()
            self.statistics()
