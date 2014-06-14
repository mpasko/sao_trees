from random import Random, uniform
from time import time
import inspyred
import trees
import evolution
import logging

class Record:
    def __init__(self,worst,best,average,evaluations):
        self.worst=worst
        self.best=best
        self.average=average
        self.evaluations=evaluations
        self.case=''
    def __str__(self):
        txt="case,worst,best,average,evaluations\n"
        txt+=str(self.case)+","
        txt+=str(self.worst)+","
        txt+=str(self.best)+","
        txt+=str(self.average)+","
        txt+=str(self.evaluations)
        return txt

def merge_records(records):
    if len(records)==0:
        return None
    def arith(items):
        return reduce(lambda x,y:x+y,items)/len(items)
    worst = arith([r.worst for r in records])
    best = arith([r.best for r in records])
    average = arith([r.average for r in records])
    evaluations = arith([r.evaluations for r in records])
    record=Record(worst,best,average,evaluations)
    record.case=records[0].case
    return record

class MemoryHandler:
    def __init__(self,name):
#        logging.Handler.__init__(self)
#        self.level=logging.INFO
        self.name=name
        self.list=[]
    def info(self, record):
        record.case=self.name
        self.list.append(record)
    def emit(self, record):
        self.info(record)

def merge_handlers(handlers):
    dic = dict()
    for h in handlers:
        for j,record in zip(range(len(h.list)),h.list):
            if j not in dic:
                dic[j]=[record]
            else:
                dic[j].append(record)
    return [merge_records(dic[index]) for index in dic]

def logging_observer_factory(logger):
    def logging_observer(population, num_generations, num_evaluations, args):
        best = max(population)
        worst = min(population)
   
        sum=0.0
        for individual in population:
            sum+=individual.fitness
        average=sum/float(len(population))
        logger.info(Record(worst.fitness,best.fitness,average,num_evaluations))
    return logging_observer

def customized_replacer(random, population, parents, offspring, args):
    args['mutation_rate']*=args.get('mutation_cooling',1)
    temporary=args.get('temporary_turn_size',args['tournament_size'])
    temporary*=args.get('tournament_cooling',1)
    args['tournament_size']=int(temporary)
    return inspyred.ec.replacers.steady_state_replacement(random, population, parents, offspring, args)

def perform_run(params):
    global rand
    my_ec = inspyred.ec.EvolutionaryComputation(rand)
    my_ec.selector = inspyred.ec.selectors.tournament_selection
    crossover=inspyred.ec.variators.crossover(evolution.crossover_tree)
    my_ec.variator = [crossover, evolution.mutate_tree]
    my_ec.replacer = customized_replacer
    my_ec.terminator = inspyred.ec.terminators.generation_termination
    my_ec.observer = logging_observer_factory(params['logger'])
    graph=params['graph']
    
    size=params.get('population_size',100)
    final_pop = my_ec.evolve(
        generator = evolution.generate_tree,
        evaluator = evolution.evaluate_tree,
        pop_size = size,
        maximize = False,
        max_evaluations = 6000,
        max_generations = 200,
        num_selected = int(params.get('crossover_probability',0.4)*size),
        mutation_rate = params.get('mutation_rate',0.1),
        mutation_cooling = params.get('mutation_cooling',1.0),
        tournament_cooling = params.get('tournament_cooling',1.0),
        temporary_turn_size = params.get('tournament_percentage',0.3)*size,
        # only int is allowed here:
        tournament_size = int(params.get('tournament_percentage',0.3)*size),
        c = graph.c,
        q = graph.q,
        v2e = graph.v2e,
        best = 100000000000000
    )
    return
    
def subsequent_runs(run_parameters):
    g1 = trees.Graph("benchmark/n010d100C100c001Q100q001s-3i1.txt")
    g2 = trees.Graph("benchmark/n015d100C100c001Q100q001s-3i1.txt")
    g3 = trees.Graph("benchmark/n020d100C100c001Q100q001s-3i1.txt")
    graphs=[g1,g2,g3]
    runs=10
    if 'debug' in run_parameters:
        graphs=[g1]
        runs=1
    
    for graph in graphs:
        handlers=[]
        run_parameters['graph']=graph
        for i in range(runs):
            name=run_parameters['name']
            handler=MemoryHandler(name)
            run_parameters['logger']=handler
            perform_run(run_parameters)
            handlers.append(handler)
        mean=merge_handlers(handlers)
        print "("+name+") next graph is:"
        for mean_record in mean:
            print str(mean_record)
    return

def main():
    global rand
    logger = logging.getLogger('inspyred.ec')
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('inspyred.log', mode='w')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    rand = Random()
    rand.seed(int(time()))
    
    params=dict()
    params['name']='simple'
    params['debug']=True
    subsequent_runs(params)
    params=dict()
    params['name']='mutation_cooling'
    params['mutation_cooling']=0.99
    params['mutation_rate']=1.0
    params['debug']=True
    subsequent_runs(params)
    params=dict()
    params['name']='tournament_cooling'
    params['tournament_cooling']=0.99
    params['tournament_percentage']=1.0
    params['debug']=True
    subsequent_runs(params)

if __name__ == '__main__':
    main()

