import networkx as nx
from statistics import mean 
from scipy.special import binom

# requested number of nodes and edges
N = 1123
E = 2384

# calculate probability p and construct random network
p = E/binom(N, 2)
G = nx.erdos_renyi_graph(N, p, seed=0)

# PageRank
rankings = nx.pagerank(G)

# print results
{print(f"{k}: {v:.5f}") for k, v in
    sorted(rankings.items(), key=lambda item: item[1], reverse=True)[:8]}
