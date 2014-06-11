from random import choice, shuffle, uniform
from re import split
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

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

            # converting to representation recognizable by networkX ( zero-based indexing )
            edgeList = [(edge[0]-1, edge[1]-1) for edge in edges]
            # inverse of above, given edge tuple returns its index
            v2e = {(x[0],x[1]) : edgeList.index(x) for x in edgeList } 
            
            # pair costs are encoded as costs of edges between edges
            # edge own costs is encoded as costs of loop connecting it to itself
            q = np.zeros( (len(edgeList), len(edgeList)) )
            for edge in edgePairs:
                q[v2e[(edge[0]-1, edge[1]-1)], v2e[(edge[2]-1, edge[3]-1)]] = edge[4]

            for edge in edges:
                q[v2e[(edge[0]-1, edge[1]-1)], v2e[(edge[0]-1, edge[1]-1)]] = edge[2]

            self.c = nx.Graph(edgeList)  # adjacency matrix
            self.q = nx.Graph(q) # matrix of costs between pairs of edges
            self.v2e = v2e

""" 
Generate a random tree using random walk over the graph.

Based on RandomTreeWithRoot algorithm from: http://www.cs.cmu.edu/~15859n/RelatedWork/RandomTrees-Wilson.pdf

"""
def generateRandomSpanningTree(graph):
    root = choice(graph.nodes())
    Tree = set()
    Next = { }
    Tree.add(root)
    Next[root] = None

    for i in graph.nodes():
        u = i
        while u not in Tree:
            Next[u] = choice(graph.neighbors(u))
            u = Next[u]

        u = i

        while u not in Tree:
            Tree.add(u)
            u = Next[u]

    spanning_tree = nx.Graph()
    for u,v in Next.items():
        if v != None:
            spanning_tree.add_edge(u,v)

    return spanning_tree

""" 
Get the cost of the tree.
"""
def getCost(tree, edgePairCosts, v2e):  
    cost = 0.0
    edges = tree.edges()
    for x in edges:
        for y in edges:
            cost += edgePairCosts.get_edge_data(v2e[x],v2e[y])["weight"]

    return cost
""" 
Mutate the tree. Select random edge. Delete it and then try to connect two smaller trees with another edge. 
If no other is available return to initial tree.
"""
def mutation(tree, graph):
    v1 = choice(tree.nodes())
    v2 = choice(tree.neighbors(v1)) # choice could be made to be proportional to weight of removed edge (the bigger the weight the more probably to be removed)
    #removal of an edge splits tree into 2 subtrees
    tree.remove_edge(v1,v2)

    # we obtain nodes accesible from each vertex
    n1 = nx.dfs_tree(tree, v1).nodes()
    n2 = nx.dfs_tree(tree, v2).nodes()

    # we list possible candidates for new connection
    possible_connections = [(u,v) for u in n1 for v in n2 if graph.has_edge(u, v)]

    if possible_connections == []:
        tree.add_edge(v1, v2) # no changes
    else:
        possible_connections.remove((v1,v2)) # remove previous connection
        edge = choice(possible_connections)
        tree.add_edge(edge[0], edge[1]) # new node
""" 
Find common edges in both trees. Find largest connected subgraph in resulting graph.
Build the rest of the graph using random walk.
"""
#@profile
def crossover(t1, t2, graph):
    # here we get from |V-1| edges (when two graphs are identical) 
    # to minimum 1 common edge
    edges = nx.compose(t1,t2).edges()
    shuffle(edges)
    # we select the largest resulting subgraph

    g = nx.Graph()
    g.add_nodes_from(t1.nodes())
    for edge in edges:
        if g.size()  == t1.order() - 1:
            break
        if not nx.has_path(g, edge[0], edge[1]):
            g.add_edge(edge[0], edge[1])
    
    if uniform(0,1) <= 0.25:        
        if nx.intersection(t1,t2).size() ==  t1.size():
            mutation(g, graph)

    return g
      
if __name__ == '__main__':
    g = Graph("benchmark/n010d100C010c001Q010q001s-3i1.txt")
    def energy(tree):
        return getCost(tree, g.q, g.v2e)

    def move(tree):
        mutation(tree, g.c)
    

    plt.figure()
    tree = generateRandomSpanningTree(g.c)
    nx.draw_circular(tree)
    plt.show()
    tree1 = generateRandomSpanningTree(g.c)
    plt.figure()
    nx.draw_circular(tree1  )
    plt.show()
    
    mutation(tree, g.c)
    plt.figure()
    nx.draw_circular(tree)
    plt.show()
    print(getCost(tree, g.q,g.v2e))
    print(getCost(tree1, g.q,g.v2e))
    print(getCost(tree2, g.q,g.v2e))
    
    

    


    
