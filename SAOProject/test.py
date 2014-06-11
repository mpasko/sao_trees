
from genetic import *

def fun(x):
    if x < 0:
        return 0.0
    if x > 100:
        return 0.0
    return (1.0 - float(x)/100.0)**2;
    
def crossover(x,y):
    point = randint(0,7)
    xmask=2**point-1
    ymask=255-xmask
    px=x & xmask
    py=y & ymask
    return px | py
    
def mutation(x):
    point = randint(0,7)
    return x^point

if __name__ == '__main__':
    popul=[]
    for x in range(0, 100):
        val = randint(0,100)
        ind = Individual(val,fun)
        popul.append(ind)
        print(str(ind))
    
    gen=BasicGenetic("test",popul,fun,crossover,mutation)
    #every problem must have its own configuration
    gen.crossover_prob = 0.8
    gen.generations(50)
    print("Result: (size ",len(gen.population), ")")
    for ind in gen.population:
        ind.fitness = fun(ind.chromosome)
        print(str(ind))
