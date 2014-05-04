from random import choice
from re import split
from anneal import Annealer
import numpy as np
import networkx as nx

class Graph:
    """Graph data loaded from file"""       
    def __init__(self,filename):
        with open(filename) as f:
            # loading from file
            order = int(f.readline().replace("param n :=", "").replace(";", ""))
            size = int(f.readline().replace("param m :=", "").replace(";", ""))
            f.readline()
            edgesLine = [x for x in f.readline().replace("param c := ", "").replace(" ;", "").split("\t") if "\n" not in x]
            edges = [[int(y) for y in split('\[|\]|,',x) if y != ''] for x in edgesLine]
            f.readline()
            edgePairsLine = [x for x in f.readline().replace(" ;", "").split("\t")  if "\n" not in x]
            edgePairs = [[int(y) for y in split('\[|\]|,',x) if y != ''] for x in edgePairsLine]

            # converting to representation recognizable by networkX
            edgeList = [(edge[0]-1, edge[1]-1, { 'weight' : edge[2] } ) for edge in edges]
            # mapping between [v1,v2] and edge number used in q
            v2e = {(x[0],x[1]) : edgeList.index(x) for x in edgeList } 
            
            edgePairList = [(v2e[(edge[0]-1, edge[1]-1)], v2e[(edge[2]-1, edge[3]-1)], { 'weight' : edge[4] } ) for edge in edgePairs]
        
            self.c = nx.Graph(edgeList)  # adjacency matrix
            self.q = nx.Graph(edgePairList) # matrix of costs between pairs of edges
            self.v2e = v2e


class SpanningTree:
    """Tree data along with operations to manipulate it"""
    def __init__(self,graph):
        self.graph = graph
        self.tree = self.randomSpanningTree()

    """ Generating random spanning tree using DFS search. Connecting each vertex to its predecessor generates spanning tree. """
    def randomSpanningTree(self):
        graph = self.graph.c
        source = choice(graph.nodes()) # random start element
        spanning_tree = nx.Graph()
        # random spanning tree from predecessors
        spanning_tree.add_edges_from([(u,v) for u,v in nx.dfs_predecessors(graph, source).items()])
        return spanning_tree
    
    """ Cost of solution. The lower the better. """
    def getCost(self):
        edgeCosts = self.graph.c
        pairCosts = self.graph.q
        tree = self.tree

        s = sum([edgeCosts.get_edge_data(uv[0],uv[1])["weight"] for uv in tree.edges()])
        edgePairs = [(self.graph.v2e[x], self.graph.v2e[y]) for x in tree.edges() for y in tree.edges()]
        s += sum([pairCosts.get_edge_data(e[0],e[1])["weight"] for e in edgePairs if e[0] != e[1]]) 

        return s
    
    """ Makes random change to the state """
    def randomChange(self):
        # edge chosen to remove
        tree = self.tree 
        graph= self.graph.c
        v1 = choice(tree.nodes())
        v2 = choice(tree.neighbors(v1))
        #removal of an edge splits tree into 2 subtrees
        tree.remove_edge(v1,v2)

        # we obtain nodes accesible from each vertex
        n1 = nx.dfs_tree(tree, v1).nodes()
        n2 = nx.dfs_tree(tree, v2).nodes()

        # we list possible candidates for new connection
        possible_connections = [(u,v) for u in n1 for v in n2 if graph.has_edge(u, v)]
        possible_connections.remove((v1,v2)) # remove previous connection

        if possible_connections == []:
            tree.add_edge(v1, v2) # no changes
        else:
            edge = choice(possible_connections)
            tree.add_edge(edge[0], edge[1]) # new node

    def copy(self):
        g = SpanningTree(self.graph)
        g.tree = self.tree.copy()

        return g

        

def energy(state):
    return state.getCost()

def move(state):
    state.randomChange()


        
if __name__ == '__main__':
    g = Graph("benchmark/n030d100C010c001Q010q001s-3i1.txt")
    state = SpanningTree(g)

    annealer = Annealer(energy, move)
    schedule = annealer.auto(state, minutes=1)
    state, e = annealer.anneal(state, schedule['tmax'], schedule['tmin'],  schedule['steps'], updates=6)
    print(state.getCost())


    