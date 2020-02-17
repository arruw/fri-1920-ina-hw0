import matplotlib.pyplot as plt
import networkx as nx

G = nx.read_edgelist("./input/karate_club.adj", create_using=nx.DiGraph)
print(f"# nodes: {len(G.nodes)}")
print(f"# edges: {len(G.edges)}")

nx.draw_shell(G, labels={n: n  for n in G.nodes})
plt.savefig("./output/part1.png")
plt.show()