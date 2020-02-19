import csv
import re
import networkx as nx
from statistics import mean 

# read raw data
raw_data = list()
with open("input/raw_history_data.csv") as f:
    raw_data = list(csv.reader(f))

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
prevNode = {"domain":"/"}
for key in sorted(cleaned_data.keys()):
    node = cleaned_data[key]
    prevNode = cleaned_data.get(node["fromVisitId"], prevNode)
    edge = f"{prevNode['domain']}:{node['domain']}"
    edges[edge] = edges.get(edge, 0) + 1

G = nx.DiGraph()
G.add_weighted_edges_from([(*edge.split(":"), weight) for edge,weight in edges.items()])

print(f"# nodes: {len(G.nodes)}")
print(f"# edges: {len(G.edges)}")
print(f"avg degree: {mean(map(lambda t: t[1], G.degree()))}")