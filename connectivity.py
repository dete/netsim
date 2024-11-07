import networkx as nx
import math
from itertools import combinations

def get_coprimes(n, count):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    coprimes = []
    num = 1
    while len(coprimes) < count:
        if gcd(num, n) == 1:
            coprimes.append(num)
        num += 1
    return coprimes


n = 201
G = nx.Graph(nodes=range(n))
cycles = get_coprimes(n, math.ceil(n / 6))

print(cycles)

for i in range(n):
    for c in cycles:
        G.add_edge(i*c % n, (i + 1)*c % n)

# Find the minimum node cut
node_cut = nx.minimum_node_cut(G)
print(f"Minimum node cut: {len(node_cut)} {node_cut}")
girth = nx.girth(G)
print(f"Girth: {girth}")
degrees = [d for n, d in G.degree()]
minimum_degree = min(degrees)
print(f"Minimum degree: {minimum_degree}")
maximum_degree = max(degrees)
print(f"Maximum degree: {maximum_degree}")
