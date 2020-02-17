import csv
import re
import networkx as nx
import sqlite3
import matplotlib.pyplot as plt

# # Can not open the connection
# def getConnection(file):
#     conn = None
#     try:
#         conn = sqlite3.connect(file)
#     except sqlite3.Error as e:
#         print(e)
#     return conn

# raw_data = list()
# with getConnection("~/.mozilla/firefox/g7fen7n6.default-release/places.sqlite") as conn:
#     raw_data = conn.execute("""
#         SELECT mh.id, from_visit, url
#         FROM moz_historyvisits mh 
#         INNER JOIN moz_places mp ON mp.id = mh.place_id
#         ORDER BY mh.id 
#         """)

# read raw data
raw_data = list()
with open("input/myhistory.csv") as f:
    reader = csv.reader(f)
    raw_data = list(reader)

# clean raw data
cleaned_data = dict()
for row in raw_data:
    visitId = row[0]
    fromVisitId = row[1]
    url = row[3]

    if(not url.startswith("http")): continue

    match = re.search("^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)", url)
    url = url[match.regs[0][0]:match.regs[0][1]]
    domain = url.split("://")[1]
    baseDomain = ".".join(domain.split(".")[-2:])

    cleaned_data[visitId] = {"fromVisitId": fromVisitId, "domain": baseDomain}


# build network
G = nx.DiGraph()
labels = set()
nodeSize = dict()
edgeSize = dict()
prevNode = {"domain": "0"}
for toKey in sorted(cleaned_data.keys()):
    toNode = cleaned_data[toKey]
    fromNode = cleaned_data.get(toNode["fromVisitId"], prevNode)

    # if fromNode["domain"] == "0": continue

    G.add_edge(fromNode["domain"], toNode["domain"])

    labels.add(fromNode["domain"])
    labels.add(toNode["domain"])
    nodeSize[fromNode["domain"]] = nodeSize.get(fromNode["domain"], 0) + 1
    nodeSize[toNode["domain"]] = nodeSize.get(toNode["domain"], 0)   + 1
    nodeSize[fromNode["domain"]+":"+toNode["domain"]] = nodeSize.get(fromNode["domain"]+":"+toNode["domain"], 0) + 1

    # prevNode = toNode

fig = plt.gcf()
fig.set_size_inches(20,20)
fig.tight_layout()
nx.draw_networkx(G,
    labels={label: label for label in labels},
    node_size = [nodeSize[n] for n in G.nodes()],
    edge_color="gray"
    )
plt.savefig("output/part2.png")
plt.show()