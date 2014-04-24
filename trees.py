
from numpy import *
import random
import numpy
import sets

def edge_number(e):
    """Tricky way to convert edge into serial number"""
    """Enumerating as 21,31,32,41,42,43,51,52,53,54,..."""
    edge = e
    #assume first goes biger number
    if e[0]<e[1]:
        edge = [e[1],e[0]]
    x = e[0]-2
    #serial number of first occurence of edge with e[0] (like an arithmetical string)
    first = x * (x + 1) / 2
    #difference grows up since first occurence of e[0]
    difference = e[0]-e[1]
    #here we go
    return first + difference - 1

class Graph:
    """Graph data encapsulated"""
    size=0
    pairWeights=[]
    def len(self):
        return self.size
        
    def __init__(self,size):
        self.size=size
        total = size*(size-1)/2
        sample=numpy.random.random_sample((total, total))
        #Removing diagonal entries, making matrix simmetric
        for x in range(0, total):
            for y in range(0, total):
                if x-y>0:
                    sample[x][y] = sample[y][x]
                elif x==y:
                    sample[x][y] = 0.0
        self.pairWeights=sample
    def debug(self):
        print self.pairWeights
        
    def getValue(self,e1,e2):
        return self.pairWeights[edge_number(e1)][edge_number(e2)]

class Tree:
    """Tree data along with operations to manipulate it"""
    data=[]
    size=0
    weight=0.0
    def randomize(self):
        self.data=[ [x,random.randint(x+1,self.size-1)] for x in range(0, self.size-1)]
    
    def recalc_target(self):
        self.weight=0.0
        for a in self.data:
            for b in self.data:
                self.weight = self.weight + self.graph.getValue(a,b)
    
    def __init__(self,graph):
        self.size=graph.len()
        self.graph=graph
        self.randomize()
        self.recalc_target()
        
    def randomChange(self):
        selection=random.randint(0,self.size-2)
        #edge chosen to remove
        removed=self.data[selection]
        del self.data[selection]
        #produce merging sets (we can still travel to vertexes "navigability[x]" from vertex x)
        navigability=[ sets.Set([x]) for x in range(0, self.size)]
        #removal of an edge splits tree into 2 subtrees
        subset1=navigability[removed[0]]
        subset2=navigability[removed[1]]
        def merge(s_a, s_b):
            s_a.update(s_b)
            s_b.update(s_a)
        for edge in self.data:
            merge(navigability[edge[0]],navigability[edge[1]])
        #last thing is to choose 2 vertexes from both sets to join with new edge
        list1=[x for x in subset1]
        list2=[y for y in subset2]
        a=random.randint(0,len(list1)-1)
        b=random.randint(0,len(list2)-1)
        inserted=[list1[a],list2[b]]
        self.data.append(inserted)
        self.recalc_target()
        
    def debug(self):
        print self.data, "target:",self.weight
        
    def targetFunction(self):
        return self.weight
        
        
if __name__ == '__main__':
    g=Graph(5)
    print g.len()
    t=Tree(g)
    t.debug()
    for x in range(0,40):
        t.randomChange()
        t.debug()