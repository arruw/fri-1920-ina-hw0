import csv
import re
import networkx as nx
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import math
from matplotlib import colors as mcolors

# read raw data
raw_data = list()
with open("input/raw_history_data.csv") as f:
    reader = csv.reader(f)
    raw_data = list(reader)

# clean raw data
cleaned_data = dict()
for row in raw_data[1:]:
    visitId = int(row[0])
    fromVisitId = int(row[1])
    url = row[3]

    if(not url.startswith("http")): continue

    match = re.search("^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)", url)
    url = url[match.regs[0][0]:match.regs[0][1]]
    domain = url.split("://")[1]
    baseDomain = ".".join(domain.split(".")[-2:])

    cleaned_data[visitId] = {"fromVisitId": fromVisitId, "domain": baseDomain}

# build network
edges = dict()
nodes = dict()
prevNode = {"domain":"/"}
for key in sorted(cleaned_data.keys()):
    node = cleaned_data[key]
    prevNode = cleaned_data.get(node["fromVisitId"], prevNode)
    edge = f"{prevNode['domain']}:{node['domain']}"
    edges[edge] = edges.get(edge, 0) + 1

G = nx.DiGraph()
G.add_weighted_edges_from([(*edge.split(":"), weight) for edge,weight in edges.items()])

# PageRank
rankings = nx.pagerank(G)

# trim the network
rankLimit = sorted(rankings.values())[-200]
G.remove_nodes_from([n for n in G.nodes() if rankings[n] < rankLimit])

# node size normalization parameters
minRank = rankLimit
maxRank = max(rankings.values())
minNew = 10
maxNew = 600

# draw network
with open("input/domain_blacklist.txt") as f:
    blacklist = [l.strip() for l in f.readlines()]

pos = nx.kamada_kawai_layout(G)

fig: Figure = plt.gcf()
fig.set_size_inches(20,20)
fig.set_dpi(200)
fig.tight_layout()
nx.draw_networkx_nodes(G, pos,
    node_size = [(maxNew-minNew)/(maxRank-minRank)*(rankings[n]-maxRank)+maxNew for n in G.nodes()],
    alpha=1.0)
nx.draw_networkx_labels(G, pos,
    labels={n: "" if n in blacklist else n for n in G.nodes()},
    font_size=6)
nx.draw_networkx_edges(G, pos,
    edge_color="gray",
    alpha=0.3)
plt.savefig("output/part2.png", bbox_inches='tight')
# plt.show()