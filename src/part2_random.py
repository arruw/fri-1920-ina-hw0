import networkx as nx
from statistics import mean 
from scipy.special import binom

# requested number of nodes and edges
N = 1123
E = 2384

# calculate probability p and construct random network
p = E/binom(N, 2)
G = nx.erdos_renyi_graph(N, p, seed=0)

# print the results
print(f"# nodes: {len(G.nodes)}")
print(f"# edges: {len(G.edges)}")
print(f"avg degree: {mean(map(lambda t: t[1], G.degree()))}")